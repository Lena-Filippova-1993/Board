from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Exists, OuterRef
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters import FilterSet
from .forms import *
from .models import *


class PostList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 15





class ResponseCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    model = Response
    form_class = RespondForm
    template_name = 'post.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        post=get_object_or_404(Post, id=self.kwargs['pk'])
        response.author = self.request.user
        response.post_id = self.kwargs['pk']
        response.post=post
        response.save()
        author = User.objects.get(pk=post.author_id)
        send_mail(
            subject='Отклик на объявление',
            message=f'На объявление {post} был добавлен отклик {response.text} пользователем {self.request.user}.\n'
                    f'Прочитать отклик:\nhttp://127.0.0.1:8000/posts/{response.post.id}',
            from_email="lena-filippova-93@mail.ru",
            recipient_list=[author.email],
        )
        return super().form_valid(form)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['post_id'] = self.kwargs['pk']

class PostDetail(DetailView, ResponseCreate):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if Response.objects.filter(author_id=self.request.user.id).filter(post_id=self.kwargs.get('pk')):
    #         context['respond'] = "Responsed"
    #     elif self.request.user == Post.objects.get(pk=self.kwargs.get('pk')).author:
    #         context['respond'] = "My"
    #     return context


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('FBoard.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('FBoard.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('Вы не являетесь автором объявления...')


class PostDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('FBoard.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('Вы не являетесь автором объявления...')



class PostFilter(FilterSet):
    class Meta:
        model = Response
        fields = [
            'post',
        ]
    def __init__(self,*args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(author_id=kwargs['request'])


class Responses(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Response.objects.filter(post__author_id=self.request.user.id)
        context['filterset'] = PostFilter(self.request.GET, queryset, request=self.request.user.id)
        return context


@login_required
def response_accept(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.status = True          # меняем флаг на True
        send_mail(
            subject=f'Ваш отклик на объявление принят!',
            message=f'Здравствуйте, {response.author}! Отклик к объявлению {response.post.title} принят.\n',
            from_email='lena-filippova-93@mail.ru',
            recipient_list=[response.author.email],
        )
        response.save()
        return HttpResponseRedirect('/posts/responses')
    else:
        return HttpResponseRedirect('/accounts/login')


@login_required
def response_delete(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.delete()       # Удаляем отзыв
        return HttpResponseRedirect('/posts/responses')
    else:
        return HttpResponseRedirect('/accounts/login')

# @login_required
# @csrf_protect
# def subscriptions(request):
#     if request.method == 'POST':
#         post_id = request.POST.get('post_id')
#         post = Post.objects.get(id=post_id)
#         action = request.POST.get('action')
#
#         if action == 'subscribe':
#             Subscription.objects.create(user=request.user, post=post)
#         elif action == 'unsubscribe':
#             Subscription.objects.filter(
#                 user=request.user,
#                 post=post,
#             ).delete()
#
#     posts_with_subscriptions = Post.objects.annotate(
#         user_subscribed=Exists(
#             Subscription.objects.filter(
#                 user=request.user,
#                 post=OuterRef('pk'),
#             )
#         )
#     ).order_by('id')
#     return render(
#         request,
#         'subscriptions.html',
#         {'posts': posts_with_subscriptions},
#     )