import json

import requests
from django.http import Http404
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model

from profiles.forms import ChahubCreationForm
from profiles.models import Profile

User = get_user_model()


def sign_up(request):
    # return HttpResponse("Not implemented yet!")

    if request.method == 'POST':
        form = ChahubCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # return HttpResponse("User created successfully!")
            return redirect('/')
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = ChahubCreationForm()
        return render(request, 'registration/signup.html', {'form': form})


# Todo: Make this into a class based view
def profile(request, username):
    context = {}
    user = None
    profiles = None
    try:
        user = User.objects.get(username=username)
        print(user)
    except User.DoesNotExist:
        profiles = Profile.objects.filter(username=username)
        profiles.filter(email=profiles.first().email)
        print(profiles)

    if user and not profiles:
        context['object_mode'] = 'user'
        context['objects'] = user.pk
    elif profiles and not user:
        context['object_mode'] = 'profile'
        context['objects'] = [profile.pk for profile in profiles]
    else:
        raise Http404("No profile or user could be found for that email!")

    return render(request, 'profiles/profile.html', context)
