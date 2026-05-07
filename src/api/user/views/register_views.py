from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User, UserOTPVerifications
from api.user.serializers import user_serializers
from api.send_mail_sms import send_otp_email
from django.utils import timezone

class RegisterViews(APIView):

    def post(self, request):

        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        if password != password2:
            return Response({
                "error": "Passwords not match"
            }, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            User.objects.get(email=email)
            return Response({
                "error": "Email already exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        ser = user_serializers.UserCreateSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            user = User.objects.get(email=email)
            otp = UserOTPVerifications.objects.create(
                user=user,
                code="",
                expired_at=timezone.now(),
                error_expired_at=timezone.now()
            )
            code = otp.generate_code()
            send_otp_email(email, code)
            return Response({
                "message": "Verifications code sent to your email"
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "error": "Something went wrong"
        }, status=status.HTTP_400_BAD_REQUEST)
        

