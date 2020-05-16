from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    coolname = models.CharField(max_length=100)
    bio = models.TextField()
    rating = models.FloatField(default=2.5)
    photo = models.ImageField(upload_to='images/')
    email = models.EmailField()
    ranking = models.PositiveIntegerField()
    # when creating the author object , assign the last rank
    # get all the authors sorted according to the rating
    # then find the index, and assign that to ranking
    # do that in views.py , before rendering to the authordetails.html page

    # subscribed_author = models.ManyToManyField('Author', related_name='subscribers_authors', default=None)
    # when an author wants to subscribe authors

    active = models.BooleanField(default=False)
    # so as to activate the author after acceptance of first work
    # if an author is unable to login, then simply his first work has not been accepted
    # mention this special bit of information on the login page

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return self.coolname

    def get_ranking(self):
        author_ordered_list = Author.objects.order_by('-rating')
        rank = 1
        for author in author_ordered_list:
            if author.coolname == self.coolname:
                self.ranking = rank
                break
            rank += 1
        return self.ranking

    def get_rating(self):
        # assign value to self.rating
        # estimate the average rating of all the posts
        # check if there are atleast more than ten votes on each work
        # then only use this get rating , else return default rating
        all_works = self.work.all()
        num_works = 0
        total_rating = 0
        for work in all_works:
            if work.total_votes < 10:
                return self.rating
            # every author must have at least 10 votes for each of his Work
            # otherwise his rating would remain the same
            num_works += 1
            total_rating += work.rating
        try:
            self.rating = total_rating/num_works
        except:
            self.rating = 2.5
        self.save()
        return self.rating

    def get_subscribed_list(self):
        return self.subscribed_author.all()


class Blog(models.Model):
    author = models.ForeignKey(Author, related_name='bloglinks', on_delete=models.CASCADE)
    url = models.URLField()
    sitename = models.CharField(max_length=100)

    def __str__(self):
        return self.author.coolname + '/' + self.sitename
