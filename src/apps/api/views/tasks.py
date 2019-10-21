from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.authenticators import ProducerAuthentication
from api.pagination import BasicPagination
from api.permissions import ProducerPermission
from api.serializers import tasks as serializers
from tasks.models import Task


class TaskViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
    pagination_class = BasicPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.TaskCreationSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        for task in request.data:
            serializer = self.get_serializer(data=task)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)
