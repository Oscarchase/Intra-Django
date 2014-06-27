#!/usr/bin/env python3

import requests
import re
import json
from sys import stdin
from getpass import getpass
from urllib.parse import urljoin

from forum.models import Category, Thread, Post, Comment
from auth.models import DogeUser

# Intranet constants
INTRA_BASE_URL = 'https://intra.42.fr/'
INTRA_URL = lambda path: urljoin(INTRA_BASE_URL, path)

INTRA_LOGIN_PATH = 'login'
AUTH_PAYLOAD = lambda login, password: {
    'login'    : login,
    'password' : password
}

FORUM_BASE_URL = 'https://intra.42.fr/forum/index/get'
FORUM_BASE_PARAMS = {
    'format' : 'json',
    'path' : '/'
}

FORUM_SUB_CAT_URL = 'https://intra.42.fr/forum/node/list'
FORUM_SUB_CAT_PARAMS = lambda path : {
    'format' : 'json',
    'nodes[]' : path
}

FORUM_THREADS_URL = 'https://intra.42.fr/forum/thread/list'
FORUM_THREADS_PARAMS = lambda path : {
    'format' : 'json',
    'node' : path
}

FORUM_POST_URL = 'https://intra.42.fr/forum/post/list'
FORUM_POST_PARAMS = lambda thread : {
    'format' : 'json',
    'thread' : thread
}

class IntraSession(requests.Session) :

    def __init__(self, login, password):
        super().__init__()
        self.students = list()
        self.login = login
        self.password = password

    def __enter__(self):
        super().__enter__()
        login_url = INTRA_URL(INTRA_LOGIN_PATH)
        payload = AUTH_PAYLOAD(self.login, self.password)
        try :
            # Ignore SSL verifications...
            response = self.post(login_url, data=payload, verify=False)
            if response.status_code != requests.codes.ok :
                print('Authentification failed : %d' % response.status_code)
        except Exception as e :
            print('Authentification failed : %s' % e)
        return (self)

    def __exit__(self, type, value, traceback):
        super().__exit__(type, value, traceback)

def leech_category(session, category, category_data):
    response = session.get(FORUM_THREADS_URL, params=FORUM_THREADS_PARAMS(category_data['path']))
    json_string = '\n'.join(response.text.split('\n')[1:])
    threads_data = json.loads(json_string)
    for thread_data in threads_data:
        # Threads
        try:
            author = DogeUser.objects.get(login=thread_data['user']['login'])
        except:
            continue
        thread = Thread(
            title=thread_data['name'],
            category=category,
            author=author,
            created=thread_data['date'],
        )
        thread.save()
        response = session.get(FORUM_POST_URL, params=FORUM_POST_PARAMS(thread_data['path']))
        json_string = '\n'.join(response.text.split('\n')[1:])
        posts_data = json.loads(json_string)
        for post_data in posts_data:
            # Posts
            try:
                author = DogeUser.objects.get(login=post_data['user']['login'])
            except:
                continue
            post = Post(
                thread=thread,
                author=author,
                content=post_data['content'],
                created=post_data['date']
            )
            post.save()
            for comment_data in post_data['comments']:
                # Comments
                try:
                    author = DogeUser.objects.get(login=comment_data['user']['login'])
                except:
                    continue
                comment = Comment(
                    post=post,
                    author=author,
                    content=comment_data['content'],
                    created=comment_data['date']
                )
                comment.save()


def main():
    print('Login: ', end='', flush=True)
    login = stdin.readline()
    password = getpass('Password: ')
    with IntraSession(login, password) as session:
        print('Fetching categroies')
        response = session.get(FORUM_BASE_URL, params=FORUM_BASE_PARAMS)
        json_string = '\n'.join(response.text.split('\n')[1:])
        categories_data = json.loads(json_string)
        for category_data in categories_data['node']['children']:
            # Parent categories
            try:
                category = Category.objects.get(title=category_data['name'])
            except Category.DoesNotExist:
                category = Category(title=category_data['name'])
                category.save()
            #
            print(category_data['name'])
            print('Fetching subcategory')
            response = session.get(FORUM_SUB_CAT_URL, params=FORUM_SUB_CAT_PARAMS(category_data['path']))
            json_string = '\n'.join(response.text.split('\n')[1:])
            sub_cat_data = json.loads(json_string)
            leech_category(session, category, category_data)
            for sub_cat in sub_cat_data[category_data['path']]:
                # Sub categories
                try:
                    sub_category = Category.objects.get(title=sub_cat['name'],
                                                        sub_category=category)
                except Category.DoesNotExist:
                    sub_category = Category(title=sub_cat['name'],
                                            sub_category=category)
                    sub_category.save()
                #
                print('\t', sub_cat['name'])
                leech_category(session, sub_category, sub_cat)


if __name__ == '__main__':
    main()
