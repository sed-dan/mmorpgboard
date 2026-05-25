from django import forms
from .models import Post, Response
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(label='', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['category', 'title', 'content']
        labels = {'category': 'Категория',
                  'title': 'Заголовок'
                  }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['resp_content']
        widgets = {
            'resp_content': forms.Textarea(attrs={
                'rows': 1,
                'class': 'form-control form-control-sm',
                'placeholder': 'Отклик',
                'maxlength': 100
            }),
        }
        labels = {'resp_content': ''}
