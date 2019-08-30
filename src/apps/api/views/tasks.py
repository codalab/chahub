from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers import tasks as serializers
from api.views.mixins import ProducerModelViewSet
from tasks.models import Task, Solution


class TaskViewSet(ProducerModelViewSet):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)


class SolutionViewSet(ProducerModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = serializers.SolutionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
