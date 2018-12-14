from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers import competitions as serializers
from producers.models import Producer


class ProducerViewSet(ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = serializers.ProducerSerializer
    authentication_classes = (ProducerAuthentication, )
    permission_classes = (ProducerPermission, )

    def create(self, request, *args, **kwargs):
        # Augment the default behavior to return the secret key instead of the entire producer object

        # We then display the API key to the user to forward on to the producer

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({"api_key": serializer.instance.api_key}, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET'])
def producer_statistics(request, version):
    try:
        stats = {
            'competition_count': 0,
            'dataset_count': 0,
            'participant_count': 0,
            'submission_count': 0,
            'user_count': 0,
            'organizer_count': 0,
        }
        for producer in Producer.objects.all():
            for stat_key in stats.keys():
                stats[stat_key] += getattr(producer, stat_key, 0)
        return Response(data=stats, status=status.HTTP_200_OK)
    except:
        return Response(data={'status': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
