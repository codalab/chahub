from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers import competitions as serializers
from api.views.mixins import BulkViewSetMixin
from competitions.models import Competition, Submission


# NOTE: We don't have delete mixin
class CompetitionViewSet(BulkViewSetMixin, ModelViewSet):
    """Updating and inserting competitions are done by Producers.

    request.user = Producer in this case."""
    queryset = Competition.objects.all()
    serializer_class = serializers.CompetitionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)

    extra_prefetch = ['phases', 'admins', 'participants']

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['producer'] = self.request.user
    #     return context
    #
    # def get_queryset(self):
    #     qs = Competition.objects.all()
    #     qs = qs.prefetch_related('phases', 'producer', 'admins', 'participants')
    #
    #     producer = self.request.query_params.get('producer', None)
    #     creator_id = self.request.query_params.get('creator_id', None)
    #
    #     if producer:
    #         qs = qs.filter(producer__id=producer)
    #     if creator_id:
    #         qs = qs.filter(creator_id=creator_id)
    #
    #     return qs
    #
    # def create(self, request, *args, **kwargs):
    #     """Overriding this for the following reasons:
    #
    #     1. Returning the huge amount of HTML/etc. back by default by DRF was bad
    #     2. We want to handle creating many competitions this way, and we do that
    #        custom to make drf-writable-nested able to interpret everything easily"""
    #     # Make the serializer take many competitions at once
    #     for competition in request.data:
    #         serializer = self.get_serializer(data=competition)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #     return Response({}, status=status.HTTP_201_CREATED)


#
#
# class PhaseViewSet(ModelViewSet):
#     queryset = Phase.objects.all()
#     serializer_class = serializers.PhaseSerializer
#
#

# NOTE: We don't have delete mixin
class SubmissionViewSet(BulkViewSetMixin, ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['producer'] = self.request.user
    #     return context
