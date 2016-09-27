import json
import os

from django.shortcuts import render
from js2ds.script import schemas, config, schema_meta, JSON, project, group, navigation


# page for managing schemas
def schema(request):
    title = "JSON Schema Management"
    log_message = ""
    flag = True
    group_data = group.get()

    # upload new schema files
    if request.method == 'POST':
        for g in group_data:
            for fileobject in request.FILES.getlist('upload_files_' + group_data[g]['schema']):
                # byte file object
                # print(fileobject.read())
                # print(type(fileobject))
                # name of file, use str() to parse
                # print(fileobject)
                schemas.upload_byte_file(group_data[g]['schema'], fileobject)
                log_message += "<UPLOADED: " + str(fileobject) + "> "

    # delete all schemas files
    delete_all = request.POST.get('delete_all', "NO")
    if delete_all != "NO":
        schemas.delete_all(delete_all)
        log_message += "All files in folder: " + delete_all + " deleted!"
        flag = False

    # get schema data in text_area
    text_area_data = request.POST.get('text_area', "NO")
    # get schema folder location
    schema_folder = request.POST.get('schema_folder', "NO")

    # save schema data to file
    schema_filename = request.POST.get('schema_save', "NO")
    if schema_filename != "NO":
        schemas.update(schema_folder, text_area_data, schema_filename)
        log_message += "File: " + schema_filename + " in folder " + schema_folder + " updated!"

    # delete schema file
    delete_schema = request.POST.get('schema_delete', "NO")
    if delete_schema != "NO":
        schemas.delete(schema_folder, delete_schema)
        log_message += "File: " + delete_schema + " in folder " + schema_folder + " deleted!"
        flag = False

    # schema data from existing files
    # must be after delete, upload file(s) and rename
    group_data = group.get()
    for g in group_data:
        group_data[g]['data'] = schemas.get(group_data[g]['schema'])

    return render(request, 'js2ds-schema.html', {'title': title,
                                                 'flag': flag,
                                                 'log_message': log_message,
                                                 'group_data': group_data,
                                                 },
                  )


# page for meta-schema
def meta_schema(request):
    title = "Meta-Schema"
    schema_data = dict()
    schema_data = schema_meta.get()
    return render(request, 'js2ds-meta-schema.html', {'title': title,
                                                      'schema_data': schema_data},
                  )


