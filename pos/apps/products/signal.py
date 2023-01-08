from apps.core.services.status import *
from apps.core.services.generators import product_id_generator
from .models import OutletProduct


# @receiver(post_save, sender=OutletProduct)
# def post_save_outlet_product(sender, instance: OutletProduct, created, **kwargs):
#     if created:
#         instance.original_price = instance.product.original_price
#         instance.selling_price = instance.product.selling_price
#         instance.minimal_price = instance.product.minimal_price
#         instance.save()


@receiver(post_save, sender=OutletProduct)
def create_product(sender, instance: OutletProduct, created, **kwargs):
    if created:
        if instance.px_code is None or instance.px_code == "":
            instance.px_code = product_id_generator()
        instance.save()


@receiver(m2m_changed, sender=OutletProduct.attributes.through)
def product_variation_change(sender, instance: OutletProduct, action, **kwargs):
    # if action == 'pre_add':
    #     pass

    if action == 'post_add':
        product_attr = ", ".join(attr.value for attr in instance.attributes.all())
        instance.title = f"{instance.product.title}, {product_attr}"
        instance.save()

    # if action == 'pre_remove':
    #     pass
    #
    # if action == 'post_remove':
    #     pass
    #
    # if action == 'pre_clear':
    #     pass
    #
    # if action == 'post_clear':
    #     pass

