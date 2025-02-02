from django.shortcuts import render, redirect
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class PostList(ListView):
    model = Post
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()   #filter()는 특정조건에 해당할때

        return context

class PostSearch(PostList):
    def get_queryset(self):
        q = self.kwargs['q']
        object_list = Post.objects.filter(Q(title__contains=q) | Q(content__contains=q))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostSearch, self).get_context_data()
        context['search_info'] = 'Search: "{}"'.format(self.kwargs['q'])
        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()   #filter()는 특정조건에 해당할때
        context['comment_form'] = CommentForm()

        return context

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post

    fields = [
        'title', 'content', 'head_image', 'category', 'tags'
    ]

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else:
            return redirect('/blog/')


class PostUpdate(UpdateView):
    model = Post
    fields = [
        'title', 'content', 'head_image', 'category', 'tags'
    ]


class PostListByTag(ListView):
    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        tag = Tag.objects.get(slug=tag_slug)

        return tag.post_set.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()   #filter()는 특정조건에 해당할때
        tag_slug = self.kwargs['slug']
        context['tag'] = Tag.objects.get(slug=tag_slug)

        return context

class PostListByCategory(ListView):

    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)

        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()   #filter()는 특정조건에 해당할때

        slug = self.kwargs['slug']

        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        # context['title'] = 'Blog - {}'.format(category.name)
        return context

def new_comment(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect((comment.get_absolute_url()))
    else:
        return redirect('/blog/')


# class CommentDelete(DeleteView):
#     model = Comment
#
#     def get_object(self, queryset=None):
#         comment = super(CommentDelete, self).get_object()  #super는 DeleteView에서 불러오는것
#         if comment.author != self.request.user:
#             raise PermissionError('Comment 삭제 권한이 없습니다')
#         return comment
#
#     def get_success_url(self):
#         post = self.get_object().post
#         return post.get_absolute_url() + '#comment-list'
#

class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm

    def get_object(self, queryset=None):
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')

        return comment

def delete_comment(request, pk):        # Function Based view
    comment = Comment.objects.get(pk=pk)
    post = comment.post

    if request.user == comment.author:
        post = comment.post
        comment.delete()
        return redirect(post.get_absolute_url() + '#comment-list')
    else:
        raise PermissionError('Comment 삭제 권한이 없습니다.')
        # return redirect('/blog/')



    # class CommentDelete(DeleteView):
    #     model = Comment
    #
    #     def get_object(self, queryset=None):
    #         comment = super(CommentDelete, self).get_object()  # super는 DeleteView에서 불러오는것
    #         if comment.author != self.request.user:
    #             raise PermissionError('Comment 삭제 권한이 없습니다')
    #         return comment
    #
    #     def get_success_url(self):
    #         post = self.get_object().post
    #         return post.get_absolute_url() + '#comment-list'

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