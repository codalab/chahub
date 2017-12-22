from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers import competitions as serializers
from competitions.models import Competition, Phase, Submission



class CompetitionViewSet(ModelViewSet):
    """Updating and inserting competitions are done by Producers.

    request.user = Producer in this case."""
    queryset = Competition.objects.all()
    serializer_class = serializers.CompetitionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)

    def get_serializer_context(self):
        context = super().get_serializer_context()














        # TODO: Handle this in serializer
        context['producer'] = self.request.user

        return context

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)
#
#
# class PhaseViewSet(ModelViewSet):
#     queryset = Phase.objects.all()
#     serializer_class = serializers.PhaseSerializer
#
#
# class SubmissionViewSet(ModelViewSet):
#     queryset = Submission.objects.all()
#     serializer_class = serializers.SubmissionSerializer
