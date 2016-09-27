import json
import os
import datetime
from js2ds.script import JSON


def write(group, author, schema, project):
    # current directory ( example: js2ds/script )
    current_dir = os.path.dirname(__file__)
    # parent directory ( example: js2ds )
    parent_dir = os.path.dirname(current_dir)
    # config directory ( example: js2ds/config )
    config_dir = os.path.join(parent_dir, 'config')
    # print(schema_dir)

    json_data = json.loads(open(config_dir+'/group.json').read())
    json_data[group] = dict()
    json_data[group]['author'] = author
    json_data[group]['date'] = str(datetime.datetime.now()).split(" ")[0]
    json_data[group]['schema'] = schema
    json_data[group]['project'] = project
    json_data[group]['parent'] = parent(schema)

    # output JSON with nice formatting
    with open(config_dir+'/group.json', 'w') as out:
        json.dump(json_data, out, indent=4)


# return the parent schema
def parent(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    matrix = []
    for f in files:
        temp = JSON.read(path + '/' + f)
        temp = temp['properties']
        for name in temp:
            if temp[name]['type'] == 'entity' or temp[name]['type'] == 'entity[]':
                matrix.append(temp[name]['eType'] + '.atjs')
    for m in matrix:
        atjs = m + '.atjs'
        if atjs in matrix:
            files.remove(atjs)
    out = list(set(files) - set(matrix))
    return out[0]


# remove one group from group.json
def remove(group_name):
    # current directory ( example: js2ds/script )
    current_dir = os.path.dirname(__file__)
    # parent directory ( example: js2ds )
    parent_dir = os.path.dirname(current_dir)
    # config directory ( example: js2ds/config )
    config_dir = os.path.join(parent_dir, 'config')
    # print(schema_dir)

    json_data = get()
    json_data.pop(group_name, None)

    # output JSON with nice formatting
    with open(config_dir+'/group.json', 'w') as out:
        json.dump(json_data, out, indent=4)


def get():
    # current directory ( example: js2ds/script )
    current_dir = os.path.dirname(__file__)
    # parent directory ( example: js2ds )
    parent_dir = os.path.dirname(current_dir)
    # config directory ( example: js2ds/config )
    config_dir = os.path.join(parent_dir, 'config')
    # print(schema_dir)

    json_data = json.loads(open(config_dir+'/group.json').read())
    return json_data
