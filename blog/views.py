from django.utils import timezone
from  django.shortcuts import render, get_object_or_404 ,redirect
from .forms import  * 
from .models import *
from django.contrib.auth import login 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm , authenticate
from collections import Counter
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views import View

def post_list(request, category_slug=None):
    posts = Post.objects.all().order_by('published_date')
   # categories = Category.objects.all()

  #  if category_slug:
   #     category = get_object_or_404(Category, slug=category_slug)
    #    posts = posts.filter(category=category)

    return render(request, 'blog/post_list.html', {'posts': posts, })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post, parent_comment=None)
    comment_form = CommentForm()
    reply_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.created_date = timezone.now()
            parent_comment_id = request.POST.get('parent_comment_id')

            if parent_comment_id:
                parent_comment = get_object_or_404(Comment, id=parent_comment_id)
                comment.parent_comment = parent_comment

            comment.save()
            return redirect('post_detail', slug=post.slug)

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'reply_form': reply_form})



def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES,)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_list')
        
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

 

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

def category_post(request, slug):
    category = Post.objects.filter(category__slug = slug)
    print(category)
    return render(request, 'blog/post_list.html', {'posts': category})
 
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag_list.html', {'tags': tags})

def tag_post(request, slug):
    tag = Post.objects.filter(tags__slug = Tag.objects.filter(slug=slug).last().slug)
    
    return render(request,'blog/post_list.html', {'posts': tag})
  
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')  
        else:
            user=form.get_email()
            login(request,user)
            return redirect('post_list')
    else:
        form = LoginForm()
    return render(request, 'blog/user_login.html', {'form': form})

def user_logout(request):
    logout(request)
    
    return redirect('post_list' )

def user_detail(request, user_id):
    print(user_id)
    print("---------")
    user = get_object_or_404(User,request.FILES, id=user_id,)
    
    
    return render(request, 'blog/user_detail.html', {'user': user})

def edit_profile(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = EditProfileForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

            messages.success(request, 'Your profile was successfully updated.')
            return redirect('user_detail', user_id=user.id)  
        else:
            messages.error(request, 'There was an error updating your profile. Please correct the errors below.')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'blog/edit_profile.html', {'user': user, 'form': form})

