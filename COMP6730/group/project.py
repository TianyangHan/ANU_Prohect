
# Group member:
# Tianyang Han, u7549569
# Congwei Yang, u7453564

# import sys
############################  1    ########################
def get_stdlib_packages():
    '''


    It is work to get the package's name in the Stdlib

    Returns
    -------
    sys_infor : It is work to get the information of python
    module_name_set : It is work to list the package's name in Stdlib

    '''
    import sys
    import isort
    sys_infor = sys.version_info
    module_name_set = eval("isort.stdlibs.py3" + str(sys_infor.minor) + ".stdlib")

    for i in module_name_set.copy():
        # traverse the list to get the package's name
        if i[0] == '_':
            module_name_set.remove(i)
    if 'this' in module_name_set:
        module_name_set.remove('this')
    if 'antigravity' in module_name_set:
        module_name_set.remove('antigravity')
    return sys_infor, module_name_set


def task1():
    '''
    It shows the information of computer system and python
    -------

    '''
    import platform
    sys_infor, module_name_set = get_stdlib_packages()
    module_name_list = list(module_name_set)
    module_name_list.sort()
    res1 = ""
    for i in module_name_list[0:5]:
        res1 += i + ", "
    res2 = ""
    for i in module_name_list[-6:-1]:
        res2 += i + ", "
    print("Python " + str(sys_infor.major) + "." + str(sys_infor.minor) + "." + str(sys_infor.micro), " on",
          str(platform.platform()))  # output the information of the computer.
    print("StdLib contains " + str(len(module_name_set)) + " external modules and packages:")
    print(res1[:-2] + " ... ", res2[:-2])
    del platform


############################  2    ########################

def get_real(module_name_list):
    '''
    It is work to make sure which package can not be imported

    Parameters
    ----------
    module_name_list : list
        It is the list of packages which is in Stdlib

    Returns
    -------
    imported : list
        It is the list which can be imported
    not_imported : list
        It is the list which can not be imported

    '''
    import importlib
    not_imported = []
    imported = []
    for i in module_name_list:
        try:
            pkg = importlib.import_module(i)
            # make sure the package can be imported
            imported.append(i)
            if i != "importlib":
                del pkg
        except:
            not_imported.append(i)
    return imported, not_imported


def task2():
    '''
    It shows every packages that can be imported
    -------

    '''
    sys_infor, module_name_set = get_stdlib_packages()
    module_name_list = list(module_name_set)
    module_name_list.sort()
    real, fake = get_real(module_name_list)
    res = ""
    for i in fake:
        res += i + ", "
    print("These StdLib packages on Python " + str(sys_infor.major) + "." + str(sys_infor.minor) + "." + str(
        sys_infor.micro) + " are not importable:")
    print(res[:-2])  # output every importable packages


############################  3    ########################

def module_dependency(imported, mod):
    '''
    It works to get the list of names of importable Stdlib packages and return
    the list of names of module which the module a_module depends.

    Parameters
    ----------
    imported : list
        It is the list of the names of importable module
    mod : the name of the importable module in Stdlib

    Returns
    -------
    depend : It is the importable module in Stdlib.
    count : Integer
        The number of the module which the a_module depends.

    '''
    import importlib
    import inspect
    count = 0
    pkg = importlib.import_module(mod)
    info = vars(pkg)
    depend = []
    for key, value in info.items():
        if inspect.ismodule(info[key]) and key in imported:  # make sure the package is allowed
            count += 1
            depend.append(value)
    del pkg
    return depend, count


def top_five_dependent_pkg(imported):
    '''
    It print the names of five most dependent Stdlib modules and the number of modules
    each of them depends on.

    Parameters
    ----------
    imported : list
        It is the list of the names of importable module.

    Returns
    -------
    None.

    '''
    res = {}
    for mod in imported:
        _, count = module_dependency(imported, mod)
        res[mod] = count

    sort_key = sorted(res, key=res.__getitem__)
    sort_key.reverse()
    for tmp in sort_key[0:5]:
        print(tmp, res[tmp])  # output the five most dependent module and the number of module


