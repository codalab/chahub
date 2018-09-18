from django.views.generic import TemplateView

from utils.views import AdminRequired


class ProducerManagementView(AdminRequired, TemplateView):
    template_name = 'producers/management.html'
