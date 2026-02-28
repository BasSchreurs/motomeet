# meetups/admin.py
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Meetup

class MeetupAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('title', 'start_date', 'end_date')
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Meetup, MeetupAdmin)