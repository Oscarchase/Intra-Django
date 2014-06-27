#!/usr/bin/env python3

import requests
import re
import json
from sys import stdin
from getpass import getpass
from urllib.parse import urljoin

from modules.models import Module, Activity

# Intranet constants
INTRA_BASE_URL = 'https://intra.42.fr/'
INTRA_URL = lambda path: urljoin(INTRA_BASE_URL, path)

INTRA_LOGIN_PATH = 'login'
AUTH_PAYLOAD = lambda login, password: {
    'login'    : login,
    'password' : password
}

MODULES = (
    INTRA_URL('/module/2013/ALGO-1-001/PAR-1-1'),
    INTRA_URL('/module/2013/UNIX-1-001/PAR-1-1'),
    INTRA_URL('/module/2013/INFOG-1-001/PAR-1-1'),
    INTRA_URL('/module/2013/WEB-1-002/PAR-2-1'),
    INTRA_URL('/module/2013/UNIX-1-002/PAR-2-1'),
)

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

ACT_TYPE = {
    'exam' : Activity.EXAM,
    'proj' : Activity.PROJECT,
    'tp' : Activity.TD
}

def main():
    print('Login: ', end='', flush=True)
    login = stdin.readline()
    password = getpass('Password: ')
    with IntraSession(login, password) as session:
        for module in MODULES:
            response = session.get(module, params={'format' : 'json'})
            json_string = '\n'.join(response.text.split('\n')[1:])
            data = json.loads(json_string)
            module = Module(
                name=data['title'],
                description=data['description'],
                places=420,
                start=data['begin'],
                end=data['end'],
                register_start=data['begin'],
                register_end=data['end_register'],
                credits=data['user_credits'],
            )
            module.save()
            for activity in data['activites']:
                project = Activity(
                    module=module,
                    name=activity['title'],
                    type=ACT_TYPE.get(activity['type_code'], Activity.TD),
                    description=activity['description'],
                    places=420,
                    start=data['begin'],
                    end=activity['end'],
                    register_start=data['begin'],
                    register_end=data['end_register'],
                    group_size=data.get('nb_max', 1),
                    peer_number=data.get('min_peer_note', 4)
                )
                project.save()

if __name__ == '__main__':
    main()
