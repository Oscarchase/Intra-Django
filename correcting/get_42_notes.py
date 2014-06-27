import requests
import json

from sys import stdin
from getpass import getpass
from urllib.parse import urljoin
from random import choice

from auth.models import DogeUser
from modules.models import Module, Activity
from correcting.models import Grade, Rank

# Intranet constants
INTRA_BASE_URL = 'https://intra.42.fr/'
INTRA_URL = lambda path: urljoin(INTRA_BASE_URL, path)

INTRA_LOGIN_PATH = 'login'
AUTH_PAYLOAD = lambda login, password: {
    'login'    : login,
    'password' : password
}

USER_PROFILE_PATH = 'user'
USER_NOTES_PATH = lambda login: '%s/%s/notes' % (USER_PROFILE_PATH, login)
USER_NOTES_URL = lambda login: INTRA_URL(USER_NOTES_PATH(login))
USER_NOTES_PARAMS = {
    'format' : 'json'
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

GRADES = {
    'A' : Rank.RANK_A,
    'B' : Rank.RANK_B,
    'C' : Rank.RANK_C,
    'D' : Rank.RANK_D,
    'Echec' : Rank.RANK_FAIL,
}

def main():
    print('Login: ', end='', flush=True)
    login = stdin.readline()
    password = getpass('Password: ')
    with IntraSession(login, password) as session:
        users = DogeUser.objects.all()
        for user in users:
            print(user)
            response = session.get(USER_NOTES_URL(user.login),
                                   params=USER_NOTES_PARAMS,
                                   verify=False)
            json_string = '\n'.join(response.text.split('\n')[1:])
            user_data = json.loads(json_string)
            for module_data in user_data['modules']:
                try:
                    module = Module.objects.get(name=module_data['title'])
                except Module.DoesNotExist:
                    continue
                module.registered.add(user)
                # Adding ranks
                try:
                    rank_value = GRADES[module_data['grade']]
                except KeyError:
                    continue
                rank = Rank(student=user, module=module, value=rank_value)
                rank.save()
            # Adding grades
            for note_data in user_data['notes']:
                try:
                    activity = Activity.objects.get(name=note_data['title'])
                except Activity.DoesNotExist:
                    continue
                grade = Grade(
                    student=user,
                    activity=activity,
                    value=note_data['final_note'],
                    grader=choice(users)
                )
                grade.save()
