from django import template
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

register = template.Library()

def replace_query_param(url, key, value):
    parsed_url = urlparse(url)
    query = dict((k, v if len(v) > 1 else v[0])
                    for k, v in parse_qs(parsed_url.query).items())
    query[key] = value
    query_string = urlencode(query)
    return urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        query_string,
        parsed_url.fragment
    ))

@register.filter(name='setpage')
def set_page(url, page):
    return replace_query_param(url, 'page', page)

@register.filter(name='setsort')
def set_sort(url, field):
    return replace_query_param(url, 'sort', field)

