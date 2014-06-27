from django.contrib import admin
from forum.models import Category, Post, Thread, Comment, Announcement

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(Announcement)
