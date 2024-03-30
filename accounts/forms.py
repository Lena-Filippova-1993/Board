from django import forms
from allauth.account.forms import SignupForm
from django.core.mail import send_mail
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        send_mail(
            subject='Добро пожаловать!',
            message=f'Дорогой(-ая) {user.username} Вы успешно зарегистрировались на сайте!',
            from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
        )
        return user

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )
class FormCode(forms.Form):
    code = forms.IntegerField(label="Код регистрации")