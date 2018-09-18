import json

import debug_toolbar
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import TemplateView

from producers.models import Producer

urlpatterns = [
    # Our URLS
    # path('', include('pages.urls', namespace='pages')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('producers/', include('producers.urls', namespace='producers')),

    # Third party
    path('api/<str:version>/', include('api.urls')),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Django built in
    # path('accounts/', include('django.contrib.auth.urls', namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

# Catch all for our single page app routing, everything else goes to index.html for routing
# urlpatterns += [re_path(r'.*', TemplateView.as_view(template_name="index.html"))]


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """We want to send some content to the front page before the page loads,
        we used to have to ping the API for producer data, for example"""
        context = super().get_context_data(**kwargs)
        context['producers'] = json.dumps(list(Producer.objects.all().values('id', 'name', 'url')))

        if not self.request.GET:
            from api.views.search import get_default_search_results
            context['default_search_results'] = json.dumps(get_default_search_results())

        return context

    # I don't think we'll use this in an iframe, but just-in-case
    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


urlpatterns += [re_path(r'^$', IndexView.as_view())]
