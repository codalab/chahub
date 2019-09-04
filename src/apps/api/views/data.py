from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.pagination import BasicPagination
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
