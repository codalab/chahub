from django.urls import path

from . import views

app_name = "profiles"
urlpatterns = [
    path('signup', views.SignUpView.as_view(), name="signup"),
    path('detail/<str:username>', views.UserView.as_view(), name="user_profile"),
    path('merge/<uuid:merge_key>', views.MergeAccountsView.as_view(), name="finalize_merge"),
    path('merge/', views.MergeAccountsView.as_view(), name="merge"),
    path('verify_email/<uuid:verification_key>', views.verify_email, name="verify_email")
]
