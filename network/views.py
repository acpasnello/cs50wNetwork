from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Like, Follow
from .forms import PostForm
from .helpers import get_likes
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

    paginator = Paginator(posts, 10)
    if request.GET:
        if request.GET.get('page'):
            page_number = request.GET.get('page')
        else:
            page_number = 1
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"postform": form, 'page_obj': page_obj, 'posts': posts, 'liked': liked, 'postcount': range(posts.count())})

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
    # Profile owner
    user = User.objects.get(pk=userid)
    # Get user's followers and following counts
    followers = user.myfollowers
    followerCount = followers.count()
    following = user.myfollowing
    followingCount = following.count()
    # Check if viewing user follows the profile owner
    userFollowsProfile = False
    for item in followers.all():
        if item.follower_id == request.user.id:
            userFollowsProfile = True
    # User viewing their own profile?
    selfview = False
    if userid == request.user.id:
        selfview = True
    # Get profile user's posts
    posts = Post.objects.filter(poster=user).order_by('-posted')
    # check like status of each post for user viewing profile
    liked = {}
    for post in posts:
        # check if user has liked each post
        getlikes = Like.objects.filter(post=post).filter(user_id=request.user.id).count()
        if getlikes > 0:
            liked[post.pk] = True
        else:
            liked[post.pk] = False
    return render(request, "network/profile.html", {"profile_user": user, "followerCount": followerCount, "followingCount": followingCount, 'posts': posts, 'liked': liked, 'userFollowsProfile': userFollowsProfile, 'selfview': selfview})

def get_userlist(request, desiredlist):
    if request.method == "POST":
        jsonData = json.loads(request.body)
        #userid = request.POST.get('userid', default=None)
        userid = jsonData.get('userid')
    user = User.objects.get(pk=userid)
    userlist = []
    if desiredlist == "Followers" or desiredlist == "Follower":
        list = user.myfollowers.all()
        for item in list:
            userlist.append(User.objects.get(pk=item.follower.id))
    elif desiredlist == "Following":
        list = user.myfollowing.all()
        for item in list:
            userlist.append(User.objects.get(pk=item.following.id))
    else:
        return HttpResponseRedirect(reverse('profile', args=[userid]))

    return JsonResponse([item.serialize() for item in userlist], safe=False)

def following_index(request):
    userid = request.user.id
    user = User.objects.get(pk=userid)
    # print("user: ", user)
    followinglist = user.myfollowing.values('following')
    # print("following: ", followinglist)
    posts = Post.objects.filter(poster__in=followinglist).order_by('-posted')
    liked = get_likes(posts, userid)
    form = PostForm()
    
    paginator = Paginator(posts, 10)
    if request.GET:
        if request.GET.get('page'):
            page_number = request.GET.get('page')
        else:
            page_number = 1
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {'page_obj': page_obj, "posts": posts, "liked": liked, "postform": form})

@csrf_exempt
def editpost(request):
    if request.method == "POST":
        # Load submitted data
        jsonData = json.loads(request.body)
        postid = jsonData.get('postid')
        existingpost = Post.objects.get(pk=postid)
        print(existingpost)
        userid = request.user.id
        print(userid)
        user = User.objects.get(pk=userid)
        # Confirm user requesting owns post
        if existingpost.poster == user:
            # Update post in database
            print(existingpost.content)
            existingpost.content = jsonData.get('newContent')
            print(existingpost.content)
            existingpost.save()
            print(existingpost.serialize())
            response =  JsonResponse(existingpost.serialize())
            # response.headers['Access-Control-Allow-Origin', "*"]
            return response
        else:
            message = 'Users may only edit their own posts.'
            return JsonResponse(message)

@csrf_exempt
def updatefollow(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        activeUser = User.objects.get(pk=request.user.id)
        profileUser = User.objects.get(username=data["user"])
        currentState = data["currentState"]
        if currentState == "true":
            # Delete follow instance
            existingFollow = Follow.objects.filter(follower=activeUser).filter(following=profileUser)
            existingFollow.delete()
            return HttpResponse(status=202)
        elif currentState == "false":
            # Check follow instance does not exist
            if Follow.objects.filter(follower=activeUser).filter(following=profileUser):
                return HttpResponse(status=204)
            # Save new follow instance
            newFollow = Follow(follower=activeUser, following=profileUser)
            newFollow.save()
            return HttpResponse(status=201)
