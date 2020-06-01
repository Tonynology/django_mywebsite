from django.shortcuts import render
from .models import Post
# Create your views here.


def index(request):
    posts = Post.objects.all() #장고에서 기본적으로 제공한다.

    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
        }
    )