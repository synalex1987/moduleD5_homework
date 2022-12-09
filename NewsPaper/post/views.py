from datetime import datetime
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post
from .filters import PostFilter
from .forms import PostForm


# Класс для отображения всех постов/новостей
class PostList(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'post_list'
    ordering = ['-time']

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['total'] = Post.objects.all().count
        return context


# Класс для отображения детальной информации о поста/новости на отдельной странице
class PostDetail(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    #template_name = 'post/post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


# Класс для отображения постов/новостей по фильтру.
class PostListFiltered(ListView):
    model = Post
    template_name = 'post/search.html'
    context_object_name = 'post_list_filtered'
    ordering = ['-time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'post/post_create.html'
    permission_required = ('post.add_post',)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = 'post/post_create.html'
    permission_required = ('post.change_post',)

    def get_object(self, **kwargs):
        return Post.objects.get(pk=self.kwargs.get('pk'))
    
    
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'post/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('post.delete_post',)
    


# TEST TEST TEST
# Класс для отображения ВСЕХ постов/новостей, а также по фильтру. Для тестирования
class PostListWithFilters(ListView):
    model = Post
    template_name = 'post/test/post_list_with_query.html'
    context_object_name = 'post_list_with_query'
    ordering = ['-time']
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['total'] = Post.objects.all().count
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)
