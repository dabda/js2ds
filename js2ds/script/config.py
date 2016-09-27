import json
import os


def get(attribute):
    # current directory ( example: js2ds/script )
    current_dir = os.path.dirname(__file__)
    # parent directory ( example: js2ds )
    parent_dir = os.path.dirname(current_dir)
    # config directory ( example: js2ds/config )
    schema_dir = os.path.join(parent_dir, 'config')
    # print(schema_dir)

    json_data = json.loads(open(schema_dir+'/config.json').read())
    # print(schema_dir+'/config.json')
    # print(json_data)
    # print(json_data['root'])

    return json_data[attribute]


def write(value, key):
    # current directory ( example: js2ds/script )
    current_dir = os.path.dirname(__file__)
    # parent directory ( example: js2ds )
    parent_dir = os.path.dirname(current_dir)
    # config directory ( example: js2ds/config )
    config_dir = os.path.join(parent_dir, 'config')
    # print(schema_dir)

    json_data = json.loads(open(config_dir+'/config.json').read())
    json_data[key] = value
    # print(json_data)

    # output JSON with nice formatting
    with open(config_dir+'/config.json', 'w') as out:
        json.dump(json_data, out, indent=4)
