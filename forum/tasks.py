from __future__ import absolute_import, unicode_literals

from forum.models import Post
from users.models import User
from celery.utils.log import get_task_logger
from django.utils import timezone


# from acebc.celery import periodic_task, shared_task
from django.core.mail import send_mail
from acebc.settings import EMAIL_HOST_USER
from celery import shared_task
from datetime import date
from dateutil.relativedelta import relativedelta
from smtplib import SMTPException


logger = get_task_logger(__name__)

def get_recent_posts(user_group_name):
    # Calculate the datetime for one month ago
    now = timezone.now()
    one_month_ago = now - relativedelta(months=1)
    first_day_of_last_month = one_month_ago.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_of_current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Query for all posts created within the last month and belong to the specified user group
    recent_posts = Post.objects.filter(
        date_time__gte=first_day_of_last_month, 
        date_time__lt=first_day_of_current_month,
        usergroup=user_group_name
    )
    return recent_posts

def get_admins_posts():
    # Calculate the datetime for one month ago
    now = timezone.now()
    one_month_ago = now - relativedelta(months=1)
    first_day_of_last_month = one_month_ago.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_of_current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Query for all posts created within the last month and belong to the specified user group
    recent_posts = Post.objects.filter(
        date_time__gte=first_day_of_last_month, 
        date_time__lt=first_day_of_current_month,
        usergroup="admin"
    )
    return recent_posts

def send_subscription_emails(user):
    # Get the user group name
    user_group = user.groups.first()
    if user_group is None:
        logger.info(f"No user group found for user {user.email}")
        return
    user_group_name = user_group.name if user_group else None
    # Get the recent posts for the user's group
    posts = get_recent_posts(user_group_name)
    admins_posts = get_admins_posts()
    all_posts = admins_posts.union(posts)
    if not all_posts:
        logger.info(f"No new admin posts and no new posts found for user {user.email} in group {user_group_name}")
        return

    last_month = date.today().replace(day=1) - relativedelta(months=1)
    subject = f"COPE: Latest posts in {last_month.strftime('%B %Y')}"

    # Prepare the message
    intro_line = (
        "Some of the recent posts that you may have missed from last month:\n\n"
    )

    message = intro_line + "\n".join(
        [
            f"Author: {post.username}\nTitle: {post.title}\n----------\n"
            for post in all_posts
        ]
    )

    # Add website URL at the end
    message += "\nVisit our website to engage or unsubscribe: https://www.copebc.com/"
    # Send the email to each subscribed user
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        logger.info(f"Email Sent to {user.email}")
    except SMTPException as e:
        logger.error(f'Email Failed to send to {user.email} due to SMTP error: {e}')
    
    except Exception as e:
        logger.error(f'Email Failed to send to {user.email}. Error: {e}')



@shared_task(name='send_monthly_emails')
def send_monthly_emails():
    # Get all subscribed users
    subscribed_users = User.objects.filter(is_subscribed=True).iterator()

    for user in subscribed_users:
        send_subscription_emails(user)
