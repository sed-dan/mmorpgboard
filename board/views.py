from django.conf import settings
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.models import User
from .models import Post, Response
from .forms import PostForm, ResponseForm
from .filters import ResponseFilter
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'board/post_list.html'
    ordering = ['-created_at']
    paginate_by = 10


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        post.save()
        return redirect(f'/post/{post.id}/')

class PostEditView(LoginRequiredMixin, UpdateView):
    template_name = 'board/post_edit.html'
    form_class = PostForm
    success_url = '/create/'

    def dispatch(self, request, *args, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/post/' + str(self.kwargs.get('pk')))

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'board/post_detail.html'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.resp_author = request.user
            response.resp_post = post
            response.save()
            html_content = (
                    f'<p>Здравствуйте, <strong>{post.author.username}</strong>!</p>\n'
                    f'<p>На Ваше объявление был оставлен отклик. Вы можете <strong>принять</strong> его или <strong>удалить</strong>.</p>\n'
                    f'<a href="{settings.SITE_URL}/responses/">посмотреть</a>'
            )
            send_mail(
                subject='Новый отклик',
                message='На Ваше объявление был оставлен отклик',
                html_message=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[post.author.email]
            )
            return redirect('post_detail', pk=post.pk)
        return redirect('post_detail', pk=post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResponseForm()
        return context

class ResponsesView(LoginRequiredMixin, ListView):
    model = Response
    context_object_name = 'comments'
    template_name = 'board/responses.html'
    filterset_class = ResponseFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        qs = queryset.filter(resp_post__author=self.request.user)
        self.filter = ResponseFilter(self.request.GET, queryset=qs, request=self.request.user)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

def confirm_comment(request, resp_id):
    comment = Response.objects.get(id=resp_id)
    comment.status = True
    comment.save()
    html_content = (
        f'<p>Здравствуйте, <strong>{comment.resp_author.username}</strong>!</p>\n'
        f'<p>Ваш отклик <strong>был принят</strong> автором объявления!</p>\n'
        f'<a href="{settings.SITE_URL}/post/{comment.resp_post.id}/">посмотреть</a>'
    )
    send_mail(
        subject='Изменение статуса отклика',
        message=(
            f'Ваш отклик был принят автором объявления!'
        ),
        html_message=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[comment.resp_author.email]
    )
    return redirect('responses')


def delete_comment(request, resp_id):
    Response.objects.get(id=resp_id).delete()
    return redirect('responses')