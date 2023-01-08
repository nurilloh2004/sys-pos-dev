from django.db import models
from apps.core.exception.custom_exception import CustomValidationError
import requests
import uuid
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from django.db.models import Q, F, Sum
import pytz
from django.utils.translation import gettext_lazy as _
from datetime import timedelta, datetime
from django.utils import timezone
from django.conf import settings
translate = _


class BitwiseNumber:
    BIT_1 = 1
    BIT_2 = 2
    BIT_3 = 4
    BIT_4 = 8
    BIT_5 = 16
    BIT_6 = 32
    BIT_7 = 64
    BIT_8 = 128
    BIT_9 = 256
    BIT_10 = 512
    BIT_11 = 1024
    BIT_12 = 2048
    BIT_13 = 4096
    BIT_14 = 8192
    BIT_15 = 16384
    BIT_16 = 32768
    BIT_17 = 65536


class LanguageType(models.TextChoices):
    UZ = "UZ", "uz"
    EN = "EN", "en"
    RU = "RU", "ru"


class Enum(models.IntegerChoices):
    pass


class BaseProductStatus(Enum):
    DRAFT = BitwiseNumber.BIT_1
    ACTIVE = BitwiseNumber.BIT_2
    CREDIT = BitwiseNumber.BIT_3
    DELETED = BitwiseNumber.BIT_4


class BaseStatus(Enum):
    INACTIVE = BitwiseNumber.BIT_1
    ACTIVE = BitwiseNumber.BIT_2
    DEFAULT = BitwiseNumber.BIT_3
    DELETED = BitwiseNumber.BIT_4


class CurrencyType(Enum):
    UZS = BitwiseNumber.BIT_1  # 1
    USD = BitwiseNumber.BIT_2  # 2


class LanguageStatus(Enum):
    UZ = BitwiseNumber.BIT_1
    EN = BitwiseNumber.BIT_2
    RU = BitwiseNumber.BIT_3


class ActivationType(Enum):
    REGISTER = BitwiseNumber.BIT_1
    RESEND = BitwiseNumber.BIT_2
    FORGOT = BitwiseNumber.BIT_3
    LOGIN = BitwiseNumber.BIT_4


class UserStatus(Enum):
    INACTIVE = BitwiseNumber.BIT_1
    ACTIVE = BitwiseNumber.BIT_2
    DELETED = BitwiseNumber.BIT_3


class AttributeStatus(Enum):
    INACTIVE = BitwiseNumber.BIT_1
    ACTIVE = BitwiseNumber.BIT_2
    DELETED = BitwiseNumber.BIT_3


class ProductStatus(Enum):
    INACTIVE = BitwiseNumber.BIT_1
    ACTIVE = BitwiseNumber.BIT_2
    DELETED = BitwiseNumber.BIT_3


class TransactionState(Enum):
    CREATED = BitwiseNumber.BIT_1
    PROGRESS = BitwiseNumber.BIT_2
    FAILED = BitwiseNumber.BIT_3
    COMPLETED = BitwiseNumber.BIT_4


class TransactionReason(Enum):
    BUYING = BitwiseNumber.BIT_1
    SELLING = BitwiseNumber.BIT_2
    CREDIT = BitwiseNumber.BIT_3
    DEBIT = BitwiseNumber.BIT_4


class TransactionMethod(Enum):
    CASH = BitwiseNumber.BIT_1
    CARD = BitwiseNumber.BIT_2


# class UserType(Enum):
#     STAFF = BitwiseNumber.BIT_1
#     CUSTOMER = BitwiseNumber.BIT_2
#     MERCHANT = BitwiseNumber.BIT_3
#     CLIENT = BitwiseNumber.BIT_4


class OutletCustomerType(Enum):
    PROVIDER = BitwiseNumber.BIT_1
    CLIENT = BitwiseNumber.BIT_2


class BillingAccountType(Enum):
    CASHBOX = BitwiseNumber.BIT_1
    OWNER = BitwiseNumber.BIT_2
    ADMIN = BitwiseNumber.BIT_3
    MANAGER = BitwiseNumber.BIT_4
    CUSTOMER = BitwiseNumber.BIT_5


class AddressType(Enum):
    DOOR = BitwiseNumber.BIT_1
    DROP = BitwiseNumber.BIT_2


class PaymentMethod(Enum):
    CASH = BitwiseNumber.BIT_1  # 1
    CARD = BitwiseNumber.BIT_2  # 2
    CASH_CARD = BitwiseNumber.BIT_3  # 4
    CREDIT = BitwiseNumber.BIT_4  # 8
    TERMINAL = BitwiseNumber.BIT_5  # 16
    VIP_PAYMENT = BitwiseNumber.BIT_6  # 32


class DistrictStatus(Enum):
    INACTIVE = BitwiseNumber.BIT_1  # 1
    ACTIVE = BitwiseNumber.BIT_2  # 2
    DEFAULT = BitwiseNumber.BIT_3  # 4
    CENTER = BitwiseNumber.BIT_4  # 8


class OutletStatus(Enum):
    ACTIVE = BitwiseNumber.BIT_1  # 1
    INACTIVE = BitwiseNumber.BIT_2  # 4
    DELETED = BitwiseNumber.BIT_3  # 8


class OutletType(Enum):
    MAIN = BitwiseNumber.BIT_1  # 1
    BRANCH = BitwiseNumber.BIT_2  # 2


class OutletMemberType(Enum):
    MEMBER = BitwiseNumber.BIT_1  # 1
    OWNER = BitwiseNumber.BIT_2  # 2


class InvoiceStatus(Enum):
    DRAFT = BitwiseNumber.BIT_1  # 1
    UNPAID = BitwiseNumber.BIT_2  # 2
    PAID = BitwiseNumber.BIT_3  # 4
    REFUND = BitwiseNumber.BIT_4  # 8


class InvoiceCheckStatus(Enum):
    DRAFT = BitwiseNumber.BIT_1  # 1
    UNPAID = BitwiseNumber.BIT_2  # 2
    PROGRESS = BitwiseNumber.BIT_3  # 4
    COMPLETED = BitwiseNumber.BIT_4  # 8


class InOutType(Enum):
    BUYING = BitwiseNumber.BIT_1
    SELLING = BitwiseNumber.BIT_2
    REFUND = BitwiseNumber.BIT_3  # 4  возвращенный


class InvoiceReceiptType(Enum):
    CASH = BitwiseNumber.BIT_1  # 1
    CARD = BitwiseNumber.BIT_2  # 2
    CREDIT = BitwiseNumber.BIT_3  # 4
    CASH_CARD = BitwiseNumber.BIT_4  # 8



