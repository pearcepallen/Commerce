from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length = 50)
    start_bid = models.IntegerField()
    description = models.CharField(max_length = 100)
    image_link = models.CharField(max_length = 2000)
    def __str__(self):
        return f"{self.id}: Name:{self.name}, Bid:{self.start_bid}, Desc:{self.description}"

class Bid(models.Model):
    bid = models.IntegerField()

class Comment(models.Model):
    comment = models.CharField(max_length = 250)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_user")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id}: User: {self.user}, Item: {self.item}"
    class Meta:
        unique_together = ["user", "item"]