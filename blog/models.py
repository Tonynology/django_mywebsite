from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)

    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/blog/category/{}/'.format(self.slug)

    class Meta:
        verbose_name_plural = 'categories'

class Post(models.Model):
    title = models.CharField(max_length=30) #제목
    content = models.TextField()   #내용

    head_image = models.ImageField(upload_to='blog/%Y%m%d/', blank=True)

    created = models.DateTimeField()  #작성 날,시간

    author = models.ForeignKey(User, on_delete=models.CASCADE)  #글 저자

    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

#장고는 admin 페이지를 자동으로 만든다.


    def __str__(self):
        return '{} :: {}'.format(self.title, self.author)

    def get_absolute_url(self):
        return '/blog/{}/'.format(self.pk)


