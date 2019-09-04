from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.pagination import BasicPagination
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
    serializer_class = serializers.CompetitionDetailSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
    pagination_class = BasicPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CompetitionListSerializer
        return self.serializer_class


class SubmissionViewSet(ProducerModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)
    pagination_class = BasicPagination


    def create(self, request, *args, **kwargs):
        """Overriding this so we return an empty response instead of the details of the created object"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({}, status=status.HTTP_201_CREATED, headers=headers)
