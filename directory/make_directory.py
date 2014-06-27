#!/usr/bin/env python3
from django_doge.settings import AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD

import ldap
import base64

from django.contrib.auth.models import User
from auth.models import DogeUser

from datetime import datetime

ENCODING = 'utf8'

SEARCH_BASE = 'ou=2013,ou=people,dc=42,dc=fr'
SEARCH_FILTERS = '(&(objectClass=*)(!(close=non admis)))'
SEARCH_ATTRS = [
    'first-name',
    'last-name',
    'birth-date',
    'picture',
    'mobile-phone',
    'alias'
]

DATETIME_IN_FORMAT = '%Y%m%d%H%M%SZ'
DATETIME_OUT_FORMAT = '%Y-%m-%d'

def get_attr(attrs, key):
    if key in attrs:
        return attrs[key][0].decode(ENCODING)
    return None

def parse_date(attrs):
    if 'birth-date' in attrs:
        bday = attrs['birth-date'][0].decode(ENCODING)
        date = datetime.strptime(bday, DATETIME_IN_FORMAT)
        return datetime.strftime(date, DATETIME_OUT_FORMAT)
    return None

def parse_picture(attrs):
    if 'picture' in attrs:
        return base64.b64encode(attrs['picture'][0])
    return None

def make_directory():
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    conn = ldap.initialize(AUTH_LDAP_SERVER_URI)
    conn.protocol_version = ldap.VERSION3
    conn.simple_bind_s(AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)
    users = conn.search_ext_s(SEARCH_BASE, ldap.SCOPE_SUBTREE, SEARCH_FILTERS, SEARCH_ATTRS)

    for user in users:
        if not user[1]:
            continue

        dn = user[0]
        attrs = user[1]
        login = dn[4:dn.index(',')]

        dogeUser = DogeUser(
            login=login,
            mail=get_attr(attrs, 'alias'),
            first_name=get_attr(attrs, 'first-name'),
            last_name=get_attr(attrs, 'last-name'),
            birth_date=parse_date(attrs),
            picture=parse_picture(attrs),
            phone=get_attr(attrs, 'mobile-phone'),
        )
        dogeUser.save()
