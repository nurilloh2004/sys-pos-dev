from rest_framework import permissions, generics
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from .response import ResponseController
from .status import *
from .pagination import CustomPagination
from apps.products.models import Brand, Attribute, AttributeValue, Measurement, Category
from apps.upload.models import UploadFile, BaseProductImage
from .controller import Controller
from apps.core.exception.custom_exception import CustomValidationError
from apps.outlets.models import User, Outlet


class ViewMixin(Controller):

    ASC = "id"
    DESC = "-id"

    ORDER_BY = {
        "ASC": ASC,
        "DESC": DESC
    }
    URL_IDS = []
    
    def order_by_lookup(self, by):
        return self.ORDER_BY.get(by, self.DESC)

    def parse_url_ids(self, ids: str):
        if ids:
            return [int(item) for item in ids.split(",") if item.isdigit()]
        return self.URL_IDS

    @staticmethod
    def capitalize(string: str):
        """Return `Capitalize` string for given param"""
        return string.lower().capitalize()

    def get_shop_by_id(self, branch_id: int):
        try:
            return Outlet.objects.get(id=branch_id)
        except Exception as e:
            self.log(message=str(e.args))
            raise CustomValidationError(debug=str(e.args))


class ViewController(ResponseController, generics.GenericAPIView, ViewMixin):

    def get_user_main_shop(self):
        """Return default outlet from current user"""
        user = self.request.user
        try:
            return Outlet.objects.get(user_id=user.id, parent__isnull=True, type=OutletType.MAIN)
        except Exception as e:
            raise CustomValidationError(debug=str(e.args))

    def validator_images(self, images_list=None):

        if images_list is None:
            images = self.request.data["images"]
        else:
            images = images_list
        try:
            if isinstance(images, list):
                for image in images:
                    UploadFile.objects.get(id=image)
            else:
                UploadFile.objects.get(id=images)
        except Exception as e:
            raise CustomValidationError(debug=str(e.args))

    def check_attributes(self, attributes):
        for attr in attributes:
            try:
                Attribute.objects.get(id=attr['name'])
                AttributeValue.objects.get(id=attr['value'])
            except Exception as e:
                self.log(message=str(e.args))
                return False

    def validate_attributes(self, attributes: list):
        for item in attributes:
            if self.check_attributes(attributes=item['attributes']) is False:
                return False

    def get_brand_by_name(self, name: str):
        try:
            obj, _ = Brand.objects.get_or_create(name=name)
            return obj
        except Exception as e:
            raise CustomValidationError(debug=str(e.args))

    def get_default_category(self):
        return Category.get_telephone(name="Telephones")

    def get_category_by_name(self):
        try:
            name = self.request.data["category"]
            return Category.objects.get(name=name)
        except Exception as e:
            self.log(message=str(e.args))
            raise CustomValidationError(debug=str(e.args))

    def get_default_unit(self):
        try:
            obj, _ = Measurement.objects.get_or_create(name="Dona")
            return obj
        except Exception as e:
            self.log(message=str(e.args))
            raise CustomValidationError(debug=str(e.args))


class CustomListView(ViewController, generics.ListAPIView, CustomPagination):
    """ Pagination List View """
    error_text = {"en": "", "ru": ""}

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if qs:
            result = self.paginated_queryset(qs, request)
            serializer = self.serializer_class(result, many=True)
            response = self.paginated_response(data=serializer.data)
            return Response(response)
        else:
            catch = qs.model.__name__ if qs else "Objects"
            self.update_error_text(catch=str(catch))
            self.code = POSResponse.CODE_4
            self.error_message = POSResponse.MSG_4
            return self.error_response()


