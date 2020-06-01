from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView

class PostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-created')


class PostDetail(DetailView):
    model = Post

    # def post_detail(request, pk):
    #     blog_post = Post.objects.get(pk=pk)  #하나만 가져올땐 get을 쓴다.
    #
    #     return render(
    #         request,
    #         'blog/post_detail.html',
    #         {
    #             'blog_post': blog_post,
    #         }
    #     )

# def index(request):
#     posts = Post.objects.all()    #장고에서 기본적으로 제공한다.
#
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )