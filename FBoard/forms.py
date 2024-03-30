from django import forms
from .models import *

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'category',
            'title',
            'content',
        )



class RespondForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        labels = {
            'text':'Введите текст отклика:'
        }
        widgets = {
            'text':forms.Textarea(attrs={'class':'form-text', 'cols': 100, 'rows': 1})
        }