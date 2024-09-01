from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Category

def forum_home(request):
    categories = Category.objects.all()
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'forum/home.html', {'posts': posts, 'categories': categories})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
            )
            comment.save()
            return redirect('post_detail', pk=post.pk)

    return render(request, 'forum/post_detail.html', {'post': post, 'comments': comments})

@login_required
def new_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')

        if title and content and category_id:
            category = get_object_or_404(Category, pk=category_id)
            post = Post.objects.create(
                title=title,
                content=content,
                author=request.user,
                category=category,
            )
            post.save()
            return redirect('forum_home')

    categories = Category.objects.all()
    return render(request, 'forum/new_post.html', {'categories': categories})