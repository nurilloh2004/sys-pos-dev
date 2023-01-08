from apps.core.services.status import *
from apps.core.services.generics import POSResponse, CustomGenericAPIView, CustomAPIView, CustomCreateUpdateView
from .models import User, ActivationSMSCode, Group
from rest_framework.permissions import IsAuthenticated
from apps.dashboard.models import UserRole, SelectedPermission
from . import serializers as ser
from .utils.services import AccountController
from apps.outlets.models import OutletMember


class RoleViewSet(CustomCreateUpdateView):
    """POST, GET, PUT: {{BASE}}api/v1/accounts/role/{id}/ """
    serializer_class = ser.RoleSerializer
    permission_classes = [IsAuthenticated]
    model = UserRole
    tags = ["User role API"]

    def create(self, request, *args, **kwargs):
        name: str = request.data["name"].capitalize()
        user: User = request.user

        if UserRole.objects.filter(name__iexact=name, creator_id=user.id).exists():
            raise CustomValidationError(debug=self.OBJECT_ALREADY_EXISTS % name)

        try:
            permissions: list = request.data["permissions"]
            permission_ids = ""
            if permissions:
                permission_ids = ', '.join(map(str, request.data["permissions"]))
            role = UserRole.objects.create(name=name, creator_id=user.id, permission_ids=permission_ids)

            serializer = self.serializer_class(instance=role)
            return self.success_response(results=serializer.data)
        except Exception as e:
            raise CustomValidationError(debug=str(e.args))

    def update(self, request, *args, **kwargs):
        data = request.data
        try:
            role = UserRole.objects.get(id=self.kwargs['pk'])
            if data.get("name", None):
                role.name = data["name"].capitalize()

            if data.get('permissions', None):
                permission_ids = ', '.join(map(str, request.data["permissions"]))
                role.permission_ids = permission_ids
            role.save()
            serializer = self.serializer_class(instance=role)
            return self.success_response(results=serializer.data)
        except Exception as e:
            raise CustomValidationError(debug=str(e.args))


class OwnerRolesList(CustomGenericAPIView):
    """ GET: {{BASE}}api/v1/accounts/user/permissions/ """
    serializer_class = ser.RoleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = UserRole.objects.filter(creator_id=user.id)
        serializer = self.serializer_class(qs, many=True)
        return self.success_response(results=serializer.data)


class SendOtpAPIView(CustomGenericAPIView, AccountController):
    """ POST: http://127.0.0.1:8585/api/v1/auth/send-otp/ """
    serializer_class = ser.ActivationCodeSerializer

    def post(self, request, *args, **kwargs):
        self.validator_phone()
        phone = request.data['phone']

        if User.objects.filter(phone=phone).exists():
            if request.data['register']:
                raise CustomValidationError(debug=self.OBJECT_ALREADY_EXISTS % phone)
            else:
                data = self.get_activation_data()
                return self.success_response(results=data)
        else:
            if request.data['register']:
                data = self.get_activation_data()
                return self.success_response(results=data)
            else:
                self.update_error_text(catch=phone)
                self.code = POSResponse.CODE_4
                self.error_message = POSResponse.MSG_4  
                return self.error_response()


class VerifyOtpAPIView(CustomGenericAPIView, AccountController):
    """
    POST: {{BASE}}api/v1/auth/verify-otp/
    """
    serializer_class = ser.ActivationCodeSerializer

    def post(self, request, *args, **kwargs):
        self.validator_phone()
        try:
            data = request.data
            qs = ActivationSMSCode.objects.filter(phone=data['phone'], code=data['code'], is_activated=False)
            if qs.exists():
                obj = qs.latest('created_at')
                if not self.code_is_expire(obj=obj):
                    obj.activate()
                    return self.success_response(results={"phone": obj.phone, "token": obj.token})
                else:
                    self.code = POSResponse.CODE_11
                    self.error_message = POSResponse.MSG_11
                    return self.error_response()    
            else:
                self.update_error_text(catch=data['code'])
                self.code = POSResponse.CODE_10
                self.error_message = POSResponse.MSG_10
                return self.error_response()

        except Exception as e:
            self.code = POSResponse.CODE_3  
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()


class ResetPasswordAPIView(CustomGenericAPIView):

    serializer_class = ser.ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            qs = ActivationSMSCode.objects.filter(token=data["token"])
            if qs.exists():
                user = User.objects.get(phone=data["phone"])
                user.set_password(data["password"])
                user.save()
                return self.success_response()
            else:
                self.update_error_text(catch="TOKEN ")
                self.code = POSResponse.CODE_4
                self.error_message = POSResponse.MSG_4
                return self.error_response()
        except Exception as e:
            self.code = POSResponse.CODE_3
            self.error_message = POSResponse.MSG_3
            self.exception = e.args
            return self.error_response()


