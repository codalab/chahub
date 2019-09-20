from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views.generic import TemplateView

from profiles.forms import ChahubCreationForm
from profiles.models import AccountMergeRequest, EmailAddress
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


class MergeAccountsView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/merge.html'

    def get(self, request, *args, **kwargs):
        merge_key = self.kwargs.get('merge_key')
        context = self.get_context_data(**kwargs)
        if merge_key:
            # Do merge stuff then redirect
            try:
                merge_request = AccountMergeRequest.objects.get(Q(master_key=merge_key) | Q(secondary_key=merge_key))
                if self.request.user not in [merge_request.master_account.user, merge_request.secondary_account.user]:
                    raise Http404("You must be logged in as one of the users whose accounts you are merging")
                if merge_key == merge_request.master_key:
                    merge_request.master_confirmation = True
                    merge_request.metadata['master_confirmation_at'] = str(now())
                    self.request.session['message'] = 'Successfully Confirmed Master Account. Please confirm the Secondary Account'
                elif merge_key == merge_request.secondary_key:
                    merge_request.secondary_confirmation = True
                    merge_request.metadata['secondary_confirmation_at'] = str(now())
                    self.request.session['message'] = 'Successfully Confirmed Secondary Account. Please confirm the Master Account'
                else:
                    # Shouldn't be possible to hit this, probably
                    raise Http404("Error")
                merge_request.save()
                if merge_request.master_confirmation and merge_request.secondary_confirmation:
                    merge_request.merge_accounts()
                    self.request.session['message'] = 'Successfully merged accounts'
                return redirect('profiles:merge')
            except AccountMergeRequest.DoesNotExist:
                raise Http404("Could not find a merge request with that key.")
        else:
            if self.request.session.get('message'):
                context['message'] = self.request.session.pop('message', None)
        return self.render_to_response(context)


class UserView(TemplateView):
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.pop('username', None)
        try:
            user = User.objects.get(username=username)
            context['user_pk'] = user.id
            context['admin'] = self.request.user.is_superuser or self.request.user.is_staff or self.request.user == user
        except User.DoesNotExist:
            raise Http404('No user found with that username.')
        return context


def verify_email(request, verification_key):
    email = get_object_or_404(EmailAddress, verification_key=verification_key)
    if email.verified:
        return redirect('pages:index')
    email.verify()
    context = {
        "email_address": email.email,
    }
    return render(request, 'profiles/email_verified.html', context)
