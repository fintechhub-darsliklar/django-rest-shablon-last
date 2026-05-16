from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.models import ChangeEmailLogs
from django.utils import timezone
from datetime import timedelta


