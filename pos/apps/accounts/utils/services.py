from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User, ActivationSMSCode, Group
from apps.outlets.models import Currency, Outlet
from apps.core.services.status import *
from apps.dashboard.models import UserRole, SelectedPermission
from django.contrib.auth.hashers import make_password
from apps.core.services.controller import Controller


class AccountController(Controller):

    default_password = "123456i"
    owner_role_name = "Owner"

    def validator_phone(self):
        """Return True if phone number starts at +998 and length is 13, ValidationError otherwise."""
        phone: str = self.request.data.get("phone", "+000")
        if not phone.startswith("+998") or len(phone) != 13:
            raise CustomValidationError(debug=phone)

    def set_owner_role(self, user: User):
        """ Set owner role """
        group = Group.objects.create(name=str(user.phone))

        user.groups_id = group.id
        user.save()

        qs = SelectedPermission.objects.all()
        if qs.exists():
            permission_ids = ""
            for sp_id in qs:
                permission_ids += f"{sp_id.id},"
                user.groups.permissions.add(sp_id.permission.id)
            UserRole.objects.create(
                name=self.owner_role_name,
                group_id=group.id,
                creator_id=user.id,
                user_id=user.id,
                permission_ids=permission_ids[:-1]
            )

    @staticmethod
    def get_activation(user_id: int, phone: str, sms_type):
        code = ActivationSMSCode.objects.create(user_id=user_id, phone=phone, sms_type=sms_type)
        return code

    @staticmethod
    def code_is_expire(obj: ActivationSMSCode):
        if timezone.now() > obj.expires_in:
            return True
        return False

    def get_activation_data(self):
        phone = self.request.data["phone"]
        px_robot: User = User.px_bot_user()

        qs = ActivationSMSCode.objects.filter(phone=phone, is_activated=False)
        data = {"phone": phone}
        if qs.exists():
            obj = qs.latest('created_at')
            if self.code_is_expire(obj=obj):
                obj.delete()
                obj = self.get_activation(user_id=px_robot.id, phone=phone, sms_type=ActivationType.RESEND)
            data["code"] = obj.code
            data["expires_in"] = obj.expires_in
        else:
            obj = self.get_activation(user_id=px_robot.id, phone=phone, sms_type=ActivationType.REGISTER)
            data["code"] = obj.code
            data["expires_in"] = obj.expires_in
        self.reporter(message=f"{phone}\ncode: {obj.code}")
        return data

    def authentication(self, user: User) -> dict:
        token = RefreshToken.for_user(user)
        return {self.lookup_access_key: str(token.access_token), self.lookup_refresh_key: str(token)}

    def create_main_outlet(self, user: User):
        qs = Outlet.objects.filter(user_id=user.id, type=OutletType.MAIN)
        if qs.exists():
            shop = qs.last()
        else:
            currency = Currency.get_currency_uzs()
            shop = Outlet.objects.create(
                owner_id=user.id,
                user_id=user.id,
                name=self.default_shop_name,
                legal_name=self.default_shop_legal_name,
                phone=str(user.phone),
                currency_id=currency.id,
                type=OutletType.MAIN
            )
            self.create_working_day(shop=shop)
        shop.get_address()

    def make_default_password(self):
        """ Turn a plain-text default_password (123456i) into a hash for database storage """
        return make_password(self.default_password)



