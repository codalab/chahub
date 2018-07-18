from django.conf.urls import url

from . import views


app_name = 'pages'
urlpatterns = [
    url(r'^competition/create', views.CompetitionFormView.as_view(), name="competition_create"),
    url(r'^search', views.SearchView.as_view(), name="search"),
]
