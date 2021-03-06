from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.authenticators import ProducerAuthentication
from api.permissions import ProducerPermission
from api.serializers.profiles import AccountMergeRequestSerializer, UserSerializer, MyUserSerializer, \
    ProfileSerializer, ProfileCreateSerializer, ProfileListSerializer
from profiles.models import Profile, EmailAddress

User = get_user_model()


class GetMyProfile(RetrieveAPIView, GenericAPIView):
    serializer_class = MyUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_serializer_class(self):
        user = self.get_object()
        if self.has_permission(self.request, user):
            return MyUserSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return super().get_queryset().select_related('github_user_info')
        else:
            return super().get_queryset()

    def has_permission(self, request, user):
        return request.user == user or request.user.is_superuser or request.user.is_staff

    @action(detail=True, methods=('POST',), url_name='add_email_address')
    def add_email_address(self, request, pk, version):
        email_address = request.data.get('email_address')
        if not email_address:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()
        if not self.has_permission(request, user):
            raise PermissionDenied('You do not have permission to add an email address to this user')
        email = user.add_email(email_address)
        if email:
            return Response({'added email': email.email}, status=status.HTTP_201_CREATED)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('POST',), url_name="resend_verification_email")
    def resend_verification_email(self, request, pk, version):
        email_pk = request.data.get('email_pk')
        if not email_pk:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()
        if not self.has_permission(request, user):
            raise PermissionDenied('You do not have permission to resend this email')
        user.resend_verification_email(email_pk)
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=('DELETE',), url_name="remove_email_address")
    def remove_email_address(self, request, pk, version):
        email_pk = request.data.get('email_pk')
        if not email_pk:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()
        email = get_object_or_404(EmailAddress, id=email_pk, user=user)
        if not self.has_permission(request, user) or email.primary or user.email_addresses.count() == 1:
            raise PermissionDenied('You do not have permission to remove an email address from this user')
        email.delete()
        user.refresh_profiles()
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=('POST',), url_name="change_primary_email")
    def change_primary_email(self, request, pk, version):
        email_pk = request.data.get('email_pk')
        if not email_pk:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()
        if not self.has_permission(request, user):
            raise PermissionDenied("You do not have permission to change this user's primary email")
        email = get_object_or_404(EmailAddress, id=email_pk, user=user)
        email.make_primary()
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=('DELETE',), url_name='scrub_profile')
    def scrub_profile(self, request, pk, version):
        profile_pk = request.data.get('profile_pk')
        if not profile_pk:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()
        profile = get_object_or_404(Profile, user=user, id=profile_pk)
        if not self.has_permission(request, user):
            raise PermissionDenied('You do not have permission to delete this profile')
        profile.scrubbed = True
        profile.save()
        return Response({}, status=status.HTTP_200_OK)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (ProducerAuthentication, SessionAuthentication, )
    permission_classes = (ProducerPermission, )

    def get_queryset(self):
        qs = self.queryset
        if self.request.method == 'GET':
            qs = qs.select_related(
                'producer',
            )
        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return ProfileCreateSerializer
        if self.action == 'list':
            return ProfileListSerializer
        return ProfileSerializer

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
