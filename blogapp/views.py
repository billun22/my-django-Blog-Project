from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from .models import Article, Comment
from .forms import AritcleForm, CommentForm, CreateUserForm

# Create your views here.
def register(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created sucessfully. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "error")
    
    context  = {'form': form, }
    return render(request, 'register.html', context)

def login(request):
    form = AuthenticationForm()
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"hello, {user.username}!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password")
    
    context  = {'form': form}
    return render(request, 'login.html', context)

def log_out(request):
    logout(request)
    return redirect('index')


def index(request):
    articles = Article.objects.all().order_by('-publish_date')
    query = request.GET.get('search', '')
    
    if query:
        articles = Article.objects.filter(title__icontains=query)
    else:
        articles = Article.objects.all().order_by('-publish_date')
        
    context = {'articles': articles, 'query': query}
    return render(request, 'index.html', context)

@login_required
def create_post(request):
    
    if request.method == "POST":
        form = AritcleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.publisher = request.user
            article.save()
            return redirect('index')
    else:
        form = AritcleForm()
        
    context = {'form': form}    
    return render(request, 'create_post.html', context)


def post_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.filter(parent__isnull=True)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid(): 
                parent_id = request.POST.get("parent_id")
                parent = None
                if parent_id:
                    try:
                        parent = Comment.objects.get(id=parent_id)  
                    except Comment.DoesNotExist:
                        parent = None  

                comment = form.save(commit=False)
                comment.article = article
                comment.user = request.user
                comment.parent = parent
                comment.save()
                return redirect('post_detail', slug=article.slug)
        return redirect('login')
    else:
        form = CommentForm()

    context = {'article': article, 'comments': comments, 'form': form}
    return render(request, 'post_detail.html', context)

@login_required
def edit_blog(request, slug):
    
    article = get_object_or_404(Article, slug=slug)
    
    if article.publisher != request.user:
        return HttpResponseForbidden("You are not alowed to edit this post!")
    
    if request.method == 'POST':
        form = AritcleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully")
            
            return redirect('post_detail', slug=article.slug)
    
    else:
        form = AritcleForm(instance=article)
        
    context = {'form': form}
    return render(request, 'edit_blog.html', context )
        
@login_required
def delete_blog(request, slug):
    article =  get_object_or_404(Article, slug=slug)
    if request.method =='POST':
        article.delete()
        messages.warning(request, "Post deleted sucessfully")
        return redirect('index')
    
    context = {'article': article}
    return render(request, 'delete_blog.html', context)