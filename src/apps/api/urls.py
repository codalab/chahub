from django.conf.urls import url, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from .views import competitions, profiles, search, data, tasks, producers

API_PREFIX = "v1"

# API routes
router = SimpleRouter()
router.register('producers', producers.ProducerViewSet)
router.register('competitions', competitions.CompetitionViewSet)
router.register('phases', competitions.PhaseViewSet)
router.register('participants', competitions.CompetitionParticipantViewSet)
router.register('submissions', competitions.SubmissionViewSet)
router.register('profiles', profiles.ProfileViewSet)
router.register('users', profiles.UserViewSet)
router.register('datasets', data.DataViewSet)
router.register('tasks', tasks.TaskViewSet)
router.register('solutions', tasks.SolutionViewSet)

# Documentation details
schema_view = get_schema_view(
    openapi.Info(
        title="Chahub API",
        default_version='v1',
        description="Chahub is a platform for machine learning resources, like competitions, test sets, and example solutions",
        contact=openapi.Contact(email="info@codalab.org"),
        license=openapi.License(name="MIT License"),
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url('^', include(router.urls)),
    url('query/', search.SearchView.as_view()),
    url('my_profile/', profiles.GetMyProfile.as_view()),
    url('producer_stats/', producers.producer_statistics, name='producer_stats'),
    url('create_merge_request/', profiles.create_merge_request, name='create_merge_request'),

    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Docs
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=None), name='docs'),

    # Optionally, use "redoc" style
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]