def find_core_modules(imported):
    '''
    It is the function which returns the list of all core modules in Stdlib

    Parameters
    ----------
    imported : list
        It is the list of the names of importable module.

    Returns
    -------
    res : list
        It is the list of all core modules in Stdlib.

    '''
    res = []
    for mod in imported:
        _, count = module_dependency(imported, mod)
        if count == 0:
            res.append(mod)
    return res  # output all core modules


def task3():
    '''
    It shows all core packages and five most dependent Stdlib packages
    -------
    None.

    '''
    sys_infor, module_name_set = get_stdlib_packages()
    module_name_list = list(module_name_set)
    module_name_list.sort()
    imported, not_imported = get_real(module_name_list)
    top_five_dependent_pkg(imported)  # output five most dependent module
    core = find_core_modules(imported)  # return a list of core module
    core_print = ""
    for i in core:
        core_print += i + ", "
    print("The " + str(len(core)) + " core packages are:")
    print(core_print[:-2])


############################  4    ########################

def explore_package(pkg_name):
    '''
    It will determine the type and read every python file

    Parameters
    ----------
    pkg_name : the name of Stdlib package.

    Returns
    -------
    file_code_line: integer
        the total number of lines in all python flies.
    num_cls: integer
        the total number of custom types a package defines.

    '''
    import re
    import importlib
    import os
    pkg = importlib.import_module(pkg_name)
    info = vars(pkg)
    for key, value in info.items():
        if key == "__file__" and (value[-3:] != ".so" and value[-4:] != ".ddl"):
            file_code_line = 0
            num_cls = 0
            if value[-11:] == "__init__.py":
                # num = len(pkg_name)
                for root, dirs, files in os.walk(value[:-12]):
                    for f in files:
                        if f[-3:] == ".py":
                            with open(os.path.join(root, f), 'rb') as file1:
                                file_code_line += file1.read().count(
                                    '\n'.encode())  # count the number of "\n" to count lines.
                                num_cls += cal_cls(os.path.join(root, f))  # count number of classes of this .py file
                                file1.close()
                    return (file_code_line, num_cls)
            else:
                with open(value, 'rb') as file1:
                    file_code_line += file1.read().count('\n'.encode())
                    num_cls += cal_cls(value)
                    file1.close()
                return (file_code_line, num_cls)
    return (0, 0)


def cal_cls(value):
    '''
    It is use to calculate the number of class in a python file

    Parameters
    ----------
    value : string
        a python file.

    Returns
    -------
    num_class : integer
        the number of class in a python file.

    '''

    num_class = 0
    flag = 0
    for count, line in enumerate(open(value, 'rb')):
        flag += line.count("\"\"\"".encode())  # keywords "class " is only valid when the times of "\"\"\"" %2 == 0
        if (line.__contains__("class ".encode()) and (line[-2:] == ':\n') and (flag % 2 == 0)):
            num_class += 1
    return num_class  # return the number of class in one python file


def task4():
    '''
    It shows the 5 most lines packages , 5 least lines packages,5 most classes packages and
    no classes packages in a python file.

    Returns
    -------
    None.

    '''
    sys_infor, module_name_set = get_stdlib_packages()
    module_name_list = list(module_name_set)
    module_name_list.sort()
    imported, not_imported = get_real(module_name_list)
    res_line = {}
    res_cls = {}
    for i in imported:  # for loop on each importable pkgs. and store their line number and class number respectively
        (file_code_line, num_cls) = explore_package(i)
        res_line[i] = file_code_line
        res_cls[i] = num_cls
    res_line = sorted(res_line, key=res_line.__getitem__)  # sorted by line number
    res_line.reverse()
    res_cls_sort = sorted(res_cls, key=res_cls.__getitem__)
    res_cls_sort.reverse()

    print_res_line_most = ""
    print_res_line_least = ""
    for i in res_line[0:5]:
        print_res_line_most += i + ", "  # output five most lines packages
    for i in res_line[-5:]:
        print_res_line_least += i + ", "  # output five least lines packages

    print_res_cls_most = ""
    print_res_cls_none = ""
    for i in res_cls_sort[0:5]:
        print_res_cls_most += i + ", "  # output five most classes packages
    for key, value in res_cls.items():
        if value == 0:
            print_res_cls_none += key + ", "  # output the result if no classes packages

    print("5 most lines packages:", print_res_line_most[:-2])
    print("5 least lines packages:", print_res_line_least[:-2])
    print("5 most classes packages:", print_res_cls_most[:-2])
    print("NO classes packages:", print_res_cls_none[:-2])


