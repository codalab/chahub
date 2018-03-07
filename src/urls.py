import debug_toolbar
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

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
urlpatterns += [re_path(r'.*', TemplateView.as_view(template_name="index.html"))]
