from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.pagination import BasicPagination
from api.permissions import ProducerPermission


class ChaHubModelViewSet(ModelViewSet):
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
    pagination_class = BasicPagination
    # Set this to the field to want to be looking up on deletion, in our case
    # we want to lookup based on remote_id (producer comes from permission checks implicitly)
    lookup_field_on_deletion = None
    lookup_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'delete':
            self.lookup_field = self.lookup_field_on_deletion
        return super().dispatch(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        blacklist_data = ['participant', 'email', 'username']
        for field in blacklist_data:
            if hasattr(instance, field):
                setattr(instance, field, None)
        instance.deleted = True
        instance.save()
