from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *

class BidForm(forms.Form):
    bid = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={"placeholder": "Bid"}))

class CommentForm(forms.Form):
    comment = forms.CharField(label=False, widget=forms.TextInput(attrs={"placeholder": "Write a comment"}))


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(active=True)
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
        cat_id = request.POST.get("category")
        category = Category.objects.get(id = cat_id)

        l = Listing(name=request.POST.get("name"),
         start_bid=request.POST.get("start_bid"), 
         desc=request.POST.get("desc"), 
         image=request.POST.get("url"),
         user=request.user,
         category=category)
        l.save() 
    
    categories = Category.objects.all()
    return render(request, "auctions/create.html", {
        "categories": categories
    })


def item(request, id): 
    item = Listing.objects.get(id=id)
    user = request.user
    comments = Comment.objects.filter(item__id = id)
    if Bid.objects.filter(item=item).exists():
        bid = Bid.objects.filter(item=item).last()
        if Watchlist.objects.filter(user=request.user, item__id=id).exists():
            return render(request, "auctions/item.html", {
                "curr_user": user, 
                "item" : item,
                "bid": bid,
                "watch": "Remove from Watchlist",
                "comments": comments,
                "form": BidForm(),
                "comment_form": CommentForm()
            })
        else:
            return render(request, "auctions/item.html", {
                "curr_user": user, 
                "item" : item,
                "bid": bid,
                "watch": "Add to Watchlist",
                "comments": comments,
                "form": BidForm(),
                "comment_form": CommentForm()
            })
    else:
        if Watchlist.objects.filter(user=request.user, item__id=id).exists():
            return render(request, "auctions/item.html", {
                "curr_user": user, 
                "item" : item,
                "watch": "Remove from Watchlist",
                "comments": comments,
                "form": BidForm(),
                "comment_form": CommentForm()
            })
        else:
            return render(request, "auctions/item.html", {
                "curr_user": user, 
                "item" : item,
                "watch": "Add to Watchlist",
                "comments": comments,
                "form": BidForm(),
                "comment_form": CommentForm()
            })


def watchlist(request, id): #Add a html/response for when it is successfully added
    if Watchlist.objects.filter(user=request.user, item__id=id).exists():
        Watchlist.objects.filter(user=request.user, item=Listing.objects.get(id=id)).delete()
        return HttpResponseRedirect(reverse("item", args=[id]))
    else: 
        Watchlist(user=request.user, item=Listing.objects.get(id=id)).save()
        return HttpResponseRedirect(reverse("item", args=[id]))


def bid(request, id): #Add proper front end response
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            new_bid = form.cleaned_data["bid"]

            item=Listing.objects.get(id=id)
            if Bid.objects.filter(item=item).exists():
                if new_bid > Bid.objects.filter(item=item).last().bid:
                    Bid(bid=new_bid, user=request.user, item=item).save()
                    return HttpResponse("Success, larger than current bid")
                else:
                    return HttpResponse("Failer, smaller/equal current bid")
            else:
                if new_bid >= item.start_bid :
                    Bid(bid=new_bid, user=request.user, item=item).save()
                    return HttpResponse("Success, larger than start bid")
                else:
                    return HttpResponse("Failure, smaller than start bid")
    else:
        return HttpResponse("Nothing happened")


def close(request, id):
    item = Listing.objects.get(id=id)
    item.active = False
    item.save()
    end_bid = Bid.objects.filter(item=item).last()
    Winner(bid=end_bid).save()
    return(HttpResponseRedirect(reverse("index")))

def comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.cleaned_data["comment"]
            item = Listing.objects.get(id=id)
            Comment(comment=new_comment, user=request.user, item=item).save()
            return HttpResponseRedirect(reverse("item", args=[id]))
    else:
        return HttpResponseRedirect(reverse("item", args=[id]))

def watching(request):
    watch_items = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watch_items": watch_items
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    item = Category.objects.get(category=category)
    category_items = item.item_category.filter(active=True)
    return render(request, "auctions/category.html", {
        "category_items": category_items,
        "category": category
    })