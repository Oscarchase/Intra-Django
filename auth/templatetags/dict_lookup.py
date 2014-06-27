from django import template

register = template.Library()

@register.filter(name='lookup')
def dict_lookup(dictionary, key):
    return dictionary.get(key)

@register.filter(name='errlookup')
def errdict_lookup(dictionary, key):
    output = []
    for field, errors in dictionary.items():
        if field == key:
            output.append('\n'.join('%s' % e for e in errors))
    return '\n'.join(output)
