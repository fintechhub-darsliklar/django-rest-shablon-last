from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.user.views.login_views import LoginView
from api.user.views.register_views import RegisterViews
from api.user.views.verifications_views import VerificationsOTPView, VerificationsOTPLinkView, VerificationsOTPForgetPasswrdView
from api.user.views.resend_code_views import ResendVerificationsOTPView
from api.user.views.forget_password_views import ForgetPasswordView, SetForgetPasswordView
from api.user.views.change_password_views import ChangePasswordViews


router = DefaultRouter()
router.include_root_view = False

urlpatterns = [
    path("auth/login/", LoginView.as_view()),
    path("auth/resend/<str:otp_type>/", ResendVerificationsOTPView.as_view()),
    path("auth/register/", RegisterViews.as_view()),
    path("auth/register/otp/verify/", VerificationsOTPView.as_view()),
    path("auth/register/confirmations/<uuid:link_id>/", VerificationsOTPLinkView.as_view()),
    path("auth/forget-password/otp/verify/", VerificationsOTPForgetPasswrdView.as_view()),
    path("auth/forget-password/set/", SetForgetPasswordView.as_view()),
    path("auth/forget-password/<str:otp_type>/", ForgetPasswordView.as_view()),
    path("auth/change-password/", ChangePasswordViews.as_view()),

    # path('', include(router.urls)),
    # path('restaurant/', RestaurantViewset.as_view({'get': 'list','post':'create'}), name='restaurant-detail'),
]
