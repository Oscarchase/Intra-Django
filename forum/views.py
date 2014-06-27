from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse

from forum.models import Category, Thread, Post, Comment, Announcement
from forum.forms import ThreadForm, PostForm, CommentForm
from auth.models import DogeUser
from django_doge.decorators.auth import doge_user_required

def thread_redirect(thread_id):
    return HttpResponseRedirect(reverse('forum:thread', kwargs={
        'pk' : thread_id
    }))

@login_required
def index_view(request):
    return render(request, 'forum/index.html')

@login_required
def category_view(request, pk):
    category = get_object_or_404(Category, id=pk)
    sub_cat = Category.objects.filter(sub_category=category)
    threads = Thread.objects.filter(category=category).order_by('-created')
    return render(request, 'forum/categories.html', {
        'category' : category,
        'form': ThreadForm(),
        'sub_cat' : sub_cat,
        'threads' : threads,
    })

@login_required
def thread_view(request, pk):
    thread = get_object_or_404(Thread, id=pk)
    category = Category.objects.get(id=thread.category.id)
    posts = Post.objects.filter(thread=thread)
    try :
        doge_user = DogeUser.objects.get(user=request.user)
        follow = doge_user in thread.followers.all()
    except DogeUser.DoesNotExist:
        follow = False
    comments = dict()
    for post in posts:
        comments[post] = Comment.objects.filter(post=post)
    return render(request, 'forum/threads.html', {
        'thread': thread,
        'category': category,
        'posts': posts,
        'follow': follow,
        'comments': comments,
        'post_form': PostForm(),
        'comment_form': CommentForm(),
    })

#
# POSTS
#
def follow_thread(request, do_follow):
    doge_user = DogeUser.objects.get(user=request.user)
    try:
        thread_id = request.POST['thread_id']
    except KeyError:
        return HttpResponseRedirect(reverse('index'))
    thread = get_object_or_404(Thread, pk=thread_id)
    if do_follow:
        thread.followers.add(doge_user)
    else:
        thread.followers.remove(doge_user)
    thread.save()
    return thread_redirect(thread_id)

@doge_user_required
@require_POST
def follow_view(request):
    return follow_thread(request, True)

@doge_user_required
@require_POST
def unfollow_view(request):
    return follow_thread(request, False)

@doge_user_required
@require_POST
def new_thread_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    doge_user = DogeUser.objects.get(user=request.user)
    form = ThreadForm(data=request.POST)
    if form.is_valid():
        new_thread = form.create_thread(doge_user, category)
        return thread_redirect(new_thread.id)
    return HttpResponseRedirect(reverse('index'))

@doge_user_required
@require_POST
def up_post_view(request):
    doge_user = DogeUser.objects.get(user=request.user)
    try :
        post_id = request.POST['post_id']
    except KeyError:
        return HttpResponseRedirect(reverse('index'))
    post = get_object_or_404(Post, pk=post_id)
    post.upvote.add(doge_user)
    return thread_redirect(post.thread.id)

@doge_user_required
@require_POST
def up_comment_view(request):
    doge_user = DogeUser.objects.get(user=request.user)
    try:
        comment_id = request.POST['comment_id']
    except KeyError:
        return HttpResponseRedirect(reverse('index'))
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.upvote.add(doge_user)
    return thread_redirect(comment.post.thread.id)

@doge_user_required
@require_POST
def new_post_view(request, thread_id):
    doge_user = DogeUser.objects.get(user=request.user)
    form = PostForm(data=request.POST)
    thread = get_object_or_404(Thread, pk=thread_id)
    if form.is_valid():
        form.create_post(doge_user, thread)
        return thread_redirect(thread_id)
    return HttpResponseRedirect(reverse('index'))

@doge_user_required
@require_POST
def new_comment_view(request, post_id):
    doge_user = DogeUser.objects.get(user=request.user)
    form = CommentForm(data=request.POST)
    post = get_object_or_404(Post, pk=post_id)
    if form.is_valid():
        form.create_comment(doge_user, post)
        return thread_redirect(post.thread.id)
    return HttpResponseRedirect(reverse('index'))
