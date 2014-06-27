from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django_doge.decorators.forms import labels_as_placeholders
from auth.models import DogeUser
from forum.models import Thread, Post, Comment

import datetime

@labels_as_placeholders
class ThreadForm(forms.ModelForm):
    title = forms.CharField(max_length=100, label=_('Title'))
    content = forms.CharField(label=_('Post content'), widget=forms.Textarea)

    class Meta:
        model = Thread
        fields = (
            'title',
            'content',
        )

    def create_thread(self, author, category):
        new_thread = Thread(
            title = self.cleaned_data.get('title'),
            category = category,
            author = author,
            created = datetime.datetime.now(),
        )
        new_thread.save()
        new_post = Post(
            content = self.cleaned_data.get('content'),
            thread = new_thread,
            author = author,
            created = datetime.datetime.now(),
        )
        new_post.save()
        new_thread.most_recent_post = new_post
        new_thread.save()
        return new_thread

@labels_as_placeholders
class PostForm(forms.ModelForm):
    content = forms.CharField(label=_('Answer'), widget=forms.Textarea)

    class Meta:
        model = Post
        fields = (
            'content',
        )

    def create_post(self, author, thread):
        new_post = Post(
            content = self.cleaned_data.get('content'),
            thread = thread,
            author = author,
            created = datetime.datetime.now(),
        )
        new_post.save()
        thread.most_recent_post = new_post
        thread.save()
        return new_post

@labels_as_placeholders
class CommentForm(forms.ModelForm):
    content = forms.CharField(label=_('Comment'), widget = forms.Textarea)

    class Meta:
        model = Comment
        fields = (
            'content',
        )

    def create_comment(self, author, post):
        new_comment = Comment(
            content = self.cleaned_data.get('content'),
            post = post,
            author = author,
            created = datetime.datetime.now(),
        )
        new_comment.save()
        return new_comment
