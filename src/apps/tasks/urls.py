from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path('<int:pk>/', views.TaskDetail.as_view(), name='detail')
]
