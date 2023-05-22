from django.core.mail import send_mass_mail, send_mail
from .models import Post, Category
from django.utils import timezone
from datetime import timedelta
from celery import shared_task
import time


@shared_task
def weekly_digest():
    week_ago = timezone.now() - timedelta(weeks=1)

    categories = Category.objects.prefetch_related('subscribers')
    new_posts = Post.objects.filter(add_time__gt=week_ago).select_related('category')

    for category in categories:
        category_new_posts = new_posts.filter(category=category)
        if category_new_posts:
            messages = []
            for subscriber in category.subscribers.all():
                message = (
                    "Weekly digest",
                    f"News posts in {category.category_title}:\n" +
                    "\n".join([f"{post.title}: {post.get_absolute_url()}" for post in category_new_posts]),
                    'spartak_pvl@mail.ru',
                    [subscriber.email],
                )
                messages.append(message)

            send_mass_mail(messages)


@shared_task
def notify_subscribers(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return
    categories = post.category.all()
    for category in categories:
        for subscriber in category.subscribers.all():
            send_mail(
                subject=f"Новая статья в категории {category.category_title}",
                message=f"Проверьте новую статью: {post.title}. {post.content[:50]}... Прочитать статью можно по ссылке: {post.get_absolute_url()}",
                from_email='spartak_pvl@mail.ru',
                recipient_list=[subscriber.email],
                fail_silently=False,
            )