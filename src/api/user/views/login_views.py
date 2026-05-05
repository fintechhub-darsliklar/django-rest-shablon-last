from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User


class LoginView(APIView):

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        message = "Email or password wrong"
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user.is_active:
                    return Response({
                        "message": "Login successs",
                    }, status=status.HTTP_200_OK)
                message = "User not verified!"
        except:
            pass

        return Response({
            "error": message,
        }, status=status.HTTP_400_BAD_REQUEST)
    
