from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers import data as serializers
from api.views.mixins import BulkViewSetMixin
from datasets.models import Data

# class DataGroupViewSet(ModelViewSet):
#     queryset = DataGroup.objects.all()
#     serializer_class = serializers.DataGroupSerializer
#     permission_classes = (IsAuthenticated,)


# NOTE: We don't have delete mixin
class DataViewSet(BulkViewSetMixin, ModelViewSet):
    """Updating and inserting competitions are done by Producers.

    request.user = Producer in this case."""
    queryset = Data.objects.all()
    serializer_class = serializers.DataSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
