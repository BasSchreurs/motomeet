from django.urls import path
from .views import article_detail, article_list

urlpatterns = [
    path('', article_list, name='article_list'),            # /news/
    path('<slug:slug>/', article_detail, name='article_detail'),  # /news/some-article/
]