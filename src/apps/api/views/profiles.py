from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers.profiles import MyProfileSerializer, ProfileDetailSerializer

User = get_user_model()


# TODO: Probably should remove GetMyProfile in place of just using ProfileViewSet
# ...that is, unless we need special private data from our own profile, like email
class GetMyProfile(RetrieveAPIView, GenericAPIView):
    # queryset = User.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ProfileView(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileDetailSerializer
