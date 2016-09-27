import json
import os

from js2ds.script import schemas


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
def populate(filename, schema_name, project_name, root_path, parameters, schema_location):
    # if project_name empty return
    if project_name == "":
        return
    if project_name == "{}":
        return

    json_data = dict()
    json_data[schema_name.split(".")[0]] = dict()

    schema_data = dict()
    schema_data = schemas.get(schema_location)
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
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = ""
        elif schema_data[schema_name]['properties'][o]['type'] in ["integer"]:
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = ""
        elif schema_data[schema_name]['properties'][o]['type'] in ["double"]:
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = ""
        elif schema_data[schema_name]['properties'][o]['type'] in ["file"]:
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = ""
        elif schema_data[schema_name]['properties'][o]['type'] in ["entity"]:
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = ""
        else:
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = []

    # create output directory if not exist
    if not os.path.exists(os.path.dirname(os.path.realpath(filename))):
        os.makedirs(os.path.dirname(os.path.realpath(filename)))
    # write to file
    with open(filename, 'w') as out:
        json.dump(json_data, out, indent=4)


# check if file is .atjs file
# check if file is correct
def is_atjs(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for f in files:
        # check if file extension is correct
        temp = str(f).split(".")
        # no file extension
        if len(temp) == 1:
            return False, "<" + f + ">" + "Not .atjs file"
        # check extension
        if temp[1] == "atjs":
            pass
        else:
            return False, "<" + f + ">" + "Not .atjs file"

        # read file to check if valid
        try:
            json_object = json.loads(open(path + '/' + f).read())
        except ValueError:
            return False, "<" + f + ">" + "Not valid JSON file"

        # check if json has valid keys
        if 'Name' not in json_object:
            return False, "<" + f + ">" + "has no 'Name' key"
        if 'Order' not in json_object:
            return False, "<" + f + ">" + "has no 'Order' key"
        if 'properties' not in json_object:
            return False, "<" + f + ">" + "has no 'properties' key"
        if 'Filename' not in json_object:
            return False, "<" + f + ">" + "has no 'Filename' key"

        if type(json_object['Name']) is not str:
            return False, "<" + f + ">" + "'Name' is not str"
        if type(json_object['Order']) is not list:
            return False, "<" + f + ">" + "'Order' is not list"
        if type(json_object['properties']) is not dict:
            return False, "<" + f + ">" + "'properties' is not dict"
        if type(json_object['Filename']) is not str:
            return False, "<" + f + ">" + "'Filename' is not str"

        for key, value in json_object.items():
            if key not in ['Name', 'Order', 'properties', 'Filename']:
                return False, "<" + f + ">" + "key ['" + key + "'] not defined"

        order = json_object['Order']
        for key, value in json_object['properties'].items():
            if key not in order:
                return False, "<" + f + ">" + "['properties']['" + key + "'] not in 'Order'"

        for o in order:
            if type(json_object['properties'][o]) is not dict:
                return False, "<" + f + ">" + "['properties']['" + o + "'] is not dict"

            if 'type' not in json_object['properties'][o]:
                return False, "<" + f + ">" + "['properties']['" + o + "']has no 'type' key"
            if 'description' not in json_object['properties'][o]:
                return False, "<" + f + ">" + "['properties']['" + o + "']has no 'description' key"

            if type(json_object['properties'][o]['type']) is not str:
                return False, "<" + f + ">" + "['properties']['" + o + "']['type'] is not str"
            if type(json_object['properties'][o]['description']) is not str:
                return False, "<" + f + ">" + "['properties']['" + o + "']['description'] is not str"

            if json_object['properties'][o]['type'] not in ['string', 'string[]', 'integer', 'integer[]', 'double', 'double[]', 'file', 'file[]', 'files', 'entity', 'entity[]', 'entity_name'] :
                return False, "<" + f + ">" + "['properties']['" + o + "']['type'] has wrong type"

            if json_object['properties'][o]['type'] in ["string", "string[]", "entity_name"]:
                for key, value in json_object['properties'][o].items():
                    if key not in ['type', 'description', 'pattern']:
                        return False, "<" + f + ">" + "['properties']['" + o + "']['" + key + "'] has wrong key"
                    if type(value) is not str:
                        return False, "<" + f + ">" + "['properties']['" + o + "']['" + key + "'] value not str"

            if json_object['properties'][o]['type'] in ["integer", "integer[]", "double", "double[]"]:
                for key, value in json_object['properties'][o].items():
                    if key not in ['type', 'description', 'maximum', 'minimum']:
                        return False, "<" + f + ">" + "['properties']['" + o + "']['" + key + "'] has wrong key"
                    if type(value) is not str:
                        return False, "<" + f + ">" + "['properties']['" + o + "']['" + key + "'] value not str"

            if json_object['properties'][o]['type'] in ["file", "file[]"]:
                if 'root' not in json_object['properties'][o]:
                    return False, "<" + f + ">" + "['properties']['" + o + "'] has no root key"

                for key, value in json_object['properties'][o].items():
                    if key not in ['type', 'description', 'root', 'value']:
                        return False, "<" + f + ">" + "['properties']['" + o + "']['" + key + "'] has wrong key"
                    if type(value) is not str:
                        return False, "<" + f + ">" + "['properties']['" + o + "']['" + key + "'] value not str"

            if json_object['properties'][o]['type'] in ["entity", "entity[]"]:
                if 'eType' not in json_object['properties'][o]:
                    return False, "<" + f + ">" + "['properties']['" + o + "'] has no eType key"
                if 'parameters' not in json_object['properties'][o]:
                    return False, "<" + f + ">" + "['properties']['" + o + "'] has no parameters key"

                if type(json_object['properties'][o]['eType']) is not str:
                    return False, "<" + f + ">" + "['properties']['" + o + "']['eType'] is not str"
                if type(json_object['properties'][o]['parameters']) is not list:
                    return False, "<" + f + ">" + "['properties']['" + o + "']['parameters'] is not list"

                for key, value in json_object['properties'][o].items():
                    if key not in ['type', 'description', 'eType', 'parameters']:
                        return False, "<" + f + ">" + "['properties']['" + o + "']['" + key + "'] has wrong key"
                    if type(value) not in [str, list]:
                        return False, "<" + f + ">" + "['properties']['" + o + "']['" + key + "'] value not str/list"

    return True, ""


def legacy(filename, schema_name, project_name, root_path, parameters, schema_location):
    json_data = read(filename)

    schema_data = dict()
    schema_data = schemas.get(schema_location)
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
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = ""
        elif schema_data[schema_name]['properties'][o]['type'] in ["integer"]:
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = ""
        elif schema_data[schema_name]['properties'][o]['type'] in ["double"]:
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = ""
        elif schema_data[schema_name]['properties'][o]['type'] in ["file"]:
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = ""
        elif schema_data[schema_name]['properties'][o]['type'] in ["entity"]:
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = ""
        else:
            if o not in json_data[schema_name.split(".")[0]]:
                json_data[schema_name.split(".")[0]][o] = []

    # create output directory if not exist
    if not os.path.exists(os.path.dirname(os.path.realpath(filename))):
        os.makedirs(os.path.dirname(os.path.realpath(filename)))
    # write to file
    with open(filename, 'w') as out:
        json.dump(json_data, out, indent=4)
