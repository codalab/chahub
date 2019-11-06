from django.urls import path

from . import views

app_name = "datasets"

urlpatterns = [
    path('<int:pk>/', views.DatasetDetail.as_view(), name='detail')
]
