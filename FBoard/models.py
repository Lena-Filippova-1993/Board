from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import TextField
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    CATEGORIES = (
        ('healers', 'Хилы'),
        ('tanks', 'Танки'),
        ('dd', 'ДД'),
        ('dealers', 'Торговцы'),
        ('gildmasters', 'Гилдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potionsmakers', 'Зельевары'),
        ('spell_masters', 'Мастера заклинаний')
    )
    category = models.CharField(max_length=25, choices=CATEGORIES, verbose_name='Категория', default='healers')
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, verbose_name='Названиe', default='Введите заголовок...')
    content = RichTextUploadingField(verbose_name='Текст объявления', default='Вводите текст сюда...')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = TextField(verbose_name='Отклик', default='')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    dateCreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} Отзыв {self.text} от {self.author}'

    def get_absolute_url(self):
        return reverse(viewname='post_detail', kwargs={'pk':self.post_id})
