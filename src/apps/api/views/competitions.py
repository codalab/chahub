from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers import competitions as serializers
from competitions.models import Competition, Submission


# NOTE: We don't have delete mixin
class CompetitionViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    """Updating and inserting competitions are done by Producers.

    request.user = Producer in this case."""
    queryset = Competition.objects.all()
    serializer_class = serializers.CompetitionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['producer'] = self.request.user
        return context

    def get_queryset(self):
        qs = Competition.objects.all()
        qs = qs.prefetch_related('phases', 'producer', 'admins', 'participants')
        return qs

    def create(self, request, *args, **kwargs):
        # We're only overriding this so that we can replace the response with an empty dictionary
        # instead of sending back the huge HTML text
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({}, status=status.HTTP_201_CREATED, headers=headers)


#
#
# class PhaseViewSet(ModelViewSet):
#     queryset = Phase.objects.all()
#     serializer_class = serializers.PhaseSerializer
#
#

# NOTE: We don't have delete mixin
class SubmissionViewSet(CreateModelMixin, GenericViewSet):
    queryset = Submission.objects.all()
    serializer_class = serializers.SubmissionSerializer
    authentication_classes = (ProducerAuthentication,)
    permission_classes = (ProducerPermission,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['producer'] = self.request.user
        return context
