from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from datetime import timedelta
from .models import Post
from sign.models import UserCode
from django.contrib.auth.models import User


@shared_task()
def weekly_notification_task():
    last_week = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    users = User.objects.filter()

    for user in users:
        html_content = render_to_string(
            'board/weekly_notif.html',
            {
                'user': user.username,
                'posts': posts,
                'link': settings.SITE_URL,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Публикации за прошедшую неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def clear_old_codes():

    cutoff_date = timezone.now() - timedelta(minutes=10)

    deleted_count, _ = UserCode.objects.filter(created_at__lt=cutoff_date).delete()

    return f"Успешно удалено {deleted_count} старых записей."