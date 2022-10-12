from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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

    return render(request, "network/index.html", {"postform": form})

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
