import json
import os


def get():
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

    # the return dictionary initialization
    schema_dict = dict()

    # fill schema_dict with key, value pairs
    # key is name of file
    # value is json data
    for sf in schema_files:
        json_data = json.loads(open(schema_dir+'/'+sf).read())
        schema_dict[sf] = json_data

    return schema_dict


def upload_byte_file(file_object):
    # current directory
    current_dir = os.path.dirname(__file__)
    # parent directory
    parent_dir = os.path.dirname(current_dir)
    # schema directory
    schema_dir = os.path.join(parent_dir, 'schema')
    # print(schema_dir)

    # 'wb' stands for write and byte
    # our f variable is a byte object
    with open(schema_dir + '/' + str(file_object), 'wb') as out:
        out.write(file_object.read())


def update(file_data, filename):
    # current directory
    current_dir = os.path.dirname(__file__)
    # parent directory
    parent_dir = os.path.dirname(current_dir)
    # schema directory
    schema_dir = os.path.join(parent_dir, 'schema')
    # print(schema_dir)

    # string data to json data
    json_data = json.loads(file_data)

    # write json to file
    with open(schema_dir + '/' + filename, 'w') as out:
        json.dump(json_data, out, indent=4)


def delete(filename):
    # current directory
    current_dir = os.path.dirname(__file__)
    # parent directory
    parent_dir = os.path.dirname(current_dir)
    # schema directory
    schema_dir = os.path.join(parent_dir, 'schema')
    # print(schema_dir)

    # delete schema file
    os.remove(schema_dir+'/'+filename)
