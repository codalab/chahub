from django.conf.urls import url
from django.urls import path

from . import views

app_name = "profiles"
urlpatterns = [
    # url(r'^signup', views.sign_up, name="signup"),
    url(r'^signup', views.SignUpView.as_view(), name="signup"),
    path('detail/<str:username>', views.ProfileView.as_view(), name="profile"),
    path('detail/<int:producer>/<int:remote_id>', views.ProfileView.as_view(), name="profile"),
    path('merge/<uuid:merge_key>', views.MergeAccountsView.as_view(), name="merge"),
    path('merge/', views.MergeAccountsView.as_view(), name="merge_success")
]
