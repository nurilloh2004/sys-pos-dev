from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS', 'PUT')


class BlockedDevicePermission(BasePermission):
    """
    Global permission check for blocked IPs.
    BlockedDevice
    """

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        # blocked = BlockedDevice.objects.filter(ip_addr=ip_addr).exists()
        blocked = False
        return not blocked


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # If the outlet belongs to the current user he can make changes
        if obj.author == request.user:
            return True
        return False


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return False


class HasCreateOutletPermission(BasePermission):

    message = F'Adding more than 1 BRANCH not allowed for free trial.'

    def has_permission(self, request, view):
        user = request.user
        count = user.owner_market_count()
        if user.is_authenticated:
            if request.method == 'POST' and count > 3:
                return False
            return True


class HasCreateMemberPermission(BasePermission):
    allowed_count = 1
    message = f'Adding more than {allowed_count} MEMBER not allowed for free trial.'

    def has_permission(self, request, view):
        user = request.user
        count = user.owner_member_count()

        if user.is_authenticated:
            if request.method == 'POST' and count > 5:
                return False
            return True


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class CustomerAccessPermission(BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True


class IsFinancesMember(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Finances").exists():
            return True


class AuthorAllStaffAllButEditOrReadOnly(BasePermission):
    # permission_classes = [~IsFinancesMember]  # using not operator
    # permission_classes = [(IsStaff, IsOwner)]  # or operator used
    # permission_classes = (IsStaff & IsOwner & IsFinancesMember)
    # permission_classes = [(IsFinancesMember | IsStaff) & IsOwner]  # using parentheses

    message = 'You must be the owner of this object.'

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):

        """GET, POST, PUT, DELETE"""

        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):

        """ GET, PUT, DELETE """

        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False

