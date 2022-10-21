from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
import json

from .models import User, Post, Like, Follow
from .forms import PostForm
# from .helpers import login_required
# U: Tony
# P: network
# U: admin
# P: network

def index(request):
    form = PostForm()
    # Get 10 posts at a time
    posts = Post.objects.all().order_by('-posted')
    liked = {}
    for post in posts:
        # check if user has liked each post
        getlikes = Like.objects.filter(post=post).filter(user_id=request.user.id).count()
        if getlikes > 0:
            liked[post.pk] = True
        else:
            liked[post.pk] = False

    return render(request, "network/index.html", {"postform": form, 'posts': posts, 'liked': liked, 'postcount': range(posts.count())})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
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
        return render(request, "network/register.html")


def post(request):
    # If POST, process new post
    if request.method == "POST":
        if request.user.is_authenticated:
            data = request.POST
            form = PostForm(data)
            if form.is_valid():
                # Add logged in user as poster
                newpost = form.save(commit=False)
                newpost.poster = request.user
                # newpost.poster_id = "Test"
                newpost.likecount = '0'
                newpost.save()
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, "network/index.html")
        else:
            return render(request, "network/index.html")
    else:
        return render(request, "network/index.html")

def like(request, postid):
    post = Post.objects.get(pk=postid)
    newLike = Like(user=request.user, post=post)
    newLike.save()
    post.likecount += 1
    post.save()
    return render(request, "network/index.html")

def unlike(request, postid):
    postid = int(postid)
    post = Post.objects.get(pk=postid)
    unlike = Like.objects.filter(user=request.user).filter(post=post)
    unlike.delete()
    if post.likecount > 0:
        post.likecount -= 1
        post.save()
    return render(request, "network/index.html")
    # return JsonResponse({"message": f"Post liked by {request.user}."}, status=201)

def profile(request, userid):
    user = User.objects.get(pk=userid)
    followerCount = user.myfollowers.count()
    followingCount = user.myfollowing.count()
    posts = Post.objects.filter(poster=user).order_by('-posted')
    liked = {}
    for post in posts:
        # check if user has liked each post
        getlikes = Like.objects.filter(post=post).filter(user_id=request.user.id).count()
        if getlikes > 0:
            liked[post.pk] = True
        else:
            liked[post.pk] = False
    return render(request, "network/profile.html", {"profile_user": user, "followerCount": followerCount, "followingCount": followingCount, 'posts': posts, 'liked': liked})

def get_userlist(request, desiredlist):
    if request.method == "POST":
        jsonData = json.loads(request.body)
        #userid = request.POST.get('userid', default=None)
        userid = jsonData.get('userid')
    user = User.objects.get(pk=userid)
    userlist = []
    if desiredlist == "followers":
        list = user.myfollowers.all()
        for item in list:
            userlist.append(User.objects.get(pk=item.follower.id))
    elif desiredlist == "following":
        list = user.myfollowing.all()
        for item in list:
            userlist.append(User.objects.get(pk=item.following.id))
    else:
        return HttpResponseRedirect(reverse('profile', args=[userid]))

    # response = JsonResponse({'userlist': userlist})
    #return JsonResponse(serializers.serialize('json', userlist, use_natural_foreign_keys=True), safe=False)
    return JsonResponse([item.serialize() for item in userlist], safe=False)
    # return render(request, "network/userlist.html", {"list": userlist})
