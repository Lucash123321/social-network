from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User, Comment, Follow
from .forms import PostForm, CommentForm


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'group': group, 'page_obj': page_obj}
    return render(request, 'posts/group_posts.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.select_related('author').filter(author__username=user).order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_count = post_list.count()
    author = User.objects.get(username=username)

    if request.user.is_authenticated:
        following = Follow.objects.filter(author=author, user=request.user).exists()
    else:
        following = False

    if username == request.user.username:
        is_author = True
    else:
        is_author = False

    context = {
        'username': username,
        'page_obj': page_obj,
        'posts_count': posts_count,
        'following': following,
        'is_author': is_author
    }
    return render(request, 'posts/profile.html', context)


def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    posts_count = Post.objects.select_related('author').filter(author__username=post.author.username).count()
    form = CommentForm()
    comments = Comment.objects.filter(post=post)
    followers = Follow.objects.filter(author=post.author.id).count()
    following = Follow.objects.filter(user=request.user.id).count()
    context = {'post': post,
               'posts_count': posts_count,
               'form': form,
               'comments': comments,
               'followers': followers,
               'following': following}
    return render(request, 'posts/view_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('posts:view_post', post_id=post_id)
        return redirect('posts:view_post', post_id=post_id)
    return redirect('posts:view_post', post_id=post_id)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid() and post.author == request.user:
            post.save()
            return redirect('posts:view_post', post_id=post_id)
        return redirect('posts:view_post', post_id=post_id)
    is_edit = True
    context = {'form': form, 'is_edit': is_edit}
    return render(request, 'posts/create_post.html', context)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    username = get_object_or_404(User, username=username)
    author = User.objects.get(username=username)
    already_following = Follow.objects.filter(author=author, user=request.user).exists()
    if request.user != username and not already_following:
        Follow.objects.create(author=username, user=request.user)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(author=author, user=request.user).delete()
    return redirect('posts:profile', username=username)
