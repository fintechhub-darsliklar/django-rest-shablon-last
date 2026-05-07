from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_otp_email(user_email, otp_code):
    # 1. HTML tarkibni render qilish
    context = {'code': otp_code}
    html_message = render_to_string('verify_email.html', context)
    
    # 2. Plain text varianti (HTML qo'llab-quvvatlamaydigan pochta xizmatlari uchun)
    plain_message = strip_tags(html_message)
    subject = f"Tasdiqlash kodi"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    # 3. Xatni yuborish
    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    )