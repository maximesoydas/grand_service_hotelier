from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from interventions_web_manager.views import interventions_view, index, interventions_list, update_intervention_status, add_intervention, delete_intervention

schema_view = get_schema_view(
    openapi.Info(
        title="Interventions API",
        default_version='v1',
        description="API documentation for the Interventions Manager",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/interventions/', interventions_list, name='interventions'),
    path('interventions', interventions_view, name="interventions"),
    path('api/update_intervention_status/', update_intervention_status, name='update-intervention-status'),
    path('api/add_intervention/', add_intervention, name='add-intervention'),
    path('api/delete_intervention/', delete_intervention, name='delete-intervention'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
