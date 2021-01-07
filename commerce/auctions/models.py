from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=60, unique=True)
    def __str__(self):
        return f"{self.id}: {self.category}"

class Listing(models.Model):
    name = models.CharField(max_length = 50)
    start_bid = models.IntegerField()
    desc = models.CharField(max_length = 100)
    image = models.CharField(max_length = 2000)
    active = models.BooleanField(default = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listing") #user that created listing
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="item_category")
    def __str__(self):
        return f"{self.id}: Name:{self.name}, Bid:{self.start_bid}, Desc:{self.desc}"

class Bid(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id}: Bid: {self.bid} | User:{self.user} |Item:{self.item}"

class Comment(models.Model):
    comment = models.CharField(max_length = 250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")
    def __str__(self):
        return f"{self.id}: User: {self.user}, Item: {self.item}"
    class Meta:
        unique_together = ["user", "item"]

class Winner(models.Model):
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="winning_bid")
    def __str__(self):
        return f"{self.id}: Bid: {self.bid}"

