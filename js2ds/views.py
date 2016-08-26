from django.shortcuts import render
from script import schemas, config, schema_meta, project, JSON
import json


# page for managing schemas
def schema(request):
    title = "JSON Schema Management"
    link = ["/index/", "/meta-schema/"]

    # root_path is saved in config.json (the same for root_schema)
    # if we get the value from POST we use that one
    # if no value from POST we use default value, second argument
    root_path = request.POST.get('root_path', config.get('root'))
    config.write(root_path, 'root')
    root_schema = request.POST.get('root_schema', config.get('parent'))
    config.write(root_schema, 'parent')

    # upload new schema files
    if request.method == 'POST':
        for fileobject in request.FILES.getlist('upload_files'):
            # byte file object
            # print(fileobject.read())
            # print(type(fileobject))
            # name of file, use str() to parse
            # print(fileobject)
            schemas.upload_byte_file(fileobject)

    # delete all schemas files
    delete_all = request.POST.get('delete_all', "NO")
    if delete_all == "YES":
        config.delete()

    # get schema data in textarea
    textarea_data = request.POST.get('textarea', "NO")

    # save schema data to file
    schema_filename = request.POST.get('schema_save', "NO")
    if schema_filename != "NO":
        schemas.update(textarea_data, schema_filename)

    # delete schema file
    delete_schema = request.POST.get('schema_delete', "NO")
    if delete_schema != "NO":
        schemas.delete(delete_schema)

        # schema data from existing files
        # must be after delete, upload file(s) and rename
    schema_data = dict()
    schema_data = schemas.get()

    return render(request, 'schema.html', {'title': title,
                                           'link': link,
                                           'schema_data': schema_data,
                                           'root_path': root_path,
                                           'root_schema': root_schema,
                                           },
                  )


# page for meta-schema
def meta_schema(request):
    title = "Meta-Schema"
    link = ["/index/", "/schema/"]
    schema_data = dict()
    schema_data = schema_meta.get()
    return render(request, 'meta-schema.html', {'title': title,
                                                'link': link,
                                                'schema_data': schema_data},
                  )


# page for js2ds creation
def index(request):
    title = "js2ds - JSON Schema to Directory Structure"
    link = "/schema/"
    refresh = "/index/"

    # root_path is the root of directory structure ( example: G:/projects )
    root_path = config.get('root')
    # root_schema is the name of the root schema ( example: Project.atjs )
    root_schema = config.get('parent')

    # schema data from existing files ( key -> name of schema, value -> json )
    schema_data = dict()
    schema_data = schemas.get()
    # abstract filename of root_schema ( example: PROJ-{}/proj/{}.atp )
    filename = schema_data[root_schema]['Filename']

    # get name of project to DELETE ( example: BasicMatrixMul )
    project_delete = request.POST.get('delete', "")
    if project_delete != "":
        # extract leftmost directory from filename ( example: PROJ-{} )
        temp = filename.split("/")[0]
        # create full name of directory to delete ( example: PROJ-BasicMatrixMul )
        project_delete = temp.replace("{}", project_delete)
        # delete the directory ( example: G:/projects/PROJ-BasicMatrixMul )
        project.delete(root_path, project_delete)

    # load project list ( example: ['BasicMatrixMul', 'BasicSort'] )
    # project_list = project.get_list(root_path, schema_data[root_schema]['Filename'])
    project_list = project.get_list(root_path, filename)

    return render(request, 'index.html', {'title': title,
                                          'link': link,
                                          'root_schema': root_schema.split(".")[0],
                                          'project_list': project_list},
                  )


