from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView, RetrieveAPIView

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers.profiles import MyProfileSerializer, ProfileSerializer
from api.views.mixins import BulkViewSetMixin
from profiles.models import Profile

User = get_user_model()


# TODO: Probably should remove GetMyProfile in place of just using ProfileViewSet
# ...that is, unless we need special private data from our own profile, like email
class GetMyProfile(RetrieveAPIView, GenericAPIView):
    # queryset = User.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # def get_object(self):
    #     return self.request.user


class ProfileViewSet(BulkViewSetMixin, ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (ProducerAuthentication, SessionAuthentication, )
    permission_classes = (ProducerPermission, )

    # def create(self, request, *args, **kwargs):
    #     """Overriding this for the following reasons:
    #
    #     1. Returning the huge amount of HTML/etc. back by default by DRF was bad
    #     2. We want to handle creating many competitions this way, and we do that
    #        custom to make drf-writable-nested able to interpret everything easily"""
    #
    #     serializer = self.get_serializer(data=request.data, partial=False, many=True)
    #     serializer.is_valid(raise_exception=False)
    #     if serializer.errors:
    #         print(serializer.errors)
    #     else:
    #         self.perform_create(serializer)
    #
    #
    #     return Response({}, status=status.HTTP_201_CREATED)
    #     # headers = self.get_success_headers(serializer.data)
    #     # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
