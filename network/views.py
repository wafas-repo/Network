import json
from turtle import pos
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import PostCreateForm, UserForm

from .models import User, Post, UserProfile


def index(request):
    recent_posts = Post.objects.all().order_by('-dt_posted')[0:5];
    posts = Post.objects.all().order_by('-dt_posted');
    users = UserProfile.objects.all().order_by('followers')[0:5];
    # set up pagination
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    post_list = p.get_page(page)
    nums = 'a' * post_list.paginator.num_pages

    form = PostCreateForm(request.POST or None)
    if form.is_valid():
        content = request.POST.get('content')
        post = Post.objects.create(username=request.user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))

    context = {
        'form': form,
        'posts': posts,
        'recent_posts':recent_posts,
        'users': users,
        'post_list': post_list,
        'nums': nums
    }
    return render(request, "network/index.html", context)
    
@csrf_exempt
def edit(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

@csrf_exempt
def like(request, post_id):
    post = Post.objects.get(id=post_id)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    data = {
            'message': "Successfully submitted form data.",
            'post_id': post_id,
            'liked': liked,
            'like_total': post.total_likes()
    }
    return JsonResponse(data)


def login_view(request):
    recent_posts = Post.objects.all().order_by('-dt_posted')[0:5];
    users = UserProfile.objects.all().order_by('followers')[0:5];
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html", {'recent_posts':recent_posts, 'users':users})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    recent_posts = Post.objects.all().order_by('-dt_posted')[0:5];
    users = UserProfile.objects.all().order_by('followers')[0:5];
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html", {'recent_posts':recent_posts, 'users':users})

def profile(request, pk):
    uid = User.objects.get(id=pk)
    users = UserProfile.objects.all().order_by('followers')[0:5];
    recent_posts = Post.objects.all().order_by('-dt_posted')[0:5];
    profile = UserProfile.objects.get(user=uid)
    user = profile.user
    posts = Post.objects.filter(username=user).order_by('-dt_posted')
    followers = profile.followers.all()
    following = profile.following.all()
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    post_list = p.get_page(page)
    nums = 'a' * post_list.paginator.num_pages

    if len(followers) == 0:
        is_following = False

    if request.user in followers:
        is_following = True
    else:
        is_following = False
        
    number_of_followers = len(followers)
    number_of_following = len(following)


    return render(request, "network/profile.html", {
        "profile": profile, 
        "posts": posts,
        'users':users,
        'recent_posts':recent_posts,
        "number_of_followers": number_of_followers,
        "number_of_following": number_of_following,
        "is_following": is_following,
        'post_list': post_list,
        'nums': nums
    })


def add_follower(request, user_id):
    profile = UserProfile.objects.get(user=user_id)
    profile.followers.add(request.user)
    curr_user = UserProfile.objects.get(user=request.user.id)
    curr_user.following.add(profile.user)

    return redirect('profile', profile.user.id)

def remove_follower(request, user_id):
    profile = UserProfile.objects.get(user=user_id)
    profile.followers.remove(request.user)
    curr_user = UserProfile.objects.get(user=request.user.id)
    curr_user.following.remove(profile.user)

    return redirect('profile', profile.user.id)

def following(request, username):
    users = UserProfile.objects.all().order_by('followers')[0:5];
    recent_posts = Post.objects.all().order_by('-dt_posted')[0:5];
    uid = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=uid)
    following = profile.following.all()
    posts = Post.objects.filter(username__in=following).order_by('-dt_posted')
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    post_list = p.get_page(page)
    nums = 'a' * post_list.paginator.num_pages
           
    return render(request, "network/following.html", {
        "posts":posts,
        'post_list': post_list,
        'nums': nums,
        'users':users,
        'recent_posts':recent_posts
    })


def updateUser(request):
    users = UserProfile.objects.all().order_by('followers')[0:5];
    recent_posts = Post.objects.all().order_by('-dt_posted')[0:5];
    uid = request.user
    profile = UserProfile.objects.get(user=uid)
    form = UserForm(instance=profile)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=uid.id)
        else:
            print('invalid')
    return render(request, 'network/update-user.html', {'recent_posts':recent_posts, 'users':users, 'form':form})
    




