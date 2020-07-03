from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
# from ckeditor.fields import RichTextField

from ckeditor_uploader.fields import RichTextUploadingField

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

class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/blog/tag/{}/'.format(self.slug)

class Post(models.Model):
    title = models.CharField(max_length=30) #제목
    # content = MarkdownxField()   #내용
    # content = RichTextField()  # 내용
    content = RichTextUploadingField(blank = True, null=True)  # 내용
    content2 = RichTextUploadingField(blank = True, null=True, config_name='special')  # 내용

    head_image = models.ImageField(upload_to='blog/%Y%m%d/', blank=True)

    created = models.DateTimeField(auto_now=True)  #작성 날,시간

    author = models.ForeignKey(User, on_delete=models.CASCADE)  #글 저자

    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    tags = models.ManyToManyField(Tag, blank=True) #require가 아닌 목록은 blank 해야함

    class Meta:
        ordering = ['-created']
#장고는 admin 페이지를 자동으로 만든다.


    def __str__(self):
        return '{} :: {}'.format(self.title, self.author)

    def get_absolute_url(self):
        return '/blog/{}/'.format(self.pk)

    def get_update_url(self):
        return self.get_absolute_url() + 'update/'

    def get_markdown_content(self):
        return markdown(self.content)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # ForeignKey = 다 대 일 구조
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_markdown_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return self.post.get_absolute_url() + '#comment-id-{}'.format(self.pk)