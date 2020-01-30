from django.urls import path

from . import views

app_name = "competitions"

urlpatterns = [
    path('<int:pk>/', views.CompetitionDetail.as_view(), name='detail')
]