class CustomCreateUpdateView(ViewController, generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    """ Create Retrieve Update API View """

    model = None

    def get_instance(self):
        """ return instance object by lookup_pk if exists `CustomValidationError` otherwise """
        try:
            return self.model.objects.get(id=self.kwargs['pk'])
        except Exception as e:
            raise CustomValidationError(debug=str(e.args))

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.model.objects.get(pk=self.kwargs["pk"])
            serializer = self.serializer_class(instance=instance)
            return self.success_response(results=serializer.data)
        except Exception as e:
            self.update_error_text(catch=self.kwargs)
            self.code = POSResponse.CODE_4
            self.error_message = POSResponse.MSG_4
            self.exception = e.args
            return self.error_response()

    def custom_update(self, data, partial: bool):
        instance = self.get_instance()
        try:
            serializer = self.serializer_class(instance=instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return self.success_response(results=serializer.data)
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()


class CustomModelViewSet(ViewController, generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    """ ViewSet Create Retrieve Update MIXIN """
    tags = []
    model = None

    def create(self, request, *args, **kwargs):
        """override this method"""
        try:
            if self.model.objects.filter(name__iexact=request.data["name"]).exists():
                self.update_error_text(catch=request.data)
                self.code = POSResponse.CODE_1
                self.error_message = POSResponse.MSG_1
                return self.error_response()
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.success_response(results=serializer.data)
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.model.objects.get(pk=self.kwargs["pk"])
            serializer = self.serializer_class(instance=instance)
            return self.success_response(results=serializer.data)
        except (AttributeError, TypeError, KeyError, Exception):
            qs = self.get_queryset()
            if qs.exists():
                serializer = self.serializer_class(qs, many=True)
                return self.success_response(results=serializer.data)
            else:
                self.update_error_text(catch=self.kwargs)
                self.code = POSResponse.CODE_4
                self.error_message = POSResponse.MSG_4
                return self.error_response()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data
        try:
            serializer = self.serializer_class(instance=self.get_object(), data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return self.success_response(results=serializer.data)
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()


class CustomGenericViewSet(ViewController, generics.RetrieveUpdateAPIView, GenericViewSet):
    """ Generic View Set """
    pass


class CustomGenericAPIView(ViewController):
    """ Generic Api View """
    pass


class CustomAPIView(ViewController):
    """ Generic Api View """
    pass


class CustomRetrieveView(ResponseController, generics.RetrieveAPIView):
    """ Retrieve API View """
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            serializer = self.get_serializer(obj)
            return self.success_response(result=serializer.data)
        except Exception as e:
            self.update_error_text(catch=self.kwargs["pk"])
            self.code = POSResponse.CODE_4
            self.error_message = POSResponse.MSG_4
            self.exception = e.args
            return self.error_response()


class CustomRetrieveUpdateDestroyView(ResponseController, generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve Update Destroy API View """
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'


class POSResponse:

    CODE_0 = 0
    MSG_0 = {
        # "uz": "OK",
        "en": "OK",
        "ru": "ОК"
    }

    CODE_1 = 1
    MSG_1 = {
        "en": "%s already exist",
        "ru": "%s уже существует"
    }

    CODE_2 = 2
    MSG_2 = {
        "en": "created successfully",
        "ru": "успешно создан"
    }

    CODE_3 = 3
    MSG_3 = {
        "en": "invalid data",
        "ru": "неверные данные",
    }

    CODE_4 = 4
    MSG_4 = {
        "en": "%s not found!",
        "ru": "%s не найден!",
    }

    CODE_5 = 5
    MSG_5 = {
        "en": "creation failed",
        "ru": "создание не удалось",
    }

    CODE_6 = 6
    MSG_6 = {
        "en": "%s invalid value(s)",
        "ru": "%s недопустимый формат значения"
    }

    CODE_7 = 7
    MSG_7 = {
        "en": "%s awaiting activation",
        "ru": "%s ожидает активации"
    }

    CODE_8 = 8
    MSG_8 = {
        "en": "%s activated successfully",
        "ru": "%s активирован успешно"
    }

    CODE_9 = 9
    MSG_9 = {
        "en": "%s already activated",
        "ru": "%s уже активирован"
    }

    CODE_10 = 10
    MSG_10 = {
        "en": "%s invalid activation code",
        "ru": "%s неверный код активации"
    }

    CODE_11 = 11
    MSG_11 = {
        "en": "time is over",
        "ru": "время вышло"
    }

    CODE_12 = 12
    MSG_12 = {
        "en": "updated successfully",
        "ru": "успешно обновлено"
    }

    CODE_13 = 13
    MSG_13 = {
        "en": "%s deleted",
        "ru": "%s удалено"
    }

    CODE_14 = 14
    MSG_14 = {
        "en": "Status not active",
        "ru": "Статус не активен"
    }

    CODE_15 = 15
    MSG_15 = {
        "en": "Invalid password",
        "ru": "Неверный пароль"
    }

    CODE_16 = 16
    MSG_16 = {
        "en": "%s are required",
        "ru": "%s требуются"
    }

    CODE_17 = 17
    MSG_17 = {
        "en": "Invalid attributes",
        "ru": "Недопустимые атрибуты"
    }

    CODE_18 = 18
    MSG_18 = {
        "en": "Invalid amount",
        "ru": "Недопустимая сумма"
    }

    CODE_19 = 19
    MSG_19 = {
        "en": "",
        "ru": ""
    }

    CODE_20 = 20
    MSG_20 = {
        "en": "%s is required",
        "ru": "%s обязательный"
    }

    CODE_21 = 21
    MSG_21 = {
        "en": "",
        "ru": ""
    }

    CODE_22 = 22
    MSG_22 = {
        "en": "",
        "ru": ""
    }

    CODE_23 = 23
    MSG_23 = {
        "en": "Time exception",
        "ru": "Исключение времени"
    }

    CODE_24 = 24
    MSG_24 = {
        "en": "",
        "ru": ""
    }

    CODE_25 = 25
    MSG_25 = {
        "en": "",
        "ru": ""
    }

    CODE_26 = 26
    MSG_26 = {
        "en": "",
        "ru": ""
    }

    CODE_27 = 27
    MSG_27 = {
        "en": "",
        "ru": ""
    }

    CODE_28 = 28
    MSG_28 = {
        "en": "",
        "ru": ""
    }

    CODE_29 = 29
    MSG_29 = {
        "en": "",
        "ru": ""
    }

    CODE_30 = 30
    MSG_30 = {
        "en": "something went wrong",
        "ru": "что-то пошло не так"
    }

    CODE_31 = 31
    MSG_31 = {
        "en": "server is not working",
        "ru": "сервер не работает"
    }

    CODE_32 = 32
    MSG_32 = {
        "en": "Order(s) not found.",
        "ru": "Заказ(ы) не найдено"
    }

    CODE_33 = 33
    MSG_33 = {
        "en": "bad request",
        "ru": "неудачный запрос"
    }

    CODE_34 = 34
    MSG_34 = {
        "en": "",
        "ru": ""
    }

    CODE_35 = 35
    MSG_35 = {
        "en": "",
        "ru": ""
    }

    CODE_36 = 36
    MSG_36 = {
        "uz": "",
        "de": "",
        "en": "",
        "ru": ""
    }
