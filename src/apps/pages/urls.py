from django.urls import re_path

from pages.views import IndexView

app_name = 'pages'
urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name="index"),
]
