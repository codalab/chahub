from django.http import HttpResponse
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


def profile(request, id):
    return render(request, 'profiles/profile.html', {'User': User.objects.get(id=id)})
