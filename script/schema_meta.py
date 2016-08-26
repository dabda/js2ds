import json
import os


def get():
    # current directory
    current_dir = os.path.dirname(__file__)
    # parent directory
    parent_dir = os.path.dirname(current_dir)
    # meta-schema directory
    schema_dir = os.path.join(parent_dir, 'schema', 'meta_schema')
    # print(schema_dir)

    # read meta-schema
    json_data = json.loads(open(schema_dir+'/'+'PropertyTypes.atjs').read())

    return json_data
