from channels import Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers import competitions as serializers
from competitions.models import Competition


class CompetitionViewSet(ModelViewSet):
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

    def create(self, request, *args, **kwargs):
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
# class SubmissionViewSet(ModelViewSet):
#     queryset = Submission.objects.all()
#     serializer_class = serializers.SubmissionSerializer
