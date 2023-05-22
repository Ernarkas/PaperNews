from django.urls import path
from .views import ArticleCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='article_delete'),
]