from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import ProfileForm

User = get_user_model()


def index_view(request):
    return render(request, 'a_users/index.html')


@login_required
def profile_view(request, username=None):
    if not username:
        return redirect('profile', request.user.username)
    profile_user = get_object_or_404(User, username=username)
    
    sort_order = request.GET.get('sort', '') 
    if sort_order == 'oldest':
        profile_posts = profile_user.posts.order_by('created_at')
    elif sort_order == 'popular':
        profile_posts = profile_user.posts.annotate(num_likes=Count('likes')).order_by('-num_likes', '-created_at')
    else:
        profile_posts = profile_user.posts.order_by('-created_at')
        
    profile_posts_liked = profile_user.likedposts.all().order_by('-likedpost__created_at')
    profile_posts_bookmarked = profile_user.bookmarkedposts.all().order_by('-bookmarkedpost__created_at')
    profile_user_likes = profile_user.posts.aggregate(total_likes=Count('likes'))['total_likes']

    
    context = {
        'page': 'Profile',
        'profile_user': profile_user,
        'profile_user_likes': profile_user_likes,
        'profile_posts': profile_posts,
        'profile_posts_liked': profile_posts_liked,
        'profile_posts_bookmarked': profile_posts_bookmarked,
    }
    
    if request.GET.get('liked'):
        return render(request, 'a_users/partials/_profile_posts_liked.html', context) 
    if request.GET.get('bookmarked'):
        return render(request, 'a_users/partials/_profile_posts_bookmarked.html', context)
    if request.GET.get('sort'):
        return render(request, 'a_users/partials/_profile_posts.html', context)
    
    if request.htmx:
        return render(request, 'a_users/partials/_profile.html', context)
    return render(request, 'a_users/profile.html', context)

@login_required
def profile_edit(request):
    form = ProfileForm(instance=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)
    
    if request.htmx:
        return render(request, "a_users/partials/_profile_edit.html", {'form' : form})
    return redirect('profile', request.user.username)