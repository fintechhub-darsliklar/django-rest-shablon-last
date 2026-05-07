from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User, UserOTPVerifications
from api.user.serializers import user_serializers
from api.send_mail_sms import send_otp_email
from django.utils import timezone
from datetime import timedelta


class VerificationsOTPView(APIView):

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        if not email or not code or len(code) != 6:
            return Response({
                "error": "Email and code required"
            }, status=status.HTTP_400_BAD_REQUEST)
        now = timezone.now()
        try:
            otp = UserOTPVerifications.objects.get(user__email=email)
            if otp.error_expired_at > now:
                return Response({
                    "error": f"Your account blocked until {otp.error_expired_at}"
                }, status=status.HTTP_400_BAD_REQUEST)
            if code != otp.code:
                otp.attapts += 1
                if otp.attapts > 6:
                    otp.expired_at = now
                    otp.attapts = 0
                    otp.error_expired_at = now + timedelta(minutes=5)
                    otp.code = ""
                    otp.save()
                    return Response({
                        "error": f"Your account blocked until {otp.error_expired_at}"
                    }, status=status.HTTP_400_BAD_REQUEST)
                otp.save()
                return Response({
                    "error": f"sms code wrong! attapts: {otp.attapts}"
                }, status=status.HTTP_400_BAD_REQUEST)

            if not otp.is_code_expired():
                return Response({
                    "error": f"sms code expired. please resend!"
                }, status=status.HTTP_400_BAD_REQUEST)
            otp.expired_at = now
            otp.user.is_active = True
            otp.user.save()
            otp.save()

            return Response({
                "error": "Your account verified!"
            }, status=status.HTTP_200_OK)

        except:
            return Response({
                "error": "Verifications code expired!"
            }, status=status.HTTP_400_BAD_REQUEST)