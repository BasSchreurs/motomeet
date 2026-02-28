from django.shortcuts import render
from django.contrib.auth.models import User
from news.models import Article
from meetups.models import Meetup
from django.utils import timezone

def home(request):
    articles = Article.objects.all().order_by('-published_at')[:20]
    
    # Only show public meetups on homepage
    meetups = Meetup.objects.filter(
        start_date__gte=timezone.now(),
        is_public=True
    ).order_by('start_date')[:20]

    return render(request, "core/home.html", {
        'articles': articles,
        'meetups': meetups,
    })

def search_results(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')

    users = []
    articles = []
    meetups = []

    if query:
        if search_type == "users" or search_type == "all":
            users = User.objects.filter(username__icontains=query)
        
        if search_type == "articles" or search_type == "all":
            articles = Article.objects.filter(title__icontains=query).order_by('-published_at')
        
        if search_type == "meetups" or search_type == "all":
            # Only show public meetups in search results
            meetups = Meetup.objects.filter(
                title__icontains=query,
                start_date__gte=timezone.now(),
                is_public=True
            ).order_by('start_date')

    return render(request, "core/search_results.html", {
        'query': query,
        'search_type': search_type,
        'users': users,
        'articles': articles,
        'meetups': meetups,
    })

def info(request):
    return render(request, 'core/info.html')