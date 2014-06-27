from django.db import models

from auth.models import DogeUser
from re import sub

class Category(models.Model):
    title = models.CharField(max_length=50)
    sub_category = models.ForeignKey('Category', blank=True,
                                     null=True, default=None)

    def __str__(self):
        return self.title

class Thread(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    author = models.ForeignKey(DogeUser)
    created = models.DateTimeField()
    most_recent_post = models.ForeignKey('Post', blank=True, null=True, default=None, related_name='most_recent_post')
    followers = models.ManyToManyField(DogeUser, blank=True, null=True, default=None, related_name='followers')

    def __str__(self):
        return self.title

URL_PATTERN = r'(https?://[^\s]+)'
HYPERLINK_PATTERN = r'<a href="\1">\1</a>'

class Post(models.Model):
    content = models.TextField()
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(DogeUser)
    created = models.DateTimeField()
    upvote = models.ManyToManyField(DogeUser, blank=True, null=True, default=None, related_name='post_upvote')

    def __str__(self):
        return self.content[:50]

    def get_nb_up(self):
        return self.upvote.count()

    def content_as_html(self):
        html = sub(URL_PATTERN, HYPERLINK_PATTERN, self.content)
        return html.replace('\n', '<br>')

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post)
    author = models.ForeignKey(DogeUser)
    created = models.DateTimeField()
    upvote = models.ManyToManyField(DogeUser, blank=True, null=True, default=None, related_name='comment_upvote')

    def __str__(self):
        return self.content[:50]

    def get_nb_up(self):
        return self.upvote.count()

class Announcement(models.Model):
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content
