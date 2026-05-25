from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from .resources import CATEGORIES


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORIES)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Response(models.Model):
   resp_date = models.DateTimeField(auto_now_add=True)
   resp_content = models.CharField(max_length = 100)
   resp_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='responses')
   resp_author = models.ForeignKey(User, on_delete=models.CASCADE)
   status = models.BooleanField(default=False)
