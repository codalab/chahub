from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
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
    lookup_field_on_deletion = 'remote_id'
    lookup_url_kwarg = 'pk'

    def get_object(self):
        if self.request.method == "DELETE":
            return get_object_or_404(
                self.get_queryset(),
                producer=self.request.user,
                remote_id=self.kwargs[self.lookup_url_kwarg]
            )
        return super().get_object()

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'delete':
            self.lookup_field = self.lookup_field_on_deletion
        return super().dispatch(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            content = {}
        except ObjectDoesNotExist:
            content = {'detail': 'Could not find object to delete, deletion considered successful'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        blacklist_data = ['participant', 'email', 'username']
        for field in blacklist_data:
            if hasattr(instance, field):
                setattr(instance, field, None)
        instance.deleted = True
        if hasattr(instance, 'is_public'):
            instance.is_public = False
        elif hasattr(instance, 'published'):
            instance.published = False
        instance.save()

    def create(self, request, *args, **kwargs):
        """Overriding this so we return an empty response instead of the details of the created object"""
        for obj in request.data:
            serializer = self.get_serializer(data=obj)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)
