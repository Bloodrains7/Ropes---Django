from celery import shared_task
from datetime import timedelta
from celery.utils.time import timezone

from udigital.models import Comment


@shared_task
def delete_old_comments():
    threshold = timedelta(days=30)
    past_date = timezone.now() - threshold
    Comment.objects.filter(timestamp__lte=past_date).delete()
