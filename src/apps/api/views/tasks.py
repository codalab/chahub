from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers import tasks as serializers
from api.views.mixins import BulkViewSetMixin
from tasks.models import Task, Solution


# NOTE: We don't have delete mixin
class TaskViewSet(BulkViewSetMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)


class SolutionViewSet(BulkViewSetMixin, ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = serializers.SolutionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
