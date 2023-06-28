from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comment
from .forms import NewListingForm, BidForm, CommentForm


def index(request):
    #iterate through Listing.objects.all
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings":listings
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
    
def new_listing(request):
    if request.method == "GET":
        return render(request, "auctions/new_listing.html",{
            "form":NewListingForm
        })
    #render new_listing html file and use form
    elif request.method == "POST":
        listing_form = NewListingForm(request.POST, request.FILES) #might not need files part
        form_name, form_desc, form_bid, form_buy, form_image = listing_form.data["listing_name"], listing_form.data["listing_description"],listing_form.data["starting_bid"], listing_form.data["buy_now"], listing_form.data["listing_image"]
        #make sure buy now price is bigger than starting bid
        if form_buy == "":
            form_buy = None
        if form_buy is not None and float(form_buy) < float(form_bid):
            return render(request, "auctions/new_listing.html",{
                "error":"Buy Now must be greater than starting",
            "form":NewListingForm(initial={"listing_name":form_name, "listing_description":form_desc, "starting_bid":form_bid, "buy_now":form_buy, "listing_image":form_image})
        })
        curr_user = request.user
        if form_image != '':
            listing = Listing(name=form_name, description=form_desc, bid_price=form_bid, buy_now=form_buy, image=f"djangouploads/images/{form_image}", owner=curr_user)
        else:
            listing = Listing(name=form_name, description=form_desc, bid_price=form_bid, buy_now=form_buy, owner=curr_user)
        listing.save()
        #name description bid_price buy_now image
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))
        #temporary to see if it works it should go to the page for the 
        #actual listing
        

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    max_bid = listing.max_bid()
    return render(request, "auctions/listing.html", {
        "listing":listing, "bid_form":BidForm(),"max_bid":max_bid, "comment_form":CommentForm(), "comments":listing.comments.all()
    })

   

def bid(request, listing_id):
    if request.method == "POST":
        bid_form = BidForm(request.POST)
        val = bid_form.data["value"]
        listing = Listing.objects.get(pk=listing_id)
        user=request.user
        if (float(val) > listing.bid_price and listing.max_bid() is None) or int(val) > listing.max_bid():
            bid_model = Bid(amount=val, listing_ref=listing, bidder=user)
            bid_model.save()
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))
        else:
            return render(request, "auctions/listing.html", {
        "listing":listing, "bid_form":BidForm(),"max_bid":listing.max_bid(),
        "error":"Bid must be greater than starting and current bids", "comment_form":CommentForm(), "comments":listing.comments.all()
        })

def wishlist_view(request):
    user = request.user
    wishlist = user.wishlist.all()
    return render(request, "auctions/wishlist.html",
                  {
                      "wishlist":wishlist
                  })

def wishlist_add(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing.wishlisted.add(user)
    return render(request, "auctions/listing.html", {
        "listing":listing, "bid_form":BidForm(),"max_bid":listing.max_bid(),
        "message":"Successfully added to wishlist", "comment_form":CommentForm(), "comments":listing.comments.all()
        })

def wishlist_delete(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing.wishlisted.remove(user)
    wishlist = user.wishlist.all()
    return render(request, "auctions/wishlist.html",
                  {
                      "wishlist":wishlist
                  })

def new_comment(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    comment_form = CommentForm(request.POST)
    comment_text=comment_form.data["comment"]
    comment = Comment(content=comment_text, commenter=user, listing_ref=listing)
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=[listing.id]))
