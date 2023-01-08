from apps.core.services.status import UserStatus
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_superuser=False, **kwargs):
        if is_superuser:
            user = self.model(phone=phone)
        else:
            user = self.model(phone=phone)
        if not phone:
            raise ValueError('Users must have a phone number')
        if password is not None:
            user.set_password(password)
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_staffuser(self, phone, password):
        if not password:
            raise ValueError('staff/admins must have a password.')
        user = self.create_user(phone=phone, password=password)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, phone, password):
        if not password:
            raise ValueError('superusers must have a password.')
        user = self.create_user(phone=phone, password=password, is_superuser=True)
        user.is_active = True
        user.status = UserStatus.ACTIVE
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

