from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.db.models import Q

from auth.models import DogeUser

RESULTS_PER_PAGE = 50

def paginated(sequence, opts):
    try:
        page = int(opts.get('page', 1))
    except ValueError:
        page = 1
    try:
        per_page = int(opts.get('per_page', RESULTS_PER_PAGE))
    except ValueError:
        per_page = RESULTS_PER_PAGE
    page = max(page, 1)
    per_page = max(per_page, 1)
    begin = (page - 1) * per_page
    end = min(len(sequence), page * per_page)
    filtered = list()
    if len(sequence) > begin :
        filtered = sequence[begin:end]
    else:
        begin = -1
        end = 0
    return filtered, page, begin + 1, end, per_page

@login_required
def directory_view(request):
    # Search filter
    try:
        query = request.GET['query']
        sql_query = Q(login__contains=query) |\
                    Q(first_name__contains=query) |\
                    Q(last_name__contains=query)
        users = DogeUser.objects.filter(sql_query)
    except KeyError:
        users = DogeUser.objects.all()
    # Sorting
    try:
        sort_key = request.GET['sort']
        try:
            ordered = users.order_by(sort_key)
            # Forcing evaluation (maybe find a better way in the future)
            len(ordered)
            users = ordered
        except FieldError:
            pass
    except KeyError:
        pass
    # Pagination
    current_users, page, start, end, per_page = paginated(users, request.GET)
    return render(request, 'directory/directory.html', {
        'current_page' : page,
        'next_page' : str(page + 1),
        'previous_page' : str(page - 1),
        'per_page' : per_page,
        'user_start' : start,
        'user_end' : end,
        'user_count' : len(users),
        'users' : current_users
    })
