from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from .forms import RegisterForm, PostForm, CommentForm
from .models import Post, Category, Comment

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {
        'form': form
    })


@login_required
def profile_view(request):
    posts = request.user.posts.all()

    return render(request, 'blog/profile.html', {
        'posts': posts
    })

@login_required
def my_posts(request):
    posts = request.user.posts.all().order_by('-created_at')

    return render(request, 'blog/my_posts.html', {
        'posts': posts
    })

def post_list(request):
    posts = Post.objects.filter(
        status='published'
    ).select_related(
        'author',
        'category'
    ).order_by('-created_at')

    search = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    if search:
        posts = posts.filter(
            Q(title__icontains=search)
        )

    if category_slug:
        posts = posts.filter(
            category__slug=category_slug
        )

    categories = Category.objects.all().order_by('name')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {
        'posts': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'search': search,
        'category_slug': category_slug,
    })

def post_detail(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status='published'
    )

    comments = post.comments.all().order_by('created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            return redirect(
                'post_detail',
                slug=post.slug
            )
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required
def post_create(request):

    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect(
                'post_detail',
                slug=post.slug
            )

    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {
        'form': form,
        'title': 'Create Post'
    })


@login_required
def post_edit(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    # Ownership check
    if post.author != request.user:
        return HttpResponseForbidden(
            "You are not allowed to edit this post."
        )

    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():
            form.save()

            return redirect(
                'post_detail',
                slug=post.slug
            )

    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {
        'form': form,
        'title': 'Edit Post'
    })


@login_required
def post_delete(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    # Ownership check
    if post.author != request.user:
        return HttpResponseForbidden(
            "You are not allowed to delete this post."
        )

    if request.method == 'POST':
        post.delete()

        return redirect('post_list')

    return render(request, 'blog/post_confirm_delete.html', {
        'post': post
    })

@login_required
def comment_delete(request, pk):

    comment = get_object_or_404(
        Comment,
        pk=pk
    )

    if comment.user != request.user:
        return HttpResponseForbidden(
            "You are not allowed to delete this comment."
        )

    if request.method == 'POST':
        post_slug = comment.post.slug
        comment.delete()

        return redirect(
            'post_detail',
            slug=post_slug
        )

    return HttpResponseForbidden(
        "Invalid request."
    )