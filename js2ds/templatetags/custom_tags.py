from django import template
import json

register = template.Library()


# tag which formats string to look like nice formatted JSON
@register.simple_tag
def nice_json(string):
    return json.dumps(string, indent=4)


@register.simple_tag
def description(json_data):
    return json_data['description']


@register.simple_tag
def pattern(json_data):
    if 'pattern' in json_data:
        return json_data['pattern']
    else:
        return ""


@register.simple_tag
def root(json_data):
    return json_data['root']


@register.simple_tag
def eType(json_data):
    return json_data['eType']


@register.simple_tag
def parameters(json_data):
    return json_data['parameters']


@register.simple_tag
def minmax(json_data):
    data = ""
    if 'minimum' in json_data:
        data += json_data['minimum'] + ','
    else:
        data += '-inf' + ','
    if 'maximum' in json_data:
        data += json_data['maximum']
    else:
        data += 'inf'
    return data


@register.simple_tag
def minimum(json_data):
    data = "-inf"
    if 'minimum' in json_data:
        data = json_data['minimum']
    return data


@register.simple_tag
def maximum(json_data):
    data = "+inf"
    if 'maximum' in json_data:
        data = json_data['maximum']
    return data
