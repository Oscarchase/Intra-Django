from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index_view(request):
    return render(request, 'django_doge/index.html')

def not_found_view(request):
    return render(request, 'django_doge/index.html')
