from django.conf.urls import url

from . import views


app_name = 'producers'
urlpatterns = [
    url(r'^$', views.ProducerManagementView.as_view(), name="management"),
]
