import json
import os
from script import schemas


# read file
def read(filename):
    # read JSON
    if os.path.isfile(filename):
        json_data = json.loads(open(filename).read())
        return json_data
    else:
        return None


# write file
def write(filename, json_data):
    with open(filename, 'w') as out:
        json.dump(json_data, out, indent=4)


# check if file exists
def exists(filename):
    if os.path.isfile(filename):
        return True
    else:
        return False


# create file
def create(filename):
    if not os.path.exists(filename.rsplit("/", 1)[0]):
        os.makedirs(filename.rsplit("/", 1)[0])
    with open(filename, 'w+') as out:
        out.write("")


# populate JSON file and create directory structure
def populate(filename, schema_name, project_name, root_path, parameters):
    # if project_name empty return
    if project_name == "":
        return

    json_data = dict()
    json_data[schema_name.split(".")[0]] = dict()

    schema_data = dict()
    schema_data = schemas.get()
    schema_order = schema_data[schema_name]['Order']
    # we eliminate "Name" from schema_order
    schema_order.remove("Name")

    for o in schema_order:
        # create all folders
        if 'root' in schema_data[schema_name]['properties'][o]:
            make_path = schema_data[schema_name]['properties'][o]['root'].replace("{}", project_name)
            for ind, el in enumerate(parameters):
                dolar = "$" + str(ind + 1)
                make_path = make_path.replace(dolar, el)
            make_path = root_path + '/' + make_path
            if not os.path.exists(make_path):
                os.makedirs(make_path)

        # populate JSON
        if schema_data[schema_name]['properties'][o]['type'] in ["string"]:
            json_data[schema_name.split(".")[0]][o] = ""
        elif schema_data[schema_name]['properties'][o]['type'] in ["integer"]:
            json_data[schema_name.split(".")[0]][o] = ""
        elif schema_data[schema_name]['properties'][o]['type'] in ["double"]:
            json_data[schema_name.split(".")[0]][o] = ""
        elif schema_data[schema_name]['properties'][o]['type'] in ["File"]:
            json_data[schema_name.split(".")[0]][o] = ""
        else:
            json_data[schema_name.split(".")[0]][o] = []

    # write to file
    with open(filename, 'w') as out:
        json.dump(json_data, out, indent=4)
