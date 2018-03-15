from django.views.generic import TemplateView


class ProducerManagementView(TemplateView):
    template_name = 'producers/management.html'
