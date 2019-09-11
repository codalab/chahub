from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers.profiles import AccountMergeRequestSerializer, UserDetailSerializer, MyUserDetailSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        user = self.get_object()
        if self.request.user == user or self.request.user.is_superuser or self.request.user.is_staff:
            return MyUserDetailSerializer
        else:
            return UserDetailSerializer

    def get_queryset(self):
        return super().get_queryset().select_related('github_user_info')


@api_view(['POST'])
def create_merge_request(request, version):
    serializer = AccountMergeRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