# page for js2ds creation
def index(request):
    title = "js2ds - JSON Schema to Directory Structure"
    log_message = ""
    flag = True

    # empty NAVIGATON
    navigation.write({})

    # create new group/set (writen to config/group.json)
    group_add = request.POST.get('group_add', "")
    if group_add == "true":
        group_name = request.POST.get('group_name', "")
        group_author = request.POST.get('group_author', "")
        group_schema = request.POST.get('group_schema', "")
        group_project = request.POST.get('group_project', "")

        # create project output folder
        if not os.path.exists(group_project):
            os.makedirs(group_project)
        # create schema folder
        if not os.path.exists(group_schema):
            os.makedirs(group_schema)

        # check if folders were created
        if not os.path.exists(group_project):
            flag = False
            log_message += "<group_project " + group_project + " folder can not be created>"
        if not os.path.exists(group_schema):
            flag = False
            log_message += "<group_schema " + group_schema + " folder can not be created>"

        # upload schema files
        if flag:
            if request.method == 'POST':
                for fileobject in request.FILES.getlist('group_upload_schema_files'):
                    schemas.upload_byte_file(group_schema, fileobject)

        # are schemas valid
        (flag, log_message) = JSON.is_atjs(group_schema)

        # create group else error
        if flag:
            group.write(group_name, group_author, group_schema, group_project)
            log_message = "SUCCESS: New group was created: " + "<group_name: " + group_name \
                          + "> <group_author: " + group_author \
                          + "> <group_schema: " + group_schema \
                          + "> <group_project: " + group_project + ">"
        else:
            log_message = "FAILURE: " + log_message
    # END // create new group/set (writen to config/group.json)

    # read from group.json
    group_data = group.get()

    group_delete = request.POST.get('delete_group', "")
    if group_delete != "":
        log_message = project.delete(group_data[group_delete]['project'], "")
        log_message = log_message + ", " + project.delete(group_data[group_delete]['schema'], "")
        group.remove(group_delete)
        flag = False

    # read from group.json (updated values if one group got deleted)
    group_data = group.get()

    # create list of elements for each group
    for g in group_data:
        # root_path is the root of directory structure ( example: G:/projects )
        root_path = group_data[g]['project']
        # root_schema is the name of the root schema ( example: Project.atjs )
        parent = group_data[g]['parent']

        # schema data from existing files ( key -> name of schema, value -> json )
        schema_data = schemas.get(group_data[g]['schema'])
        # abstract filename of root_schema ( example: PROJ-{}/proj/{}.atp )
        filename = schema_data[parent]['Filename']

        # get name of project to DELETE ( example: BasicMatrixMul )
        project_delete = request.POST.get('delete_' + g, "")
        if project_delete != "":
            # extract leftmost directory from filename ( example: PROJ-{} )
            temp = filename.split("/")[0]
            # create full name of directory to delete ( example: PROJ-BasicMatrixMul )
            project_delete = temp.replace("{}", project_delete)
            # delete the directory ( example: G:/projects/PROJ-BasicMatrixMul )
            log_message = project.delete(root_path, project_delete)
            flag = False

        # load project list ( example: ['BasicMatrixMul', 'BasicSort'] )
        # project_list = project.get_list(root_path, schema_data[root_schema]['Filename'])
        group_data[g]['project_list'] = project.get_list(root_path, filename)

    return render(request, 'js2ds-index.html', {'title': title,
                                                'flag': flag,
                                                'log_message': log_message,
                                                'group_data': group_data},
                  )


