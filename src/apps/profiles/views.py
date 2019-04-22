import json

import requests
from django.http import Http404
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model

from profiles.forms import ChahubCreationForm

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


def profile(request, username):
    try:
        user = User.objects.select_related('github_info').get(username=username)
    except User.DoesNotExist:
        raise Http404()


    # TODO Get competitions list


    # TODO can move to frontend?
    if user.github_info:
        r = requests.get(user.github_info.repos_url)
        my_repos = json.loads(r.text)
        languages = []

        for obj in my_repos:
            if obj["language"] is not None:
                languages.append(obj["language"])
            # Removes duplicates from the list
            languages = list(dict.fromkeys(languages))

        github_info_context = json.dumps({
                "github_uid": user.github_info.github_uid,
                "login": user.github_info.login,
                "avatar_url": user.github_info.avatar_url,
                "gravatar_id": user.github_info.gravatar_id,
                "html_url": user.github_info.html_url,
                "name": user.github_info.name,
                "company": user.github_info.company,
                "bio": user.github_info.bio,
                "location": user.github_info.location,
                "created_at": str(user.github_info.created_at),
                "updated_at": str(user.github_info.updated_at),
                "node_id": user.github_info.node_id,
                "url": user.github_info.url,
                "followers_url": user.github_info.followers_url,
                "following_url": user.github_info.following_url,
                "gists_url": user.github_info.gists_url,
                "starred_url": user.github_info.starred_url,
                "subscriptions_url": user.github_info.subscriptions_url,
                "organizations_url": user.github_info.organizations_url,
                "repos_url": user.github_info.repos_url,
                "events_url": user.github_info.events_url,
                "received_events_url": user.github_info.received_events_url,
            })
    else:
        languages = []
        github_info_context = None

    return render(request, 'profiles/profile.html', {
        'user': json.dumps({
            "username": user.username,
            "name": user.name,
            "id": user.id,
            "languages": languages,
            # "competitions":
            "github_info": github_info_context,
        }),
    })
