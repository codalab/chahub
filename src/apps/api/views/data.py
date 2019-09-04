from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers import data as serializers
from api.views.mixins import ProducerModelViewSet
from datasets.models import Data


class DataViewSet(ProducerModelViewSet):
    """Updating and inserting competitions are done by Producers.

    request.user = Producer in this case."""
    queryset = Data.objects.all()
    serializer_class = serializers.DataSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
