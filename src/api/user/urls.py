from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.user.views.login_views import LoginView
from api.user.views.register_views import RegisterViews

router = DefaultRouter()
router.include_root_view = False

urlpatterns = [
    path("auth/login/", LoginView.as_view()),
    path("auth/register/", RegisterViews.as_view()),
    # path('', include(router.urls)),
    # path('restaurant/', RestaurantViewset.as_view({'get': 'list','post':'create'}), name='restaurant-detail'),
]
