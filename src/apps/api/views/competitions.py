from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers import competitions as serializers
from api.views.mixins import ProducerModelViewSet
from competitions.models import Competition, Submission, CompetitionParticipant


class CompetitionParticipantViewSet(ProducerModelViewSet):
    queryset = CompetitionParticipant.objects.all()
    serializer_class = serializers.CompetitionParticipantListSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CompetitionParticipantCreationSerializer
        return self.serializer_class


class CompetitionViewSet(ProducerModelViewSet):
    """Updating and inserting competitions are done by Producers.

    request.user = Producer in this case."""
    queryset = Competition.objects.all()
    serializer_class = serializers.CompetitionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)


class SubmissionViewSet(ProducerModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)

