# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from .models import *
#
#
# @receiver(post_save, sender=Response)
# def response_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__post=instance.post
#     ).values_list('email', flat=True)
#
#     subject = f'Новый отзыв...'
#
#     text_content = (
#         f'Отзыв: {instance.text} от {instance.author} к объявлению {instance.post}\n'
#         f'Ссылка на товар: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Отзыв: {instance.text} от {instance.author} к объявлению {instance.post}<br>'
#         f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#         f'Ссылка на объявление</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()