from django.core.urlresolvers import resolve

# Forum processing
from forum.models import Category, Thread, Post, Comment, Announcement
from auth.models import DogeUser

def forum_context(request):
    # Fetching categories
    categories = Category.objects.filter(sub_category__isnull=True)
    sub_categories = dict()
    for category in categories:
        sub_categories[category] = Category.objects.filter(sub_category=category)
    # Fetching latest anouncement
    try:
        announcement = Announcement.objects.latest('id')
    except Announcement.DoesNotExist:
        announcement = None
    # Fetching followed threads
    try :
        doge_user = DogeUser.objects.get(user=request.user)
        followed_threads = Thread.objects.filter(followers=doge_user)
    except DogeUser.DoesNotExist: # user not a doge user -> no threads followed
        followed_threads = []
    return {
        'categories' : categories,
        'sub_categories' : sub_categories,
        'announcement' : announcement,
        'followed_threads' : followed_threads,
    }

# Modules processing
from modules.models import Module, Activity

def modules_context(request):
    modules = Module.objects.all()
    activities = dict()
    for module in modules:
        activities[module] = Activity.objects.filter(module=module)
    return {
        'modules' : modules,
        'activities' : activities,
    }

# E-learning processing
def elearning_context(request):
    modules = Module.objects.all()
    activities = dict()
    for module in modules:
        activities[module] = Activity.objects.filter(module=module,
                                                     type=Activity.PROJECT)
    return {
        'modules' : modules,
        'activities' : activities,
    }

# Context processor dispatching
APP_PROCESSORS = {
    'forum' : forum_context,
    'e-learning' : elearning_context,
    'modules' : modules_context
}

def default(request):
    url = resolve(request.path)
    processor = APP_PROCESSORS.get(url.namespace, lambda request: dict())
    return processor(request)
