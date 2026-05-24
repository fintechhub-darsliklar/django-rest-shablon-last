from django.urls import path, include

urlpatterns = [
    path('admin/', include('api.admin.urls')),
    path('user/', include('api.user.urls')),
    path('auth/', include('api.auth.urls')),
]
