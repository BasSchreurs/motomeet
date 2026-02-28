#meetings/urls.py
from django.urls import path
from .views import meetup_list, meetup_detail, meetup_join, meetup_leave, delete_comment, create_meetup, edit_meetup, delete_meetup

urlpatterns = [
    path('', meetup_list, name='meetup_list'),
    path('meetups/aanmaken/', create_meetup, name='create_meetup'),
    path('meetups/<slug:slug>/', meetup_detail, name='meetup_detail'),
    path('meetups/<slug:slug>/join/', meetup_join, name='meetup_join'),
    path('meetups/<slug:slug>/leave/', meetup_leave, name='meetup_leave'),
    path('meetups/<slug:slug>/bewerken/', edit_meetup, name='edit_meetup'),
    path('meetups/<slug:slug>/verwijderen/', delete_meetup, name='delete_meetup'),
    path('reactie/<int:comment_id>/verwijderen/', delete_comment, name='delete_comment'),
    path('meetups/aanmaken/', create_meetup, name='create_meetup'),
]