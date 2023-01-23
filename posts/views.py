from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'posts': post_list, 'page': page, 'paginator': paginator})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.select_related('author').filter(author__username=user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'posts': post_list, 'username': username, 'page': page, 'paginator': paginator})


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    count = Post.objects.select_related('author').filter(author__username=username).count()
    return render(request, 'post.html', {'post': post, 'username': username, 'count': count})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'new_post.html', {'form': form})
    else:
        form = PostForm()
        return render(request, 'new_post.html', {'form': form})


@login_required
def post_edit(request, username, post_id):
    is_edit = True
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        form = PostForm(request.POST, instance=post)
        user = request.user.username
        author_posts = Post.objects.select_related('author')\
            .filter(author__username=user).values_list('id', flat=True)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print(len(author_posts))
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        if form.is_valid() and post_id in author_posts:
            post.save()
            return redirect('index')
        return render(request, 'new_post.html', {'form': form, 'is_edit': is_edit})
    else:
        form = PostForm()
        return render(request, 'new_post.html', {'form': form, 'is_edit': is_edit})
