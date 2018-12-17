from rest_framework import permissions

from producers.models import Producer


class ProducerPermission(permissions.BasePermission):
    message = 'Only producers may modify ChaHub information.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # The ProducerAuthentication class sets request.user to Producer,
            # TODO: Check object permissions, should only be able to work on non existant objects or objects where producer == producer!!!

            # TODO, MAYBE: When a user.is_superuser calls this view maybe allow them to specify a producer ID to set as request.user here ????
            # This request.user hack is gross anyway. "Producer -> request.user" is extremely unintuitive. User should mean user, not producer

            return isinstance(request.user, Producer)
