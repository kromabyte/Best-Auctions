from email import message
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from django.db.models import Max
from django.contrib import messages
from .models import Bids, Comments, User, Listing, Categories, Watchlist

# Form Class for New Listing

class CreateForm(forms.Form):
    title = forms.CharField(label= "Title", widget=forms.TextInput(attrs={
        'class' : ' form-control col-md-10',
        'placeholder':'Enter Title',
        })
        )
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={
        'class' : 'form-control col-md-10',
        'placeholder':'Enter Description',
        })
        )
    start_bid = forms.DecimalField(label='Start bid', widget=forms.NumberInput(attrs={
        'class' : 'form-control col-md-10',
        'placeholder':'Enter Bid',
        })
        )
    image = forms.ImageField(label="Upload an Image",
    )

class BidForm(forms.Form):
    bid = forms.DecimalField(label="Make a Bid", widget=forms.NumberInput(attrs={
        'class' : 'form-control col-md-10',
        'placeholder':'Enter Bid',
        })
        )
    
class CommentForm(forms.Form):
    comment = forms.CharField(label="Make a Comment", widget=forms.TextInput(attrs={
        'class' : 'form-control col-md-10',
        'placeholder':'Enter Comment',
        })
        )


        #INDEX

def index(request):
    listings = Listing.objects.filter(active=True)

    return render(request, "auctions/index.html", {
        "listings": listings, 
    })


        #CLOSED AUCTIONS

def closed(request):
    listings = Listing.objects.filter(active=False)

    return render(request, "auctions/closed.html", {
        "listings": listings,
    })


        #CATEGORIES

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Categories.objects.all(),
    })

def category(request, category_id):
    category_obj = Categories.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category_obj, active=True)

    return render(request, "auctions/category.html", {
        "category": category_obj,
        "listings": listings,
    })


        #LOGIN VIEW

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


        #LISTING

def listing(request, listing_id):
    # TAKE THE listing ID
    listing = Listing.objects.get(pk=listing_id)

    #get comments
    comments = Comments.objects.filter(lis_comments=listing)

    # take de higher bid
    bids = Bids.objects.filter(listing=listing).aggregate(Max('bid'))['bid__max']
    #set default bid
    if bids is None:
        bids = listing.start_bid

    # get the winner information
    winner = Bids.objects.filter(listing=listing).order_by("-bid").first()
    
    if winner is None:
        winner = listing.start_bid
    
    #check wishlist items
    try:
        user = Watchlist.objects.get(user=request.user)
        match = user.item.filter(id=listing_id)
    except:
        match = None
        
        #MADE A BID 
    if request.method == "POST":
        bid_form = BidForm(request.POST)

        if bid_form.is_valid():
            new_bid = bid_form.cleaned_data["bid"]
            
            if new_bid > bids:
                messages.success(request, 'you made a Bid')
                New_Bid = Bids(
                    bidder=request.user,
                    listing=listing,
                    bid=new_bid,
                )
                New_Bid.save()
                
                #UPDATE THE CURRENT BID

                listing.current_bid = new_bid
                listing.save()
                
                return redirect(reverse("listing", args=[listing_id]))

            else:
                messages.error(request, 'Your offer should be higher than the current quote!')

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_form": BidForm(),
        "bids": bids,
        "comments": comments,
        "comment_form": CommentForm,
        "match": match,
        "winner":winner
    })



    #COMMENT

def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            messages.success(request, 'you made a comment')
            new_comment = comment_form.cleaned_data["comment"]
            New_Comment = Comments(
                lis_comments=listing,
                comments=new_comment
            )
            New_Comment.save()

        return redirect(reverse("listing", args=[listing_id]))


        #CLOSE AUCTION

def close(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()
        messages.success(request, 'you close the Auction')
        
        return redirect(reverse("listing", args=[listing_id]))


        #CREATE LISTING

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES)
        category = Categories.objects.get(pk=int(request.POST["category"]))
        
        # If form is valid get de data ready to logic
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            start_bid = form.cleaned_data["start_bid"]
            
            New_Listing = Listing(
                title=title,
                description=description,
                image=image,
                start_bid=start_bid,
                category=category,
                current_bid=start_bid,
                author=request.user
                )
            New_Listing.save()
        
            return redirect(reverse("listing", args=[New_Listing.id]))

    return render(request, "auctions/create.html", {
        "createform": CreateForm(),
        "categories": Categories.objects.all(),
    })


        # WISHLIST

@login_required 
def watchlist(request):
    item = ''
    try:
        users = Watchlist.objects.get(user=request.user)
        item = users.item.all()
    except:
        users = None

    return render(request, "auctions/watchlist.html", {
        "items": item,
    })

def add_or_remove(request, listing_id):
    if request.method == "POST":
        if (request.POST["action"]) == "add":
            try:
                wishlist = Watchlist.objects.get(user=request.user)
            except Watchlist.DoesNotExist:
                wishlist = Watchlist(user=request.user)
                wishlist.save()
            try:
                listing = Listing.objects.get(pk=listing_id)
                wishlist.item.add(listing)
            except:
                create.save()
                wishlist.item.add(listing)
            messages.success(request, 'you added to Watchlist')

        elif (request.POST["action"]) == "remove":
            wishlist = Watchlist.objects.get(user=request.user)
            item = wishlist.item.get(id=listing_id)
            wishlist.item.remove(item)

            messages.success(request, 'you removed from Watchlist')

    return redirect(reverse("listing", args=[listing_id]))


