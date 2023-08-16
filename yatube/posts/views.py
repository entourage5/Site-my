from django.shortcuts import render, get_object_or_404, redirect
from posts.models import Post, Group, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from posts.forms import PostForm


def index(request):
    template_name = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'title': 'Главная',
        'page_obj': page_obj
    }
    return render(request, template_name, context)


def group_posts(request, slug):
    template_name = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:5]
    context = {
        'title': 'Здесь будет информация o группах проекта Yatube',
        'posts': posts,
        'group': group,
    }
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, template_name, context)


def profile(request, username):
    template_name = 'posts/profile.html'
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user)
    paginator = Paginator(user_posts, 5)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'author': user,
        'page_obj': page_obj,
    }
    return render(request, template_name, context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author.username)
        else:
            return render(request, 'posts/create_post.html', {'form': form})
    else:
        form = PostForm()
        return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST, instance=post)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form, 'post_id': post_id, 'is_edit': True})
    form.save()
    return redirect('posts:post_detail', post_id=post_id)