class CreateOwnerAPIView(CustomGenericAPIView, AccountController):
    """
    POST: {{BASE}}api/v1/accounts/create-owner/
    Create new owner API
    """
    tags = ["Create new owner API"]

    serializer_class = ser.UserCreateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        self.validator_phone()
        qs = ActivationSMSCode.objects.filter(token=data["token"], phone=data["phone"])
        if qs.exists():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user = serializer.instance
            self.set_owner_role(user=user)
            user.activated_date = timezone.now()
            user.set_password(data["password"])
            user.save()

            qs.update(user=user)

            self.create_main_outlet(user=user)

            instance = ser.UserShortSerializer(instance=user)
            return self.success_response(results=instance.data)
        else:
            raise CustomValidationError()


class CreateMemberAPIView(CustomGenericAPIView, AccountController):
    """
     POST: {{BASE}}api/v1/accounts/create-member/
     Create outlet member API
    """
    serializer_class = ser.UserCreateSerializer
    permission_classes = [IsAuthenticated, ]  #HasCreateMemberPermission]
    tags = ["Create outlet member API"]

    def post(self, request):
        data = request.data
        self.validator_phone()
        qs = User.objects.filter(phone=data["phone"])
        if qs.exists():
            raise CustomValidationError(debug=self.OBJECT_ALREADY_EXISTS % data["phone"])
        else:
            if "branch" in data and data["branch"]:
                outlet = self.get_shop_by_id(branch_id=data["branch"])
            else:
                outlet = self.get_user_main_shop()

            is_images = False
            if "images" in data and data["images"]:
                self.validator_images()
                is_images = True

            data["password"] = self.make_default_password()
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = serializer.instance

            outlet.create_outlet_member(user_id=user.id)

            if is_images:
                user.add_profile_images(images=data["images"])

            if outlet.type == OutletType.BRANCH:
                outlet.user_id = user.id
                outlet.save()

            return self.success_response(results=ser.UserDetailSerializer(instance=user).data)


class CreateCustomerUserAPIView(CustomGenericAPIView, AccountController):
    """
     POST: {{BASE}}api/v1/accounts/create-customer/
     Create Credit user API
     {
        "phone": "+998901232222",
        "first_name": "Qarzdor",
        "last_name": "Otarman",
        "customer_type": 1
    }
    """
    serializer_class = ser.UserCreateSerializer
    permission_classes = [IsAuthenticated]
    tags = ["Create provider/customer API"]

    def post(self, request):
        data = request.data
        self.validator_phone()

        phone = data["phone"]

        if User.objects.filter(phone=phone).exists():
            raise CustomValidationError(debug=self.OBJECT_ALREADY_EXISTS % phone)

        outlet = self.get_user_main_shop()

        customer_type = data.get("customer_type", 0)

        if customer_type not in [OutletCustomerType.CLIENT, OutletCustomerType.PROVIDER]:
            raise CustomValidationError(debug="Invalid customer_type")

        data["password"] = self.make_default_password()
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.instance
        new_customer = outlet.create_outlet_customer(user_id=user.id, customer_type=customer_type)
        results = ser.UserDetailSerializer(instance=user).data
        results["type_display"] = new_customer.get_type_display()

        return self.success_response(results=results)


class LoginAPIView(CustomGenericAPIView, AccountController):
    """
    POST: {{BASE}}api/v1/auth/login/
    """
    serializer_class = ser.LoginSerializer
    tags = ["Login API"]

    def post(self, request, *args, **kwargs):
        data = request.data
        self.validator_phone()
        qs = User.objects.filter(phone=data["phone"])
        if qs.exists():
            user = qs.last()

            if not user.check_password(raw_password=data["password"]):
                self.code = POSResponse.CODE_15
                self.error_message = POSResponse.MSG_15
                return self.error_response()

            if user.status != UserStatus.ACTIVE:
                self.code = POSResponse.CODE_14
                self.error_message = POSResponse.MSG_14
                return self.error_response()

            data = self.authentication(user=user)
            return self.success_response(results=data)
        else:
            raise CustomValidationError(debug=self.OBJECT_NOT_FOUND % data["phone"])


class UserViewSet(CustomGenericAPIView):
    queryset = User.objects.all()
    serializer_class = ser.UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return self.success_response(results=serializer.data)


class MemberDeleteViewView(CustomAPIView):
    """
     POST: {{BASE}}api/v1/accounts/delete-member/{id}/
     Delete member API
    """
    permission_classes = [IsAuthenticated]
    queryset = OutletMember.objects.all()
    tags = ["Delete member API"]

    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk, status__in=[UserStatus.ACTIVE, UserStatus.INACTIVE])
            user.status = UserStatus.DELETED
            user.save()
            qs = self.queryset.filter(user_id=user.id)
            if qs.exists():
                qs.update(status=BaseStatus.DELETED)
            return self.success_response()
        except Exception as e:
            raise CustomValidationError(debug=str(e.args))

