from django.contrib import admin
from django.urls import (
    path,
    include,
)
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import (
    EmailTokenObtainPairView,
    LogoutView,
    SocialLogin,
)


schema_view = get_schema_view(
   openapi.Info(
      title="Shitter API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),    # for register, password change and retrieving user data
    path('auth/google/', SocialLogin.as_view({
        'post': 'create',
        'put': 'log_in'
    })),   # for google reg/auth
    path('api/v1/', include('users.urls')),

    path("token/login/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),   # for auth
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/logout/", LogoutView.as_view(), name="blacklist_token"),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
