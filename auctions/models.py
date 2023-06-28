from django.contrib.auth.models import AbstractUser
from django.db import models

#MAKE __STR__ FOR THESE
class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2)
    buy_now = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="djangouploads/images/")
    owner = models.ForeignKey(User, blank=True, null=True, related_name="listings", on_delete=models.CASCADE)
    wishlisted = models.ManyToManyField(User, blank=True, related_name="wishlist")
    def max_bid(self):
        bids = [bid.amount for bid in self.bids.all()]
        if len(bids) > 0:
            return max(bids)
        else:
            return None
    def __str__(self):
        out = f"{self.name}"
        if self.max_bid():
            out += f" | Current Bid: ${self.max_bid()}"
        else:
            out += f" | Starting Bid: ${self.bid_price}"
        if self.buy_now:
            out += f" | Buy Now: ${self.buy_now}"
        return out
    
class Comment(models.Model):
    content = models.CharField(max_length=3000)
    commenter = models.ForeignKey(User, null=True, blank=True, related_name="comments", on_delete=models.CASCADE)
    listing_ref = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")


class Bid(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    listing_ref = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, null=True, blank=True, related_name="bids", on_delete=models.CASCADE)