from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.authenticators import ProducerAuthentication
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


# class DataViewSet(ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, GenericViewSet):
#     queryset = Data.objects.all()
#     serializer_class = serializers.DataSerializer
#     parser_classes = (MultiPartParser,)
#     permission_classes = (IsAuthenticated,)

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


# class DataGroupViewSet(ModelViewSet):
#     queryset = DataGroup.objects.all()
#     serializer_class = serializers.DataGroupSerializer
#     permission_classes = (IsAuthenticated,)

# NOTE: We don't have delete mixin
class DataViewSet(ModelViewSet):
    """Updating and inserting competitions are done by Producers.

    request.user = Producer in this case."""
    queryset = Data.objects.all()
    serializer_class = serializers.DataSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['producer'] = self.request.user
        return context

    def get_queryset(self):
        qs = self.queryset
        qs = qs.prefetch_related('user', 'producer')

        producer = self.request.query_params.get('producer', None)
        creator_id = self.request.query_params.get('creator_id', None)

        if producer:
            qs = qs.filter(producer__id=producer)
        if creator_id:
            qs = qs.filter(creator_id=creator_id)

        return qs

    def create(self, request, *args, **kwargs):
        """Overriding this for the following reasons:

        1. Returning the huge amount of HTML/etc. back by default by DRF was bad
        2. We want to handle creating many competitions this way, and we do that
           custom to make drf-writable-nested able to interpret everything easily"""
        # Make the serializer take many competitions at once
        for data in request.data:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)
