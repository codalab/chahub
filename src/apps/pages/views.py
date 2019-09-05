import json

from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import TemplateView

from producers.models import Producer


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """We want to send some content to the front page before the page loads,
        we used to have to ping the API for producer data, for example"""
        context = super().get_context_data(**kwargs)
        context['producers'] = json.dumps(list(Producer.objects.all().values('id', 'name', 'url')))

        if not self.request.GET:
            from utils.search import get_default_search_results
            context['default_search_results'] = json.dumps(get_default_search_results())

        return context

    # I don't think we'll use this in an iframe, but just-in-case
    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
