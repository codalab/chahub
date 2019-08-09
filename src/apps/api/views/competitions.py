from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers import competitions as serializers
from api.views.mixins import BulkViewSetMixin
from competitions.models import Competition, Submission, CompetitionParticipant


class CompetitionParticipantViewSet(BulkViewSetMixin, ModelViewSet):
    queryset = CompetitionParticipant.objects.all()
    serializer_class = serializers.CompetitionParticipantListSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CompetitionParticipantCreationSerializer
        return self.serializer_class

    def get_queryset(self):
        qs = self.queryset
        return qs


# NOTE: We don't have delete mixin
class CompetitionViewSet(BulkViewSetMixin, ModelViewSet):
    """Updating and inserting competitions are done by Producers.

    request.user = Producer in this case."""
    queryset = Competition.objects.all()
    serializer_class = serializers.CompetitionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)


# NOTE: We don't have delete mixin
class SubmissionViewSet(BulkViewSetMixin, ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)

