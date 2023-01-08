import secrets
import binascii
import os
from django.template.defaultfilters import slugify


def random_activation_sms_code():
    random_number = '123456789'
    generated = ''.join(secrets.choice(random_number) for i in range(6))
    return generated


def generate_otp_auth_key():
    return binascii.hexlify(os.urandom(20)).decode()


def generate_model_slug(field: str, model):
    i = 1
    slug = slugify(field).lower()
    while model.objects.filter(slug=slug).exists():
        slug += str(i)
        i += 1
    return slug


def product_id_generator():
    prefix = 'A'
    random_number = '123456789'
    order_id = ''.join(secrets.choice(random_number) for i in range(5))
    return f"{prefix}-{order_id}"


def invoice_id_generator(instance) -> str:
    # PX6277473
    random_number = '123456789'
    seller_id = instance.seller_id  # Seller BillingAccount ID
    instance_ids = f'{instance.id}{seller_id}'  # {1} {5}
    random_no = ''.join(secrets.choice(random_number) for i in range(5))
    return f'PX{instance_ids}{random_no}'


def receipt_no_generator(instance) -> str:
    # 61468333
    random_number = '123456789'
    invoice_id = instance.invoice_id  # Invoice ID
    random_no = ''.join(secrets.choice(random_number) for i in range(7))
    return f'{invoice_id}{random_no}'

