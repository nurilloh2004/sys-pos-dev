from apps.core.services.status import *
from apps.core.services.generics import CustomCreateUpdateView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.utils.services import User, AccountController, Group
from apps.accounts.serializers import UserDetailSerializer
from apps.dashboard.models import UserRole


class ProfileViewSet(CustomCreateUpdateView, AccountController):
    """ GET or UPDATE method """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get(self, request, *args, **kwargs):
        user = request.user
        if "pk" in kwargs:
            user = User.objects.get(id=kwargs['pk'])
        serializer = self.serializer_class(user)
        return self.success_response(results=serializer.data)

    def update(self, request, *args, **kwargs):
        instance: User = self.get_instance()  # User
        data = request.data

        is_images = False
        if data.get("images", None):
            self.validator_images()
            is_images = True

        if data.get("role", None):
            try:
                role = UserRole.objects.get(id=data["role"])
                if instance.groups:
                    group = instance.groups
                else:
                    group = Group.objects.create(name=str(instance.phone))
                instance.groups_id = group.id
                instance.save()

                role.group_id = group.id
                role.user_id = instance.id
                role.save()
            except Exception as e:
                raise CustomValidationError(debug=str(e.args))

        payload = {
            "username": data.get('username', instance.username),
            "first_name": data.get('first_name', instance.first_name),
            "last_name": data.get('last_name', instance.last_name),
            "fullname": data.get('fullname', instance.fullname),
            "email": data.get('email', instance.email),
            "status": data.get('status', instance.status)
        }
        instance.user_update(**payload)

        if is_images:
            instance.add_profile_images(images=data["images"])

        serializer = self.serializer_class(instance=self.get_instance())
        return self.success_response(results=serializer.data)
