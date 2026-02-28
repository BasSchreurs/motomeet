from django.shortcuts import render, get_object_or_404
from .models import Article

def article_list(request):
    articles = Article.objects.all().order_by('-published_at')
    return render(request, "news/article_list_page.html", {
        'articles': articles
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, "news/article_detail.html", {
        'article': article
    })