def js2ds(request):
    link = "/index/"

    # ENTITY LIST
    entity_list = []

    # PARAMETERS default is []
    parameters = []

    # ROOT_PATH directory of directory structure ( example: G:/projects )
    root_path = config.get('root')

    # SCHEMA_NAME name of schema file ( example: Project.atjs )
    schema_name = config.get('parent')
    schema_name = request.POST.get('schema_filename', schema_name)

    # ALL SCHEMA DATA from .atjs files # key -> name of schema # value -> json
    schema_data = schemas.get()

    # ENTITY_NAME from EDIT or ADD from /index/ ( example: BasicMatrixMul )
    entity_name = request.POST.get('edit', "")
    entity_name = request.POST.get('add', entity_name)
    entity_name = request.POST.get('Name', entity_name)
    # from ADD Entity /js2ds/ ( example: QuickSort )
    entity_name = request.POST.get('entity_name', entity_name)
    if entity_name != "":
        entity_list.append(entity_name)

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
        if schema_data[schema_name]["properties"][o]["type"] == "Entity []":
            for number in range(1,257):
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

            # INTEGER
            elif schema_data[schema_name]['properties'][o]['type'] in ["integer"]:
                if request.POST.get(o, "") == "":
                    existing_data[schema_name.split(".")[0]][o] = ""
                else:
                    existing_data[schema_name.split(".")[0]][o] = int(request.POST.get(o, ""))

            # DOUBLE
            elif schema_data[schema_name]['properties'][o]['type'] in ["double"]:
                if request.POST.get(o, "") == "":
                    existing_data[schema_name.split(".")[0]][o] = ""
                else:
                    existing_data[schema_name.split(".")[0]][o] = float(request.POST.get(o, ""))

            # FILE
            elif schema_data[schema_name]['properties'][o]['type'] in ["File"]:
                previous_filename = existing_data[schema_name.split(".")[0]][o]
                new_filename = request.POST.get(o, "")
                file_data = request.POST.get("textarea" + o, "")
                root = request.POST.get("root" + o, "")
                for i_par, par in enumerate(parameters):
                    dolar = "$" + str(i_par + 1)
                    root = root.replace(dolar, par)
                # delete old file and create new
                # example: G:/projects/PROJ-NoviProjekt/proj/doc/index.html
                if new_filename != previous_filename:
                    project.delete_file(root_path + '/' + root.replace("{}", entity_name) + '/' + previous_filename)
                # ERROR ERROR ENTITY NAME "" ?
                project.write(root_path + '/' + root.replace("{}", entity_name) + '/' + new_filename, file_data)
                existing_data[schema_name.split(".")[0]][o] = new_filename
                # END OF FILE

            # FILES
            elif schema_data[schema_name]['properties'][o]['type'] in ["Files"]:
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

            # ENTITY []
            elif schema_data[schema_name]['properties'][o]['type'] in ["Entity []"]:
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
                for key, value in schemas.get().items():
                    if key.split(".")[0] == e_type:
                        e_path += schemas.get()[e_type + ".atjs"]["Filename"]
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
                        project.delete_file(new_e_path.replace("{}", en_del))
                        # TODO
                        # there are still other files to delete
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
            JSON.populate(filename, schema_name, submit_add_name, root_path, e_parameters)
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
        existing_data = JSON.read(filename)
    else:
        JSON.create(filename)
        JSON.populate(filename, schema_name, entity_name, root_path, [])
        # in this case values are ""
        existing_data = JSON.read(filename)

    # array of order of displaying items
    order = schema_data[schema_name]['Order']

    # read all existing files for the textareas
    files = dict()
    for o in order:
        if schema_data[schema_name]['properties'][o]['type'] == "File":
            # example: PROJ-TestniProjekt/proj/doc
            path_part = schema_data[schema_name]['properties'][o]['root'].replace("{}", entity_name)
            for i_count, e_p in enumerate(parameters):
                dolar = "$" + str(i_count + 1)
                path_part = path_part.replace(dolar, e_p)
            # example: index.html
            last_part = existing_data[schema_name.split(".")[0]][o]
            # full path example: G:/projects/PROJ-TestniProjekt/proj/doc/index.html
            files[o] = (project.read(root_path + '/' + path_part + '/' + last_part))

    # name of files in type FILES
    files_download = dict()
    for o in order:
        if schema_data[schema_name]['properties'][o]['type'] == "Files":
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






    # -------- PRINTING ------- #
    print("===========END===========")
    print("entity_name =", entity_name)
    print("root_path =", root_path)
    print("schema_name =", schema_name)
    print("filename =", filename)
    print("order =", order)
    print("files =", files)
    print("files_download =", files_download)
    print("===========END===========")
    # --------  END ----------- #

    return render(request, 'js2ds.html', {'title': entity_name,
                                          'link': link,
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
