from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30) #제목
    content = models.TextField()   #내용

    head_image = models.ImageField(upload_to='blog/%Y%m%d/', blank=True)

    created = models.DateTimeField()  #작성 날,시간

    author = models.ForeignKey(User, on_delete=models.CASCADE)  #글 저자
#장고는 admin 페이지를 자동으로 만든다.


    def __str__(self):
        return '{} :: {}'.format(self.title, self.author)
