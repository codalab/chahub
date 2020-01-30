import debug_toolbar

from django.conf import settings
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', include('pages.urls')),
    path('api/<str:version>/', include('api.urls')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('producers/', include('producers.urls', namespace='producers')),
    path('competitions/', include('competitions.urls', namespace='competitions')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('datasets/', include('datasets.urls', namespace='datasets')),
    # Django built in
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    # Third party
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('social/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

# OLD, keeping around in case we try RiotJS routers again
# Catch all for our single page app routing, everything else goes to index.html for routing
# urlpatterns += [re_path(r'.*', TemplateView.as_view(template_name="index.html"))]
