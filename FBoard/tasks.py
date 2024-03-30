from celery import shared_task
from django.contrib.auth.models import User
from .models import Post, Response
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone


# #Отправка уведомления о принятии отклика
# @shared_task
# def respond_accept_send_email(response_id):
#     respond = Response.objects.get(id=response_id)
#     print(respond.post.author.email)
#     send_mail(
#         subject=f'Ваш отклик на объявление принят!',
#         message=f'Здравствуйте, {respond.author}! Отклик к объявлению {respond.post.title} принят.\n'
#                 f'Посмотреть принятые отклики:\nhttp://127.0.0.1:8000/posts/responses',
#         from_email='lena-filippova-93@mail.ru',
#         recipient_list=[response.author.email],
#     )


#Список объявлений за последние 7 дней

@shared_task
def send_mail_monday_8am():
    now = timezone.now()
    list_week_posts = list(Post.objects.filter(dateCreation__gte=now - timedelta(days=7)))
    if list_week_posts:
        for user in User.objects.filter():
            print(user)
            post_list = ''
            for post in list_week_posts:
                post_list += f'\n{post.title}\nhttp://127.0.0.1:8000/post/{post.id}'
            send_mail(
                subject=f'Новые объявления за прошедшую неделю.',
                message=f'Здравствуйте, {user.username}!\n Ознакомьтесь с новыми объявлениями на нашем сайте, '
                        f'появившимися за прошедшую неделю:\n{post_list}',
                from_email='lena-filippova-93@mail.ru',
                recipient_list=[user.email],
            )