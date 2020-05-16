from django.db import models
from django.contrib.auth.models import User
from author.models import Author

# Create your models here.

# Create a different app for author, then copy that part from here
# import here Author class from author app
# import NormalUser class in models.py of author app

class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='normaluser')
    subscribed_author = models.ManyToManyField(Author,related_name='subscribers_users', blank=True)
    # no requirement of through field - because we dont want any specific information about the subscription
    # the issue is that - add an Author into Author , NormalUser , User
    # the issue also that - add a NormalUser into NormalUser , User but not into Author
    photo = models.ImageField(upload_to='images/')
    email = models.EmailField()
    # can login very easily , no aproval required

    def __str__(self):
        return self.user.username

    def get_subscribed_list(self):
        return self.subscribed_author.all()
