import os
import shutil


# return list of projects in given path
# path ( example: G:/projects )
# filename ( example: PROJ-{}/proj/{}.atp )
def get_list(path, filename):
    # get directory from filename ( example: PROJ-{} )
    directory = filename.split("/")[0]
    # create empty project list
    project_list = []

    # read all files in directory, excluding directories
    # and extracts the value from {}
    for f in os.listdir(path):
        for p in directory.split("{}"):
            f = f.replace(p, "")
        project_list.append(f)
    return project_list


# deletes whole directory tree
# path ( example: G:/projects )
# directory ( example: PROJ-BasicMatrixMul )
def delete(path, directory):
    # delete ( example: G:/projects/PROJ-BasicMatrixMul )
    if os.path.isdir(path + '/' + directory):
        shutil.rmtree(path + '/' + directory)


# del tree
def del_tree(path):
    # delete ( example: G:/projects/PROJ-BasicMatrixMul )
    if os.path.isdir(path):
        shutil.rmtree(path)


# write to file
def write(filename, data):
    if "." in filename:
        with open(filename, 'wb') as out:
            out.write(str.encode(data))


# delete file
def delete_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)


# read from file
def read(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as my_file:
            data = my_file.read()
        return data


def upload(directory, file_object):
    # 'wb' stands for write and byte
    # our f variable is a byte object
    print("writing to file: ")
    with open(directory + '/' + str(file_object), 'wb') as out:
        out.write(file_object.read())
