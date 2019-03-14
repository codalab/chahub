from django.conf.urls import url
from django.urls import path

from . import views

app_name = "profiles"
urlpatterns = [
    url(r'^signup', views.sign_up, name="signup"),
    path('<str:username>', views.profile, name="profile")
]
