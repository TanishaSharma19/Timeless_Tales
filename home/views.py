from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, BlogPostForm
from django.views.generic import UpdateView
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse

# Create your views here.

def home(request):
    # Landing page (do not show blogs directly on homepage)
    top_blogs = BlogPost.objects.filter(status='published').order_by('-views')[:3]
    return render(request, "home_landing.html", {'top_blogs': top_blogs})


def blogs(request):
    posts = BlogPost.objects.filter(status='published').order_by('-dateTime')
    top_blogs = BlogPost.objects.filter(status='published').order_by('-views')[:5]
    categories = Category.objects.all()
    return render(request, "blog.html", {'posts': posts, 'top_blogs': top_blogs, 'categories': categories})

def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    if not post:
        return redirect('blogs')
    # Only show draft to author
    if post.status == 'draft' and (not request.user.is_authenticated or request.user != post.author):
        return redirect('blogs')
    if post.status == 'published':
        post.views += 1
        post.save(update_fields=['views'])
    comments = Comment.objects.filter(blog=post)
    if request.method == "POST":
        user = request.user
        content = request.POST.get('content', '')
        if content and user.is_authenticated:
            Comment(user=user, content=content, blog=post).save()
    return render(request, "blog_comments.html", {'post': post, 'comments': comments})

def Delete_Blog_Post(request, slug):
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        posts.delete()
        return redirect('/blogs/')
    return render(request, 'delete_blog_post.html', {'posts':posts})

def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '').strip()
        if searched:
            from django.db.models import Q
            blogs = BlogPost.objects.filter(
                status='published'
            ).filter(
                Q(title__icontains=searched) | Q(content__icontains=searched)
            ).order_by('-dateTime')
        else:
            blogs = BlogPost.objects.none()
        return render(request, "search.html", {'searched': searched, 'blogs': blogs})
    return render(request, "search.html", {})

@login_required(login_url = '/login')
def add_blogs(request):
    if request.method=="POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            form.save_m2m()
            obj = form.instance
            alert = True
            return render(request, "add_blogs.html", {'obj': obj, 'alert': alert})
    else:
        form=BlogPostForm()
    return render(request, "add_blogs.html", {'form':form})

class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'edit_blog_post.html'
    fields = ['title', 'slug', 'content', 'image', 'status', 'category', 'tags']


def like_blog(request, slug):
    if request.method != 'POST' or not request.user.is_authenticated:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    post = BlogPost.objects.filter(slug=slug).first()
    if not post:
        return JsonResponse({'error': 'Not found'}, status=404)
    post.likes += 1
    post.save(update_fields=['likes'])
    return JsonResponse({'likes': post.likes})

@login_required(login_url='/login')
def writer_dashboard(request):
    my_posts = BlogPost.objects.filter(author=request.user)
    total_blogs = my_posts.count()
    stats = my_posts.aggregate(
        total_views=Sum('views'),
        total_likes=Sum('likes')
    )
    total_views = stats['total_views'] or 0
    total_likes = stats['total_likes'] or 0
    most_viewed = my_posts.order_by('-views').first()
    return render(request, "writer_dashboard.html", {
        'total_blogs': total_blogs,
        'total_views': total_views,
        'total_likes': total_likes,
        'most_viewed': most_viewed,
        'my_posts': my_posts.order_by('-dateTime')[:10],
    })

def category_filter(request, slug):
    cat = Category.objects.filter(slug=slug).first()
    if not cat:
        return redirect('home')
    posts = BlogPost.objects.filter(status='published', category=cat).order_by('-dateTime')
    return render(request, "blog.html", {
        'posts': posts,
        'top_blogs': BlogPost.objects.filter(status='published').order_by('-views')[:5],
        'categories': Category.objects.all(),
        'current_category': cat,
    })

def user_profile(request, myid):
    post = BlogPost.objects.filter(id=myid)
    return render(request, "user_profile.html", {'post': post})

def profile_view(request):
    return render(request, "profile.html")

def edit_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('/edit_profile/')
    else:
        form = ProfileForm(instance=profile)

    return render(request, "edit_profile.html", {'form': form})
    """try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method=="POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "edit_profile.html", {'alert':alert})
    else:
        form=ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {'form':form})
"""

def Register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')   
    return render(request, "register.html")

def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, 'login.html')
    return render(request, "login.html")

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')
