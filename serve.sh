./manage.py collectstatic --noinput -l
uwsgi --socket /tmp/django_doge.sock --module django_doge.wsgi
