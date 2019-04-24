from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers.profiles import MyProfileSerializer, ProfileSerializer
from profiles.models import Profile

User = get_user_model()


class GetMyProfile(RetrieveAPIView, GenericAPIView):
    # queryset = User.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (ProducerAuthentication, SessionAuthentication, )
    permission_classes = (ProducerPermission, )
    http_method_names = ['GET', 'POST', 'PUT']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['producer'] = self.request.user
        return context

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        for profile in request.data:
            try:
                instance = self.queryset.get(remote_id=profile.get('remote_id'))
            except Profile.DoesNotExist:
                instance = None
            # instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            if instance:
                self.perform_update(serializer)
            else:
                self.perform_create(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

        return Response({}, status=status.HTTP_202_ACCEPTED)

    # def perform_update(self, serializer):
    #     super().perform_update()
    #     # serializer.save()

    def partial_update(self, request, *args, **kwargs):
        # kwargs['partial'] = True
        # return self.update(request, *args, **kwargs)
        return super().partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Overriding this for the following reasons:

        1. Returning the huge amount of HTML/etc. back by default by DRF was bad
        2. We want to handle creating many competitions this way, and we do that
           custom to make drf-writable-nested able to interpret everything easily"""
        # Make the serializer take many competitions at once
        for profile in request.data:
            serializer = self.get_serializer(data=profile)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)
