from apps.core.services.status import *
from apps.core.services.generators import generate_model_slug
from .models import Category, UserRole, SelectedPermission


def pre_save_parent_category(sender, instance, **kwargs):
    instance.path = instance.name
    parent_category_obj = instance.parent
    while parent_category_obj is not None:
        instance.path = parent_category_obj.name + " > " + instance.path
        parent_category_obj = parent_category_obj.parent

    if not instance.slug:
        instance.slug = generate_model_slug(instance.name, Category)
pre_save.connect(pre_save_parent_category, sender=Category)


def post_saved(sender, instance: UserRole, created, *args, **kwargs):
    if not created and instance.permission_ids and instance.user and instance.group:
        perms = []

        for permission_id in instance.permission_ids.split(","):
            item = SelectedPermission.objects.get(id=permission_id)
            perms.append(item.permission.id)

            if instance.user.groups:
                instance.user.groups.permissions.clear()

            for perm in perms:
                instance.user.groups.permissions.add(perm)

post_save.connect(post_saved, sender=UserRole)