def js2ds(request):
    # NAVIGATION
    for i in range(1, 17):
        navigation_data = request.POST.get('navigation' + str(i), "")
        if navigation_data != "":
            object_data = navigation.get()
            for pop in range(i+1,17):
                object_data.pop(str(pop), None)
            navigation.write(object_data)
            return render(request, 'js2ds.html', object_data[str(i)],)

    # ENTITY LIST
    entity_list = []

    # PARAMETERS default is []
    parameters = []

    # ENTITY_NAME from EDIT or ADD from /index/ ( example: BasicMatrixMul )
    group_data = group.get()
    entity_name = ""
    for g in group_data:
        entity_name = request.POST.get('edit_' + g, entity_name)
        entity_name = request.POST.get('add_' + g, entity_name)
        if entity_name != "":
            config.write(group_data[g]['project'], 'root')
            config.write(group_data[g]['parent'], 'parent')
            config.write(group_data[g]['schema'], 'schema')
            break
    entity_name = request.POST.get('Name', entity_name)
    # from ADD Entity /js2ds/ ( example: QuickSort )
    entity_name = request.POST.get('entity_name', entity_name)
    if entity_name != "":
        entity_list.append(entity_name)

    # ROOT_PATH directory of directory structure ( example: G:/projects )
    root_path = config.get('root')

    # SCHEMA_NAME name of schema file ( example: Project.atjs )
    schema_name = config.get('parent')
    schema_name = request.POST.get('schema_filename', schema_name)

    # ALL SCHEMA DATA from .atjs files # key -> name of schema # value -> json
    schema_location = config.get('schema')
    schema_data = schemas.get(schema_location)

    # TODO
    # checking for empty entity name (BAD back/forward)
    # creates {} directory

    # FILENAME of JSON output file
    filename = root_path + '/' + schema_data[schema_name]['Filename']
    # create full path replace {}
    if entity_name != "":
        filename = filename.replace("{}", entity_name)

    # SAVE values from SUBMIT
    submit = request.POST.get('submit_button', "")

    # on EDIT ENTITY we must also submit
    order = schema_data[schema_name]["Order"]
    submit_edit = ""
    submit_edit_name = ""
    submit_edit_key = ""
    for o in order:
        if schema_data[schema_name]["properties"][o]["type"] == "entity[]":
            for number in range(1, 257):
                submit_edit = request.POST.get('edit' + str(number) + o, submit_edit)
                if submit_edit != "":
                    submit_edit_name = request.POST.get('input_edit' + str(number) + o, "")
                    submit_edit_key = o
                    break
            if submit_edit != "":
                break
    if submit_edit == "EDIT":
        submit = "SUBMIT"
    print(submit_edit)
    print(submit_edit_name)

    # on ADD ENTITY we must also submit and then edit
    submit_add = ""
    submit_add_name = ""
    submit_add_key = ""
    for o in order:
        submit_add = request.POST.get('add_entity'+o, submit_add)
        submit_add_name = request.POST.get('add_entity_name' + o, submit_add_name)
        if submit_add != "":
            submit_add_key = o
            break
    if submit_add == "ADD":
        submit = "SUBMIT"
    print(submit_add)
    print(submit_add_name)

    # SUBMIT THE DATA
    if submit == "SUBMIT":
        print("HELLO SUBMIT")
        parameters_str = request.POST.get('parameters', "")
        parameters_str = parameters_str.replace("'", '"')
        parameters = list(json.loads(parameters_str))
        # example: Project.atjs
        schema_name = request.POST.get('schema_filename', "")
        print("schema_name: " + schema_name)
        # example: ['MatrixMul', "Strassen"]
        ent_list = request.POST.get('entity_list', "")
        ent_list = ent_list.replace("'", '"')
        entity_list = list(json.loads(ent_list))
        print("entity_list: ", entity_list)
        # example: TestniProjekt
        entity_name = request.POST.get("Name", entity_name)
        print("entity_name: " + entity_name)
        # example: F:/django/diploma/projects/PROJ-TestniProjekt/proj/TestniProjekt.atp
        filename = request.POST.get('Filename', "")
        print("filename: ", filename)
        # example: data in json file
        existing_data = JSON.read(filename)
        order = schema_data[schema_name]['Order']

        for o in order:

            # STRING
            if schema_data[schema_name]['properties'][o]['type'] in ["string"]:
                existing_data[schema_name.split(".")[0]][o] = request.POST.get(o, "")

            # STRING[]
            if schema_data[schema_name]['properties'][o]['type'] in ["string[]"]:
                string_array = request.POST.get(o, "")
                string_array = json.loads(string_array.replace("'", '"'))
                existing_data[schema_name.split(".")[0]][o] = string_array

            # INTEGER
            elif schema_data[schema_name]['properties'][o]['type'] in ["integer"]:
                if request.POST.get(o, "") == "":
                    existing_data[schema_name.split(".")[0]][o] = ""
                else:
                    existing_data[schema_name.split(".")[0]][o] = int(request.POST.get(o, ""))

            # INTEGER[]
            if schema_data[schema_name]['properties'][o]['type'] in ["integer[]"]:
                if request.POST.get(o, "") == "[]":
                    existing_data[schema_name.split(".")[0]][o] = []
                else:
                    integer_array = request.POST.get(o, "")
                    integer_array = json.loads(integer_array)
                    existing_data[schema_name.split(".")[0]][o] = integer_array

            # DOUBLE
            elif schema_data[schema_name]['properties'][o]['type'] in ["double"]:
                if request.POST.get(o, "") == "":
                    existing_data[schema_name.split(".")[0]][o] = ""
                else:
                    existing_data[schema_name.split(".")[0]][o] = float(request.POST.get(o, ""))

            # DOUBLE[]
            if schema_data[schema_name]['properties'][o]['type'] in ["double[]"]:
                if request.POST.get(o, "") == "[]":
                    existing_data[schema_name.split(".")[0]][o] = []
                else:
                    double_array = request.POST.get(o, "")
                    double_array = json.loads(double_array)
                    existing_data[schema_name.split(".")[0]][o] = double_array

            # FILE
            elif schema_data[schema_name]['properties'][o]['type'] in ["file"]:
                previous_filename = existing_data[schema_name.split(".")[0]][o]
                new_filename = request.POST.get(o, "")
                file_data = request.POST.get("textarea" + o, "")
                root = request.POST.get("root" + o, "")
                for i_par, par in enumerate(parameters):
                    dolar = "$" + str(i_par + 1)
                    root = root.replace(dolar, par)
                # delete old file and create new
                # example: G:/projects/PROJ-NoviProjekt/proj/doc/js2ds-index.html
                if new_filename != previous_filename:
                    project.delete_file(root_path + '/' + root.replace("{}", entity_name) + '/' + previous_filename)
                # ERROR ERROR ENTITY NAME "" ?
                project.write(root_path + '/' + root.replace("{}", entity_name) + '/' + new_filename, file_data)
                existing_data[schema_name.split(".")[0]][o] = new_filename
                # END OF FILE

            # FILES
            elif schema_data[schema_name]['properties'][o]['type'] in ["files"]:
                # example ['alg1.jar', 'alg2.jar']
                previous_file_names = existing_data[schema_name.split(".")[0]][o]
                # example: ['alg1.jar', 'alg3.jar', 'alg4.jar']
                new_file_names = request.POST.get(o, "[]")
                new_file_names = json.loads(new_file_names.replace("'", '"'))
                # example: PROJ-{}/proj/lib
                root_of_files = request.POST.get("root" + o, "")
                for i_par, par in enumerate(parameters):
                    dolar = "$" + str(i_par + 1)
                    root_of_files = root_of_files.replace(dolar, par)
                # files that will be deleted ( example: ["alg2.jar"] )
                files_to_be_deleted = [item for item in previous_file_names if item not in new_file_names]
                # example: F:/django/diploma/projects/PROJ-TestniProjekt/proj/src
                files_path = root_path + '/' + root_of_files.replace("{}", entity_name)
                # example: el in ['BasicSort.atp', 'BasicSort-jvm.atrd']
                for el in files_to_be_deleted:
                    # F:/django/diploma/projects/PROJ-TestniProjekt/proj/src/BasicSort.atp
                    # F:/django/diploma/projects/PROJ-TestniProjekt/proj/src/BasicSort-jvm.atrd
                    print(files_path + '/' + el)
                    project.delete_file(files_path + '/' + el)
                # upload files that were added by the user
                if request.method == 'POST':
                    for fileobject in request.FILES.getlist('upload_files' + o):
                        # byte file object
                        # print(fileobject.read())
                        # print(type(fileobject))
                        # name of file, use str() to parse
                        # print(fileobject)
                        project.upload(files_path, fileobject)
                existing_data[schema_name.split(".")[0]][o] = new_file_names
                # END OF FILES

            # ENTITY[]
            elif schema_data[schema_name]['properties'][o]['type'] in ["entity[]"]:
                # example ["Test1","Test2"]
                previous_entities = existing_data[schema_name.split(".")[0]][o]
                # example: ["Test2"]
                new_entities = request.POST.get(o, "[]")
                new_entities = json.loads(new_entities.replace("'", '"'))
                # eType ( example: "Algorithm" )
                e_type = request.POST.get("eType" + o, "")
                # parameters ( example: ["PROJ-{}"] )
                e_param = request.POST.get("param" + o, "[]")
                # full parameters names ( example: ["PROJ-BasicSort"] )
                e_param = json.loads(e_param.replace("'", '"'))
                e_parameters = []
                for ind, ele_param in enumerate(e_param):
                    e_parameters.append(ele_param.replace("{}", entity_list[ind]))
                print(e_parameters)

                # example: F:/django/diploma/projects/
                e_path = root_path + "/"
                # example: F:/django/diploma/projects/$1/tests/{}.atts
                for key, value in schemas.get(schema_location).items():
                    if key.split(".")[0] == e_type:
                        e_path += schemas.get(schema_location)[e_type + ".atjs"]["Filename"]
                # example: F:/django/diploma/projects/PROJ-TestniProjekt/algs/ALG-{}/{}.atal
                for i_count, e_p in enumerate(e_parameters):
                    dolar = "$" + str(i_count + 1)
                    e_path = e_path.replace(dolar, e_p)
                # example: F:/django/diploma/projects/PROJ-TestniProjekt/algs/ALG-{}
                new_e_path = ""
                for i_part, part in enumerate(e_path.split("/")):
                    if "{}" not in part:
                        new_e_path += part + "/"
                    elif "{}" in part:
                        new_e_path += part
                        break
                # entities that will be deleted ( example: ["Test1"] )
                entity_to_be_deleted = [item for item in previous_entities if item not in new_entities]
                # is it a file or directory
                if "." in new_e_path:
                    # file
                    for en_del in entity_to_be_deleted:
                        # TODO
                        # files to delete, names from output json
                        # from type file, file[] and files
                        # need root locations from schema and names from json
                        clean_up_names = JSON.read(new_e_path.replace("{}", en_del))
                        clean_up_roots = ""

                        # delete the output json file
                        project.delete_file(new_e_path.replace("{}", en_del))

                else:
                    # directory
                    for en_del in entity_to_be_deleted:
                        project.del_tree(new_e_path.replace("{}", en_del))
                # add the one from ADD new entity
                if submit_add == "ADD" and submit_add_key == o:
                    new_entities.append(submit_add_name)
                existing_data[schema_name.split(".")[0]][o] = new_entities
                # END OF ENTITY []

        # write to JSON
        JSON.write(filename, existing_data)
        # END of FOR in SUBMIT

        # ADD new ENTITY
        # we need to populate new JSON + create directories
        if submit_add == "ADD":
            # example: Algorithm.atjs
            schema_name = request.POST.get("eType" + submit_add_key, "") + ".atjs"
            # example: ['TestniProjekt']
            ent_list = request.POST.get('entity_list', "")
            ent_list = ent_list.replace("'", '"')
            entity_list = list(json.loads(ent_list))
            # parameters ( example: ["PROJ-{}"] )
            e_param = request.POST.get("param" + submit_add_key, "[]")
            # full parameters names ( example: ["PROJ-BasicSort"] )
            e_param = json.loads(e_param.replace("'", '"'))
            e_parameters = []
            for ind, ele_param in enumerate(e_param):
                e_parameters.append(ele_param.replace("{}", entity_list[ind]))
            # example: $1/algs/ALG-{}/{}.atal
            filename = schema_data[schema_name]["Filename"]
            # example: $1/algs/ALG-Strassen/Strassen.atal
            filename = filename.replace("{}", submit_add_name)
            # example: $PROJ-Matrix/algs/ALG-Strassen/Strassen.atal
            for i_count, e_p in enumerate(e_parameters):
                dolar = "$" + str(i_count + 1)
                filename = filename.replace(dolar, e_p)
            filename = root_path + "/" + filename
            # populate data
            JSON.populate(filename, schema_name, submit_add_name, root_path, e_parameters, schema_location)
            parameters = e_parameters
            entity_list.append(submit_add_name)
            entity_name = submit_add_name
        # END of ADD

        # EDIT ENTITY
        if submit_edit == "EDIT":
            print("HELLO EDIT")
            # example: Algorithm.atjs
            schema_name = request.POST.get("eType" + submit_edit_key, "") + ".atjs"
            # example: ['TestniProjekt']
            ent_list = request.POST.get('entity_list', "")
            ent_list = ent_list.replace("'", '"')
            entity_list = list(json.loads(ent_list))
            # parameters ( example: ["PROJ-{}"] )
            e_param = request.POST.get("param" + submit_edit_key, "[]")
            # full parameters names ( example: ["PROJ-BasicSort"] )
            e_param = json.loads(e_param.replace("'", '"'))
            e_parameters = []
            for ind, ele_param in enumerate(e_param):
                e_parameters.append(ele_param.replace("{}", entity_list[ind]))
            # example: $1/algs/ALG-{}/{}.atal
            filename = schema_data[schema_name]["Filename"]
            # example: $1/algs/ALG-Strassen/Strassen.atal
            filename = filename.replace("{}", submit_edit_name)
            # example: $PROJ-Matrix/algs/ALG-Strassen/Strassen.atal
            for i_count, e_p in enumerate(e_parameters):
                dolar = "$" + str(i_count + 1)
                filename = filename.replace(dolar, e_p)
            filename = root_path + "/" + filename
            parameters = e_parameters
            entity_list.append(submit_edit_name)
            entity_name = submit_edit_name

        # END of EDIT

    # END of SUBMIT

    # create file structure and template JSON
    # of new project if it doesnt exist
    # if it exists read JSON
    if JSON.exists(filename):
        JSON.legacy(filename, schema_name, entity_name, root_path, parameters, schema_location)
        existing_data = JSON.read(filename)
    else:
        JSON.create(filename)
        JSON.populate(filename, schema_name, entity_name, root_path, [], schema_location)
        # in this case values are ""
        existing_data = JSON.read(filename)

    # array of order of displaying items
    order = schema_data[schema_name]['Order']

    # read all existing files for the textareas
    files = dict()
    for o in order:
        if schema_data[schema_name]['properties'][o]['type'] == "file":
            # example: PROJ-TestniProjekt/proj/doc
            path_part = schema_data[schema_name]['properties'][o]['root'].replace("{}", entity_name)
            for i_count, e_p in enumerate(parameters):
                dolar = "$" + str(i_count + 1)
                path_part = path_part.replace(dolar, e_p)
            # example: js2ds-index.html
            last_part = existing_data[schema_name.split(".")[0]][o]
            # full path example: G:/projects/PROJ-TestniProjekt/proj/doc/js2ds-index.html
            files[o] = (project.read(root_path + '/' + path_part + '/' + last_part))

    # name of files in type FILES
    files_download = dict()
    for o in order:
        if schema_data[schema_name]['properties'][o]['type'] == "files":
            # example: PROJ-TestniProjekt/proj/lib
            path_part = schema_data[schema_name]['properties'][o]['root'].replace("{}", entity_name)
            for i_count, e_p in enumerate(parameters):
                dolar = "$" + str(i_count + 1)
                path_part = path_part.replace(dolar, e_p)
            # example: [] or ['alg1.jar', 'alg2.jar']
            last_part = existing_data[schema_name.split(".")[0]][o]
            files_download[o] = []
            if last_part:
                for element in last_part:
                    # full path example: G:/projects/PROJ-TestniProjekt/proj/src/alg.jar
                    full_path = root_path + '/' + path_part + '/' + element
                    files_download[o].append(full_path)

    print("===========END===========")
    print("entity_name =", entity_name)
    print("root_path =", root_path)
    print("schema_name =", schema_name)
    print("filename =", filename)
    print("order =", order)
    print("files =", files)
    print("files_download =", files_download)
    print("===========END===========")

    nav_object = dict()
    nav_object['title'] = entity_name
    nav_object['filename'] = filename
    nav_object['schema_filename'] = schema_name
    nav_object['entity_list'] = entity_list
    nav_object['parameters'] = parameters
    nav_object['schema_name'] = schema_data[schema_name]['Name']
    nav_object['entity_name'] = entity_name
    nav_object['order'] = order
    nav_object['existing_data'] = existing_data
    nav_object['files'] = files
    nav_object['files_download'] = files_download
    nav_object['schema_data'] = schema_data[schema_name]['properties']
    nav_object_json = navigation.get()
    for i in range(1, 17):
        if str(i) not in nav_object_json:
            if i > 1:
                nav_temp = navigation.get()
                nav_temp[str(i-1)]['existing_data'] = JSON.read(nav_temp[str(i-1)]['filename'])
                navigation.write(nav_temp)
            navigation.write_location(nav_object, i)
            break

    return render(request, 'js2ds.html', {'title': entity_name,
                                          'filename': filename,
                                          'schema_filename': schema_name,
                                          'entity_list': entity_list,
                                          'parameters': parameters,
                                          'schema_name': schema_data[schema_name]['Name'],
                                          'entity_name': entity_name,
                                          'order': order,
                                          'existing_data': existing_data,
                                          'files': files,
                                          'files_download': files_download,
                                          'schema_data': schema_data[schema_name]['properties']},
                  )
