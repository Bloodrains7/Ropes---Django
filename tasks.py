
from datetime import timedelta

from django.utils import timezone

from udigital.models import Comment

# @shared_task
# def delete_old_comments_task():
#     threshold = timedelta(days=30)
#     past_date = timezone.now() - threshold
#     Comment.objects.filter(timestamp__lte=past_date).delete()


def delete_old_comments():
    print(timezone.now(), "Deleting old comments...")
    threshold = timedelta(minutes=1)
    past_date = timezone.now() - threshold
    Comment.objects.filter(timestamp__lte=past_date).delete()
