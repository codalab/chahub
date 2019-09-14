from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers.profiles import AccountMergeRequestSerializer, UserDetailSerializer, MyUserDetailSerializer, \
    ProfileDetailSerializer, ProfileCreateSerializer
from profiles.models import Profile, EmailAddress

User = get_user_model()


class GetMyProfile(RetrieveAPIView, GenericAPIView):
    serializer_class = MyUserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDetailSerializer

    def get_serializer_class(self):
        user = self.get_object()
        if self.request.user == user or self.request.user.is_superuser or self.request.user.is_staff:
            return MyUserDetailSerializer
        else:
            return UserDetailSerializer

    def get_queryset(self):
        return super().get_queryset().select_related('github_user_info')

    @action(detail=True, methods=('POST',))
    def add_email_address(self, request, pk, version):
        user = self.get_object()
        email_address = request.data.get('email_address')
        if not email_address:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user.add_email(email_address)
        return Response({}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=('POST',))
    def resend_verification_email(self, request, pk, version):
        user = self.get_object()
        email_pk = request.data.get('email_pk')
        if not email_pk:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user.resend_verification_email(email_pk)
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=('DELETE',))
    def remove_email_address(self, request, pk, version):
        email_pk = request.data.get('email_pk')
        if not email_pk:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()
        email = get_object_or_404(EmailAddress, id=email_pk, user=user)
        if request.user != user and not request.user.is_staff and not request.user.is_superuser or email.primary or user.email_addresses.count() == 1:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        email.delete()
        user.refresh_profiles()
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=('POST',))
    def change_primary_email(self, request, pk, version):
        email_pk = request.data.get('email_pk')
        if not email_pk:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()
        email = get_object_or_404(EmailAddress, id=email_pk, user=user)
        if request.user != user and not request.user.is_staff and not request.user.is_superuser:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        email.make_primary()
        return Response({}, status=status.HTTP_200_OK)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    authentication_classes = (ProducerAuthentication, SessionAuthentication, )
    permission_classes = (ProducerPermission, )

    def get_queryset(self):
        pks_list = self.request.query_params.getlist('pk[]')
        if pks_list:
            return self.queryset.filter(pk__in=pks_list)
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return ProfileCreateSerializer
        return self.serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['producer'] = self.request.user
        return context

    def create(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        profiles_created = 0
        for profile in request.data:
            if not profile.get('producer') and context.get('producer'):
                profile['producer'] = context['producer'].pk
            serializer = self.get_serializer(data=profile)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            profiles_created += 1
        return Response({'profiles_created': profiles_created}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_merge_request(request, version):
    serializer = AccountMergeRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
