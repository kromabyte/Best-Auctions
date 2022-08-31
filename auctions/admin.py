from django.contrib import admin
from .models import User, Comments, Listing, Categories, Bids, Watchlist

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Categories)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)