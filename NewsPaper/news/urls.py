from django.urls import path

from .views import NewsListView, NewsDetailView, search_news, NewsCreateView, PostUpdateView, PostDeleteView, ArticleCreateView, become_author, CategoryDetailView, toggle_subscription, CategoryListView

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('search/', search_news, name='search_news'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),
    path('become_author', become_author, name='become_author'),
    path('category/<int:category_id>/subscribe', toggle_subscription, name='toggle_subscription'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_views'),
    path('categories/', CategoryListView.as_view(), name='categories_list'),



]
