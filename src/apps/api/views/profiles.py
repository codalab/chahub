from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, RetrieveAPIView

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers.profiles import MyProfileListSerializer, BaseProfileSerializer, AccountMergeRequestSerializer, \
    MyProfileDetailSerializer, ProfileDetailSerializer, ProfileCreateSerializer
from api.views.mixins import ProducerModelViewSet
from profiles.models import Profile

User = get_user_model()


# TODO: Probably should remove GetMyProfile in place of just using ProfileViewSet
# ...that is, unless we need special private data from our own profile, like email
class GetMyProfile(RetrieveAPIView, GenericAPIView):
    # queryset = User.objects.all()
    serializer_class = MyProfileDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MyProfileDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return MyProfileListSerializer
        return self.serializer_class


class ProfileViewSet(ProducerModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    authentication_classes = (ProducerAuthentication, SessionAuthentication, )
    permission_classes = (ProducerPermission, )

    def get_queryset(self):
        pks_list = self.request.query_params.getlist('pk')
        if pks_list:
            return self.queryset.filter(pk__in=pks_list)
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'list':
            # If we're getting back multiple profiles through the query parameter, give more information
            if self.request.query_params.getlist('pk'):
                return ProfileDetailSerializer
            return BaseProfileSerializer
        if self.action == 'create':
            return ProfileCreateSerializer
        return self.serializer_class


@api_view(['POST'])
def create_merge_request(request, version):
        if not request.data.get('master_account') or not request.data.get('secondary_account'):
            return Response("Master account and or secondary account not provided!", status=status.HTTP_400_BAD_REQUEST)
        serializer = AccountMergeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.errors:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                serializer.save()
            except ValidationError as error:
                return Response({'error': error.messages[0]}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
