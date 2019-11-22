from rest_framework import status
from rest_framework.response import Response

from api.authenticators import ProducerAuthentication
from api.pagination import BasicPagination
from api.permissions import ProducerPermission
from api.serializers import competitions as serializers
from api.views.chahub import ChaHubModelViewSet
from competitions.models import Competition, Submission


# NOTE: We don't have delete mixin
class CompetitionViewSet(ChaHubModelViewSet):
    """Updating and inserting competitions are done by Producers.

    request.user = Producer in this case."""
    queryset = Competition.objects.all()
    serializer_class = serializers.CompetitionDetailSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
    pagination_class = BasicPagination
    lookup_field_on_deletion = 'remote_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CompetitionListSerializer
        elif self.action == 'create':
            return serializers.CompetitionCreationSerializer
        return self.serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['producer'] = self.request.user
        return context

    def get_queryset(self):
        # TODO: Filter out competitions that don't belong to this provider ???

        qs = Competition.objects.all()
        qs = qs.prefetch_related('phases', 'producer', 'admins', 'participants')
        return qs

    def create(self, request, *args, **kwargs):
        """Overriding this for the following reasons:

        1. Returning the huge amount of HTML/etc. back by default by DRF was bad
        2. We want to handle creating many competitions this way, and we do that
           custom to make drf-writable-nested able to interpret everything easily"""
        # Make the serializer take many competitions at once
        for competition in request.data:
            serializer = self.get_serializer(data=competition)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.phases.update(deleted=True)
        super().perform_destroy(instance)


class SubmissionViewSet(ChaHubModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer
    lookup_field_on_deletion = 'remote_id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['producer'] = self.request.user
        return context

    def create(self, request, *args, **kwargs):
        """Overriding this so we return an empty response instead of the details of the created object"""
        for submission in request.data:
            serializer = self.get_serializer(data=submission)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)
