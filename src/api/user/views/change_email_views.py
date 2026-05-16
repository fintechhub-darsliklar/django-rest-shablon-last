from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.models import ChangeEmailLogs
from django.utils import timezone
from datetime import timedelta


class ChangeEmailViews(APIView):
    permission_classes = [IsAuthenticated]

    def create_change_email(self, user, exp_at):
        
           ChangeEmailLogs.objects.create(
            user=user,
            expired_at=exp_at,
            error_expired_at=self.now,
            
        )


    def get(self, request):
        now = timezone.now()
        self.now = now
        change_email_obj = ChangeEmailLogs.objects.filter(user=request.user).last()
        if change_email_obj:
            user_is_blocked = change_email_obj.is_blocked()
            if user_is_blocked:
                return Response({
                    "error": f"your account blocked until {user_is_blocked}"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            can_changed = change_email_obj.is_expired()
            if can_changed:
                return Response({
                    "message": f"you can change your password within {can_changed}"
                })

        
            if change_email_obj.attapts > 5:
                change_email_obj.error_expired_at = now + timedelta(days=3)
                change_email_obj.attapts = 0
                change_email_obj.save()
                return Response({
                    "error": f"your account blocked until {user_is_blocked}"

                }, status=status.HTTP_400_BAD_REQUEST)
        
        
        
            if change_email_obj.created_at >= now - timedelta(days=3) and change_email_obj.is_changed == False:
                change_email_obj.attapts += 1
                change_email_obj.expired_at = now + timedelta(minutes=15)
                change_email_obj.save()
            else:
                self.create_change_email(request.user, now + timedelta(minutes=15))
        else:
            self.create_change_email(request.user, now + timedelta(minutes=15))
        
        
        
        return Response({
            
            "message": "you can change your email within 15 minute"
        })
