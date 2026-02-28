from django.contrib import admin
from .models import Article
from django_summernote.admin import SummernoteModelAdmin

class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'published_at')
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ('content',)

admin.site.register(Article, ArticleAdmin)