##############################  5       ############################

def recur(imported, path):
    '''
    It compute all cyclic dependencies in the Stdlib

    Parameters
    ----------
    imported : list
        It is the list of the names of importable module.
    path : list
        It is the list of the Stdlib package.

    Returns
    -------
    path : list
        It is the list of the Stdlib package.

    '''
    import importlib
    import inspect
    import os
    if len(path) > 2 and path[0] == path[-1]:
        return path  # return the list of cycle dependency.
    if len(path) > 1:
        pkg = importlib.import_module(path[-1])
        info = vars(pkg)
    else:
        pkg = importlib.import_module(path[0])
        info = vars(pkg)
    for key, value in info.items():
        if inspect.ismodule(info[key]) and key in imported:
            path.append(key)
            # print(path)
            recur(imported, path)
            path.pop()
    del importlib
    del inspect
    del pkg
    del os


def task5():
    '''
    It shows the cycle of dependency of the Stdlib packages

    Returns
    -------
    None.

    '''
    sys_infor, module_name_set = get_stdlib_packages()
    module_name_list = list(module_name_set)
    module_name_list.sort()
    imported, not_imported = get_real(module_name_list)
    # res = []
    path = []
    final_res = []
    for i in range(len(imported)):
        path.append(imported[i])
        res = recur(imported, path)
        final_res.append(
            res)  # return the list. Length of lists is the number of importable pkgs. Each element stores the cycle started by the pkgs, \
        # whose order is corresponding to the variable "imported" , if none ,then none
        # res = []
        path = []
    print("The StdLib packages form a cycle of dependency:")  # return the cycle of dependency.
    flag = 0
    for i in range(len(final_res)):
        if final_res[i] is not None:
            print(final_res[i])
            flag = 1
    if flag == 0:
        print("None of cyclic dependencies")


############################ task 6 ##############################
def task6():
    '''
    It create a visual representation of Stdlib as graph

    Returns
    -------
    None.

    '''
    import matplotlib.pyplot as plt
    import networkx as nx
    G = nx.DiGraph()  # create graph class
    import importlib
    import inspect
    sys_infor, module_name_set = get_stdlib_packages()
    module_name_list = list(module_name_set)
    module_name_list.sort()
    imported, not_imported = get_real(module_name_list)
    dic = {}
    for package in imported:
        pkg = importlib.import_module(package)
        info = vars(pkg)
        depend = []
        for key, value in info.items():
            if inspect.ismodule(info[key]) and key in imported:
                depend.append(key)
        dic[
            package] = depend  # create a dic, which stores the tuple denoting the edges(dependencies) of importable pkgs. \
        # The key of the dic is pkgs name, and corresponding to several values, representing its dependencies.
        del pkg

    edge_list = []
    for key, value in dic.items():
        for dep in value:
            edge_list.append((key, dep))

    G.add_nodes_from(imported)  # add nodes name
    G.add_edges_from(edge_list)  # add edges from dic
    pos = nx.circular_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=0.1, font_size=2, width=0.1, arrowsize=1.5, node_color='White',
            font_color='Crimson', node_shape='d', alpha=0.7)
    plt.xticks([])
    plt.yticks([])
    plt.savefig("./u7549569_task6.png", dpi = 1000)
    plt.show()


def analyse_stdlib():
    task1()
    task2()
    task3()
    task4()
    task5()



if __name__ == '__main__':
    NAME = 'Tianyang Han'
    ID   = 'u7549569'
    print(f'My name is {NAME}, my id is {ID}, and these are my findings for Project COMP1730.2022.S2')
    analyse_stdlib()
    task6()