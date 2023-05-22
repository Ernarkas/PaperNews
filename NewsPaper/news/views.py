from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .forms import NewsSearchForm, PostForm
from .models import Post, Category
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mass_mail
import logging


class NewsListView(ListView):
    model = Post
    ordering = ['-id']
    template_name = 'news_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_author = self.request.user.groups.filter(name='authors').exists()
        context['is_author'] = is_author
        return context


class NewsDetailView(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'


def search_news(request):
    queryset = Post.objects.all()
    form = NewsSearchForm(request.GET)

    if form.is_valid():
        title = form.cleaned_data['title']
        author_name = form.cleaned_data['author_name']
        date_after = form.cleaned_data['date_after']

        if title:
            queryset = queryset.filter(title__icontains=title)

        if author_name:
            queryset = queryset.filter(author__user__username__icontains=author_name)

        if date_after:
            queryset = queryset.filter(add_time__gt=date_after)

    context = {
        'form': form,
        'posts': queryset,
    }

    return render(request, 'news_search.html', context)


class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'
    success_url = reverse_lazy('news_list')

    def send_notifications(self, post, categories):
        logger = logging.getLogger(__name__)

        messages = []

        for category in categories:
            print(f"Post {post.id} is in category {category.category_title}")
            subscribers = category.subscribers.all()

            if not subscribers:
                logger.info(f"No subscribers for category {category.category_title}")
                continue

            for subscriber in subscribers:
                logger.info(f"Processing subscriber {subscriber.username}")
                subject = f"Hello, {subscriber.username}. New article in your favorite section!"
                message = f"{post.title}\n{post.content[:50]}..."
                email = (subject, message, 'spartak_pvl@mail.ru', [subscriber.email])
                messages.append(email)

                logger.info(f"Preparing to send notification to {subscriber.email}")

        if messages:
            result = send_mass_mail(messages, fail_silently=False)
            logger.info(f"Notification send result: {result}")
        else:
            logger.info("No messages to send.")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind = 'новость'
        post.save()  # save the post before sending notifications
        categories_ids = self.request.POST.getlist('category') # get categories from request
        categories = Category.objects.filter(id__in=categories_ids) # get categories instances
        self.send_notifications(post, categories)  # add this line
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ArticleCreateView(NewsCreateView):


    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind = 'статья'
        return super(NewsCreateView, self).form_valid(form)

class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(DetailView):
    model = Post
    success_url = reverse_lazy('news_list')
    template_name = 'post_confirm_delete.html'


@login_required
def become_author(request):
    author_group = Group.objects.get_or_create(name='authors')[0]
    request.user.groups.add(author_group)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def toggle_subscription(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.user in category.subscribers.all():
        category.subscribers.remove(request.user)
    else:
        category.subscribers.add(request.user)
    return redirect('category_views', pk=category_id)



class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

class CategoryListView(ListView):
    model = Category
    template_name = 'categories_list.html'  # замените на путь к вашему фактическому шаблону
    context_object_name = 'categories'