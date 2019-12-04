from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.pagination import BasicPagination
from api.permissions import ProducerPermission
from api.serializers import data as serializers
from api.views.chahub import ChaHubModelViewSet
from datasets.models import Data, DataGroup


class DataViewSet(ChaHubModelViewSet):
    queryset = Data.objects.all()
    serializer_class = serializers.DataSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
    pagination_class = BasicPagination

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.method == 'GET':
            qs = qs.select_related('producer')
        return qs


class DataGroupViewSet(ModelViewSet):
    queryset = DataGroup.objects.all()
    serializer_class = serializers.DataGroupSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = BasicPagination
