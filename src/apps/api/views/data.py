from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.pagination import BasicPagination
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


class DataViewSet(ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, GenericViewSet):
    queryset = Data.objects.all()
    serializer_class = serializers.DataSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)
    pagination_class = BasicPagination

    def create(self, request, *args, **kwargs):
        """Overriding this so we return an empty response instead of the details of the created object"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({}, status=status.HTTP_201_CREATED, headers=headers)

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
