import json
import os


def get(attribute):
    # current directory
    current_dir = os.path.dirname(__file__)
    # parent directory
    parent_dir = os.path.dirname(current_dir)
    # schema/config directory
    schema_dir = os.path.join(parent_dir, 'schema', 'config')
    # print(schema_dir)

    json_data = json.loads(open(schema_dir+'/config.json').read())
    # print(schema_dir+'/config.json')
    # print(json_data)
    # print(json_data['root'])

    return json_data[attribute]


def write(path, attribute):
    # current directory
    current_dir = os.path.dirname(__file__)
    # parent directory
    parent_dir = os.path.dirname(current_dir)
    # schema/config directory
    schema_dir = os.path.join(parent_dir, 'schema', 'config')
    # print(schema_dir)

    json_data = json.loads(open(schema_dir+'/config.json').read())
    if json_data[attribute] != path:
        json_data[attribute] = path
        # print(json_data)

        # output JSON with nice formatting
        with open(schema_dir+'/config.json', 'w') as out:
            json.dump(json_data, out, indent=4)


def delete():
    # current directory
    current_dir = os.path.dirname(__file__)
    # parent directory
    parent_dir = os.path.dirname(current_dir)
    # schema directory
    schema_dir = os.path.join(parent_dir, 'schema')
    # print(schema_dir)

    # read all files in directory, excluding directories
    schema_files = [f for f in os.listdir(schema_dir) if os.path.isfile(os.path.join(schema_dir, f))]
    # print(schema_files)

    # delete all files in schema directory
    for sf in schema_files:
        os.remove(schema_dir+'/'+sf)
