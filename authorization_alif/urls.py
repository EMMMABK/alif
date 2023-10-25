from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from authorization_func.views import UserLogin

schema_view = get_schema_view(
   openapi.Info(
      title="AlifAPI",
      default_version='v1',
      description="Your API description",
      terms_of_service="https://www.alif.com/terms/",
      contact=openapi.Contact(email="alif@gmail.com"),
      license=openapi.License(name="License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path('api/token/', UserLogin.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('admin/', admin.site.urls),
   path('api/', include('authorization_func.urls')),
   path('api/', include('news_func.urls')),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]