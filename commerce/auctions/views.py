from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *

class BidForm(forms.Form):
    bid = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={"placeholder": "Bid"}))


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all()
    })


def login_view(request):
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "POST":
        l = Listing(name=request.POST.get("name"),
         start_bid=request.POST.get("start_bid"), 
         desc=request.POST.get("desc"), 
         image=request.POST.get("url"))
        l.save() 
    return render(request, "auctions/create.html")


def item(request, id): 
    item = Listing.objects.get(id=id)
    if Watchlist.objects.filter(user=request.user, item__id=id).exists():
        return render(request, "auctions/item.html", {
            "item" : item,
            "watch": "Remove from Watchlist",
            "form": BidForm()
        })
    else:
        return render(request, "auctions/item.html", {
            "item" : item,
            "watch": "Add to Watchlist",
            "form": BidForm()
        })


def watchlist(request, id): #Add a html/response for when it is successfully added
    if Watchlist.objects.filter(user=request.user, item__id=id).exists():
        Watchlist.objects.filter(user=request.user, item=Listing.objects.get(id=id)).delete()
    else: 
        Watchlist(user=request.user, item=Listing.objects.get(id=id)).save()


def bid(request):
    if request.method == "POST":
        form = BidForm(request.POST)

        if form.is_valid():
            new_bid = form.cleaned_data["bid"]