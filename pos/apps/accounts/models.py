from django.contrib.auth.models import (
    AbstractBaseUser,
    Group,
    PermissionsMixin,
)
from apps.core.services.status import *
from apps.core.services.generators import generate_otp_auth_key
from .manager import UserManager
from apps.core.models import TimestampedModel
from apps.dashboard.models import UserRole


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    username = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    legal_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(verbose_name='email address', blank=True, max_length=255, null=True)
    phone = models.CharField(max_length=50, db_index=True, unique=True)
    activated_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=UserStatus.choices, default=UserStatus.ACTIVE)
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, verbose_name=translate('group'))
    language = models.CharField(max_length=10, choices=LanguageType.choices, default=LanguageType.UZ)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.phone} / id: {self.id}"

    class Meta:
        verbose_name_plural = "    Users"
        ordering = ['-id']

    def add_profile_images(self, images: list):
        for image_id in images:
            if not self.profile_image.filter(instance_id=self.id, image_id=image_id).exists():
                self.profile_image.create(instance_id=self.id, image_id=image_id)

    @property
    def images(self):
        qs = self.profile_image.filter(instance_id=self.id)
        data = []
        if qs.exists():
            instance = qs.latest('created_at')
            data.append({"id": instance.id, "url": instance.image.url})
        return data

    @property
    def get_full_name(self):
        full_name = ""
        if self.first_name:
            full_name += self.first_name
        if self.last_name:
            full_name += f" {self.last_name}"
        if not full_name:
            full_name += f" {self.username}"
        return full_name

    @property
    def name(self):
        full_name = ""
        if self.first_name:
            full_name += self.first_name
        if self.last_name:
            full_name += f" {self.last_name}"
        if not full_name:
            full_name += f" {self.username}"
        return full_name

    def get_short_name(self):
        return f"{self.username}"

    def get_model_permissions(self):
        role = None
        if self.groups:
            if self.groups:
                role = {"id": self.groups.id, "name": self.groups.name, "permissions": []}
                for permission in self.groups.permissions.all():
                    role["permissions"].append({"id": permission.id, "name": permission.name})
        return role

    def user_update(self, **kwargs):
        if self.id:
            User.objects.filter(id=self.id).update(**kwargs)

    @classmethod
    def private_buyer_bln(cls):
        """ Private billing BUYER """
        bot = User.px_bot_user()
        return bot.billing_account.get(user_id=bot.id)

    def get_billing_user(self, user_id):
        """ Get billing by user ID """
        return self.billing_account.get(user_id=user_id)

    @classmethod
    def px_bot_user(cls):
        """ PX BOT user """
        qs = cls.objects.filter(phone=settings.PX_ROBOT_PHONE)
        if qs.exists():
            buyer = qs.last()
        else:
            buyer = cls.objects.create(
                username="Robot",
                first_name="Posox",
                last_name="Bot",
                fullname="Posox Bot",
                email="robot@bot.com",
                phone=settings.PX_ROBOT_PHONE,
                activated_date=timezone.now(),
                status=UserStatus.ACTIVE
            )
        return buyer

    def owner_market_count(self):
        qs = self.outlet_owner.filter(status=OutletStatus.ACTIVE)
        return qs.count() + 1  # Problem n+1

    def owner_member_count(self):
        model = self.member.model
        qs = model.objects.filter(status=BaseStatus.ACTIVE).exclude(user_id=self.id)
        return qs.count() + 1  # Problem n+1

    @property
    def roles(self):
        result = None
        if self.user_role:
            result = {"id": self.user_role.id, "name": self.user_role.name, "permissions": self.user_role.permissions}
        return result


class ActivationSMSCode(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sms')
    phone = models.CharField(max_length=120)
    code = models.CharField(max_length=10, blank=True, help_text="This field is created automatically")
    sms_type = models.IntegerField(choices=ActivationType.choices, default=ActivationType.REGISTER)
    text = models.TextField(blank=True)  # sms text
    token = models.TextField(null=True, blank=True)
    is_activated = models.BooleanField(default=False)
    expires_in = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.phone

    class Meta:
        verbose_name_plural = "   ActivationSMSCodes"
        ordering = ['-id']

    # def send_sms(self):
    #     """Main function for sending SMS"""
    #     phone_is_numeric = self.phone[1:].isnumeric()  # 998901234567
    #     if phone_is_numeric and self.phone not in settings.BLACKLISTED_USERS:
    #         api = SendSMSApi(is_sms_enabled=self.is_sms_on())
    #         api.send_user_sms(msg=self.text, phone=self.phone)

    def activate(self):
        user = self.user

        self.token = generate_otp_auth_key()
        self.is_activated = True
        self.save()

        user.activated_date = timezone.now()
        user.save()

        return self
