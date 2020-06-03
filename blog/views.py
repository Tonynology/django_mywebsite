from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView

class PostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()   #filter()는 특정조건에 해당할때

        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()   #filter()는 특정조건에 해당할때

        return context

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