from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=64, default='Default category')

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=64, default='Default Title')
    description = models.CharField(max_length=1000, default='Default description') 
    image = models.ImageField(upload_to='images/', blank=True, null=True )
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="listing_category", default='6')
    active = models.BooleanField(default=True)
    start_bid = models.DecimalField(max_digits=10, decimal_places=2, default='0.1')
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default='0.1')
    author = models.ForeignKey(User, default=None, blank=False, null=True, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.id} {self.title}"


class Bids(models.Model):
    bidder = models.ForeignKey(User, default=None, blank=False, null=True, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings", default='69')
    bid = models.DecimalField(max_digits=10, decimal_places=2, default='10')
    
    def __str__(self):
        return f"{self.bidder} {self.bid}"

class Comments(models.Model):
    lis_comments = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments", default='1')
    comments = models.CharField(max_length=64, default='Default comment')

    def __str__(self):
        return f"{self.lis_comments} {self.comments}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    item = models.ManyToManyField(Listing,  blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.user} {self.item}"  