from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Q
from .models import Meetup, Comment
from .forms import CommentForm, MeetupForm

def meetup_list(request):
    # Only show public meetups on the list page
    meetups = Meetup.objects.filter(
        start_date__gte=timezone.now(),
        is_public=True
    ).order_by('start_date')
    return render(request, "meetups/meetup_list_page.html", {"meetups": meetups})

def meetup_detail(request, slug):
    meetup = get_object_or_404(Meetup, slug=slug)
    
    # Check if user can view this meetup
    can_view = (
        meetup.is_public or 
        meetup.created_by == request.user or
        (request.user.is_authenticated and request.user in meetup.invited_friends.all()) or
        (request.user.is_authenticated and meetup.attendees.filter(pk=request.user.pk).exists())
    )
    
    if not can_view:
        return redirect('meetup_list')
    
    is_attending = request.user.is_authenticated and meetup.attendees.filter(pk=request.user.pk).exists()
    is_invited = request.user.is_authenticated and request.user in meetup.invited_friends.all()
    comments = meetup.comments.select_related('author').all()
    form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.meetup = meetup
            comment.author = request.user
            comment.save()
            return redirect(reverse('meetup_detail', kwargs={'slug': slug}) + '#comments-section')

    return render(request, "meetups/meetup_detail.html", {
        "meetup": meetup,
        "is_attending": is_attending,
        "is_invited": is_invited,
        "comments": comments,
        "form": form,
    })

@login_required
def meetup_join(request, slug):
    meetup = get_object_or_404(Meetup, slug=slug)
    
    can_join = (
        meetup.is_public or 
        meetup.created_by == request.user or
        request.user in meetup.invited_friends.all()
    )
    
    if can_join:
        meetup.attendees.add(request.user)
    
    return redirect(reverse('meetup_detail', args=[slug]) + '#comments-section')

@login_required
def meetup_leave(request, slug):
    meetup = get_object_or_404(Meetup, slug=slug)
    meetup.attendees.remove(request.user)
    referer = request.META.get('HTTP_REFERER', '')
    if 'profile' in referer:
        return redirect('profile', username=request.user.username)
    return redirect(reverse('meetup_detail', args=[slug]) + '#comments-section')


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    slug = comment.meetup.slug
    if comment.author == request.user:
        comment.delete()
    return redirect(reverse('meetup_detail', kwargs={'slug': slug}) + '#comments-section')

@login_required
def create_meetup(request):
    form = MeetupForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        meetup = form.save(commit=False)
        meetup.created_by = request.user
        meetup.slug = slugify(form.cleaned_data['title'])
        meetup.save()
        
        # Save the many-to-many relationship for invited_friends
        form.save_m2m()
        
        # Automatically add the creator as an attendee
        meetup.attendees.add(request.user)
        
        return redirect('meetup_detail', slug=meetup.slug)
    return render(request, 'meetups/create_meetup.html', {'form': form})

@login_required
def edit_meetup(request, slug):
    meetup = get_object_or_404(Meetup, slug=slug)
    if meetup.created_by != request.user:
        return redirect('meetup_detail', slug=slug)
    form = MeetupForm(request.POST or None, request.FILES or None, instance=meetup, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('meetup_detail', slug=meetup.slug)
    return render(request, 'meetups/edit_meetup.html', {'form': form, 'meetup': meetup})

@login_required
def delete_meetup(request, slug):
    meetup = get_object_or_404(Meetup, slug=slug)
    if meetup.created_by != request.user:
        return redirect('meetup_detail', slug=slug)
    if request.method == 'POST':
        meetup.delete()
        return redirect('meetup_list')
    return render(request, 'meetups/delete_meetup.html', {'meetup': meetup})