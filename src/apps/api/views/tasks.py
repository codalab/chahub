from rest_framework import status
from rest_framework.response import Response

from api.authenticators import ProducerAuthentication
from api.pagination import BasicPagination
from api.permissions import ProducerPermission
from api.serializers import tasks as serializers
from api.views.chahub import ChaHubModelViewSet
from tasks.models import Task, Solution


class TaskViewSet(ChaHubModelViewSet):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
    pagination_class = BasicPagination
    lookup_field_on_deletion = 'remote_id'

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


class SolutionViewSet(ChaHubModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = serializers.SolutionCreationSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
    pagination_class = BasicPagination
    lookup_field_on_deletion = 'remote_id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['producer'] = self.request.user
        return context

    def create(self, request, *args, **kwargs):
        for solution in request.data:
            serializer = self.get_serializer(data=solution)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)
