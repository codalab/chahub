from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model, authenticate, login
from django.views.generic import TemplateView

from profiles.forms import ChahubCreationForm
from profiles.models import Profile, AccountMergeRequest
from profiles.utils import validate_next_url

User = get_user_model()


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChahubCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ChahubCreationForm(self.request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            next_url = self.request.GET.get('next')
            if next_url:
                if validate_next_url(next_url):
                    return HttpResponseRedirect(next_url)
            return redirect('/')
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)


class MergeAccountsView(TemplateView):
    template_name = 'profiles/merge.html'

    # TODO: We should require login? Not just a uuid key?
    def get(self, request, *args, **kwargs):
        # if not self.request.user.is_authenticated:
        #     return HttpResponseForbidden()
        merge_key = self.kwargs.get('merge_key')
        context = self.get_context_data(**kwargs)
        if merge_key:
            # Do merge stuff then redirect
            try:
                merge_request = AccountMergeRequest.objects.get(key=merge_key)
                # merge_request.merge_accounts()
                # merge_request.secondary_account.delete()
                merge_request.delete()
                self.request.session['message'] = 'Successfully merged accounts'
                return redirect('profiles:merge_success')
            except AccountMergeRequest.DoesNotExist:
                raise Http404("Could not find a merge request with that key.")
        else:
            if self.request.session.get('message'):
                context['message'] = self.request.session.pop('message', None)
            # else:
            #     raise Http404("Could not find a valid merge request for that key.")
        return self.render_to_response(context)


class ProfileView(TemplateView):
    """This view returns to context either:
        a) A user or list profiles
        b) A specific profile
    """
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.pop('username', None)
        producer = self.kwargs.pop('producer', None)
        remote_id = self.kwargs.pop('remote_id', None)

        # If we're given a username, and not a producer, or a remote_id
        if username and not (producer or remote_id):
            user, profiles = None, None
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                profiles = Profile.objects.filter(username=username)
                if profiles.exists():
                    # Refine our query further based on the first result, matching emails
                    profiles = profiles.filter(email__in=profiles.values_list('email', flat=True))
                else:
                    profiles = None
            # If we got a user instead of profiles
            if user and not profiles:
                context['object_mode'] = 'user'
                context['objects'] = user.pk
            # If we got profiles instead of a user
            elif profiles and not user:
                context['object_mode'] = 'profile_list'
                context['objects'] = profiles.values_list('pk', flat=True)
            # Neither
            else:
                raise Http404("No profile or user could be found for that username!")
        # If we're not given a username and we're given a specific producer and remote_id
        elif not username and (producer and remote_id):
            try:
                profile = Profile.objects.get(remote_id=remote_id, producer=producer)
                context['object_mode'] = 'profile'
                context['objects'] = profile.pk
            except Profile.DoesNotExist:
                raise Http404("No profile could be found matching that producer and remote_id")
        else:
            return HttpResponseBadRequest(content='Bad request; Please only provide either a username OR a producer ID and remote_id combo.')
        return context
