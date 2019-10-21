from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.authenticators import ProducerAuthentication
from api.pagination import BasicPagination
from api.permissions import ProducerPermission
from api.serializers import data as serializers
from datasets.models import Data, DataGroup


# class DataViewSetCreate(CreateAPIView, GenericViewSet):
#     queryset = Data.objects.all()
#     serializer_class = serializers.DataSerializer
#     parser_classes = (MultiPartParser,)
#
#     # def put(self, request, filename, format=None):
#     #     file_obj = request.data['file']
#     #     # ...
#     #     # do some stuff with uploaded file
#     #     # ...
#     #     return Response(status=204)
#     def perform_create(self, serializer):
#         serializer.save(
#             owner=self.request.user,
#             data_file=self.request.data.get('data_file')
#         )


class DataViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Data.objects.all()
    serializer_class = serializers.DataSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
    pagination_class = BasicPagination

    def create(self, request, *args, **kwargs):
        """Overriding this so we return an empty response instead of the details of the created object"""
        for dataset in request.data:
            serializer = self.get_serializer(data=dataset)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)

    # def get_serializer(self, *args, **kwargs):
    #     if self.request.method == 'POST':
    #         return serializers.DataSerializer
    #     else:
    #         return serializers.DataSerializer

    # def put(self, *args, **kwargs):
    #     return self.put()
    # def post(self, request, *args, **kwargs):
    #     # MultiPartParser
    #     pass
    # def perform_create(self, serializer):
    #     serializer.save(
    #         owner=self.request.user,
    #         data_file=self.request.data.get('data_file')
    #     )


class DataGroupViewSet(ModelViewSet):
    queryset = DataGroup.objects.all()
    serializer_class = serializers.DataGroupSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = BasicPagination
