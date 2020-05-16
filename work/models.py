from django.db import models
from django.contrib.auth.models import User
from author.models import Author
import math

# Create your models here.
class Work(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='work')
    genre = models.CharField(max_length=30) # can be Fiction , Non-Fiction
    type = models.CharField(max_length=30) # can be thought , poem , short-story
    body = models.TextField() # content of the work
    rating = models.FloatField(default=0)
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    words_in_body = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)
    slug = models.SlugField(max_length=80)
    active = models.BooleanField(default=False)
    # ranking for the author only - if possible implement for work , else no problem

    class Meta:
        ordering = ['-rating', 'genre', 'type']


    def __str__(self):
        return self.title

    def get_pub_date(self):
        return self.pub_date

    def votes_total(self):
        votes = self.votedon.all()
        num_votes = len(votes)
        self.total_votes = num_votes
        return self.total_votes

    def get_rating(self):
        return math.ceil(self.rating * 10) / 10

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def summary(self):
        return self.body[:100] + '...'

    def word_count(self):
        # return the number of words in body of the self.body
        text = self.body
        all_words = text.split(' ')
        self.words_in_body = len(all_words)
        return self.words_in_body

class Comment(models.Model):
    work = models.ForeignKey(Work,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment', null=True)
    name = models.CharField(max_length=80)# signifies the to field
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    # active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

    def pub_date_pretty(self):
        return self.created_on.strftime('%b %e %Y')

class Vote(models.Model):
    votedby = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votedby')
    votedon = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='votedon')

    def __str__(self):
        return 'Vote on {} by {}'.format(self.votedon, self.votedby)
