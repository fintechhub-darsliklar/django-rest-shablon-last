from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User, UserOTPVerifications, UserOTPIDVerifications
from django.utils import timezone
from datetime import timedelta
from api.send_mail_sms import send_otp_email


    
class ResendVerificationsOTPView(APIView):

    def send_otp_code(self, otp_data):
        code = otp_data.generate_code()
        send_otp_email(otp_data.user.email, code, "otp")

    def post(self, request, otp_type):
        email = request.data.get("email")
        if otp_type not in ("otp", "link"):
            return Response({
                "error": "error from sending resend code"
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except:
            return Response({
                "error": "error from sending resend code"
            }, status=status.HTTP_400_BAD_REQUEST)
        otp_data = UserOTPVerifications.objects.filter(user=user).last()
        now = timezone.now()
        if not otp_data:
            return Response({
                "error": "error from sending resend code"
            }, status=status.HTTP_400_BAD_REQUEST)

        if otp_data.is_code_expired():
            return Response({
                "error": f"you can resend mail code after: {otp_data.expired_at}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if otp_data.resend_attapts >= 3:
            otp_data.error_expired_at = now + timedelta(days=1)
            otp_data.resend_attapts = 0
            otp_data.attapts = 0
            otp_data.save()
            return Response({
                "error": f"you can resend mail code after: {otp_data.error_expired_at}"
            }, status=status.HTTP_400_BAD_REQUEST)

        if now < otp_data.error_expired_at:
            return Response({
                "error": f"you can resend mail code after: {otp_data.error_expired_at}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if now - timedelta(minutes=5) > otp_data.expired_at:
            return Response({
                "error": "error from sending resend code"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        otp_data.resend_attapts += 1
        self.send_otp_code(otp_data)

        return Response({
            "message": "Verifications code sent to your email"
        }, status=status.HTTP_201_CREATED)
            
    

