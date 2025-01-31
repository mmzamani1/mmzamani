from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class Categorylist(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    category = models.ForeignKey(Categorylist, on_delete=models.CASCADE, blank=True, related_name="options")
    description = models.TextField(max_length=500, blank=True)
    image = models.URLField(default='https://user-images.githubusercontent.com/52632898/161646398-6d49eca9-267f-4eab-a5a7-6ba6069d21df.png', blank=True)
    active = models.BooleanField(default=True)
    watchlist = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.title} by {self.user}'
    
class Bids(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    
    def __str__(self):
        return f'{self.bid } on {self.item} by {self.user}'