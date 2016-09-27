import json
import os


def get(path):
    # read all files in directory, excluding directories
    schema_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # print(schema_files)

    # the return dictionary initialization
    schema_dict = dict()

    # fill schema_dict with key, value pairs
    # key is name of file
    # value is json data
    for sf in schema_files:
        json_data = json.loads(open(path+'/'+sf).read())
        schema_dict[sf] = json_data

    return schema_dict


def upload_byte_file(path, file_object):
    # 'wb' stands for write, byte
    # f is a byte object
    with open(path + '/' + str(file_object), 'wb') as out:
        out.write(file_object.read())


# update schema in given schema folder
def update(path, file_data, filename):
    # string data to json data
    json_data = json.loads(file_data)

    # write json to file
    with open(path + '/' + filename, 'w') as out:
        json.dump(json_data, out, indent=4)


# delete schema in given schema folder
def delete(path, filename):
    # delete schema file
    os.remove(path+'/'+filename)


# delete all schema files in folder
def delete_all(path):
    # read all files in directory, excluding directories
    schema_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # print(schema_files)

    # delete all files in schema directory
    for sf in schema_files:
        os.remove(path+'/'+sf)
