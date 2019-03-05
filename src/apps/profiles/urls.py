from django.conf.urls import url

from . import views

app_name = "profiles"
urlpatterns = [
    url(r'^signup', views.sign_up, name="signup"),
    url(r'^(?P<id>\d+)', views.profile, name="profile")
]
