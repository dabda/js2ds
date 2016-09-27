import json
import os


def get():
    # current directory ( example: js2ds/script )
    current_dir = os.path.dirname(__file__)
    # parent directory ( example: js2ds )
    parent_dir = os.path.dirname(current_dir)
    # config directory ( example: js2ds/schema/meta_schema )
    schema_dir = os.path.join(parent_dir, 'schema')
    # print(schema_dir)

    # read meta-schema
    json_data = json.loads(open(schema_dir+'/'+'PropertyTypes.atjs').read())

    return json_data
