from django.db.models import Count, F

from api.authenticators import ProducerAuthentication
from api.pagination import BasicPagination
from api.permissions import ProducerPermission
from api.serializers import competitions as serializers
from api.views.chahub import ChaHubModelViewSet
from competitions.models import Competition, Submission, CompetitionParticipant, Phase


class CompetitionViewSet(ChaHubModelViewSet):
    """Updating and inserting competitions are done by Producers.

    request.user = Producer in this case."""
    queryset = Competition.objects.all()
    serializer_class = serializers.CompetitionDetailSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
    pagination_class = BasicPagination

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
        qs = Competition.objects.all()
        if self.request.method == 'GET':
            qs = qs.annotate(
                submission_count=Count(F('phases__submissions'), distinct=True)
            ).annotate(
                participant_count=Count(F('participants'), distinct=True)
            ).prefetch_related(
                'phases',
                'producer',
                'admins',
                'participants'
            )
        return qs

    def perform_destroy(self, instance):
        instance.phases.update(deleted=True)
        super().perform_destroy(instance)


class PhaseViewSet(ChaHubModelViewSet):
    queryset = Phase.objects.all()
    serializer_class = serializers.PhaseSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.PhaseCreationSerializer
        else:
            return self.serializer_class


class SubmissionViewSet(ChaHubModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['producer'] = self.request.user
        return context


class CompetitionParticipantViewSet(ChaHubModelViewSet):
    queryset = CompetitionParticipant.objects.all()
    serializer_class = serializers.CompetitionParticipantSerializer
