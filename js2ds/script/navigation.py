import json
import os


def write(nav_obj):
    # current directory ( example: js2ds/script )
    current_dir = os.path.dirname(__file__)
    # parent directory ( example: js2ds )
    parent_dir = os.path.dirname(current_dir)
    # config directory ( example: js2ds/config )
    config_dir = os.path.join(parent_dir, 'config')
    # print(config_dir)


    # output JSON with nice formatting
    with open(config_dir+'/navigation.json', 'w') as out:
        json.dump(nav_obj, out, indent=4)


def write_location(nav_obj, location):
    # current directory ( example: js2ds/script )
    current_dir = os.path.dirname(__file__)
    # parent directory ( example: js2ds )
    parent_dir = os.path.dirname(current_dir)
    # config directory ( example: js2ds/config )
    config_dir = os.path.join(parent_dir, 'config')
    # print(config_dir)

    json_data = json.loads(open(config_dir+'/navigation.json').read())
    json_data[location] = nav_obj


    # output JSON with nice formatting
    with open(config_dir+'/navigation.json', 'w') as out:
        json.dump(json_data, out, indent=4)


def get():
    # current directory ( example: js2ds/script )
    current_dir = os.path.dirname(__file__)
    # parent directory ( example: js2ds )
    parent_dir = os.path.dirname(current_dir)
    # config directory ( example: js2ds/config )
    config_dir = os.path.join(parent_dir, 'config')
    # print(config_dir)

    json_data = json.loads(open(config_dir+'/navigation.json').read())
    return json_data
