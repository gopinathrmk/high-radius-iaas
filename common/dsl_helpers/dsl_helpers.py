import json
import os
import keyword

# load a file into a string
def loadFileAsString(path):
    if os.path.isfile(path):
        text_file = open(path)
        data = text_file.read()
        text_file.close()
        return data
    else:
        print("File {} not found\n\n".format(path))
        exit(1)

# read the json inside the file, add all (key:value)s inside the json to the dict reference passed to the function (calling context should pass locals() for dict)
# input json example:
# {
#    "param_variable_name1": "param_vlue1",
#    "param_variable_name2": "param_vlue2",
#    ...
#    "param_variable_namen": "param_vluen"
# }
# result: each element added to dict --> key: parameter variable name, value: parameter value
# any key starting with "_comment" is considered as comment and skipped
def loadEnvVarsFromFile(path, dict):
    params = json.loads(loadFileAsString(path))
    failexec = False
    for param in params:
        if not param.lower().startswith("_comment"):
            if param in dict:
                print("ERROR - parameter {} name is duplicate. Check the parameters names inside all env files specified in the use case config\n\n".format(param))
                failexec = True
            elif not param.isidentifier() or keyword.iskeyword(param):
                print("ERROR - parameter name {} is not valid.".format(param))
                print("ERROR - Change the parameter name in order to respect following rules:")
                print("ERROR - must start with a letter or the underscore character")
                print("ERROR - cannot start with a number")
                print("ERROR - can only contain alpha-numeric characters and underscores (A-z, 0-9, and _ )")
                print("ERROR - cannot be any of the Python keywords\n\n")
                failexec = True
            else:
                dict[param] = params[param]
    return failexec


# list files inside the folder passed in path, add all (scriptnamvariable:scriptcontents) to the dict reference passed to the function (calling context should pass locals() for dict)
# result: each element added to dict --> key: script variable name, value: script contents
# example, a script inside the folder named pc_projects.py, will result in:  variable name: PC_PROJECTS, variable value: script file contents
def loadScriptsFromFolder(path, dict):
    scripts = os.listdir(path)
    failexec = False
    for script in scripts:
        fullpath = os.path.join(path, script)
        # skip folders
        if os.path.isfile(fullpath):
            if script.count('.') > 1:
                print("ERROR - script {} name not valid: multiple '.' characters not allowed\n\n".format(fullpath))
                failexec = True
            else:
                #script variable name is uppercase without extension
                scriptVariableName = (script.split('.')[0]).upper()
                if scriptVariableName in dict:
                    print("ERROR - script {} generated variable name {} is duplicate".format(fullpath,scriptVariableName))
                    print("ERROR - Check the file names inside all lib folders specified in the use case config")
                    print("ERROR - script names comparison check is not case sensitive")
                    print("ERROR - script names comparison check does not consider file extensions\n\n")
                    failexec = True
                elif not scriptVariableName.isidentifier() or keyword.iskeyword(scriptVariableName):
                    print("ERROR - script {} generated variable name {} is not valid.".format(fullpath,scriptVariableName))
                    print("ERROR - Change the file name (extension omitted) in order to respect following rules:")
                    print("ERROR - must start with a letter or the underscore character")
                    print("ERROR - cannot start with a number")
                    print("ERROR - can only contain alpha-numeric characters and underscores (A-z, 0-9, and _ )")
                    print("ERROR - cannot be any of the Python keywords\n\n")
                    failexec = True
                else:
                    dict[scriptVariableName] = loadFileAsString(fullpath)
    return failexec


def build_task_script(script_file_name, dict):
    script_var_names_list = []
    parents_history = []
    build_task_script_recursive(script_file_name=script_file_name, dict=dict, script_var_names_list=script_var_names_list, parents_history=parents_history)
    return '\n\n\n'.join([dict[script_var_name] for script_var_name in script_var_names_list])


def build_task_script_recursive(script_file_name, dict, script_var_names_list, parents_history):
    #script variable name is uppercase without extension
    script_variable_name = (script_file_name.split('.')[0]).upper()

    #script_var_names_list.insert(0,script_variable_name)
    #for cyclic dependency check, we track visited parents before recursive call
    parents_history.append(script_variable_name)

    # getting scripts used by this script in used_scripts_files_names --> children
    script_content = dict[script_variable_name]
    used_scripts_lines=[ line.strip("# \t").split("CALM_USES")[1] for line in script_content.split("\n") if line.strip("# \t").startswith("CALM_USES")
                                                                                                        and not(line.strip("# \t").endswith("CALM_USES"))
                       ]
    used_scripts_files_names =[]
    for used_scripts_line in used_scripts_lines:
        used_scripts_files_names.extend([script_file_name.strip(" \t") for script_file_name in used_scripts_line.split(',') if script_file_name.strip(" \t")!=""])
    used_scripts_files_names=list(set(used_scripts_files_names))

    # iterate on children
    for used_script_file_name in used_scripts_files_names:
        #current used script var name
        used_script_var_name = (used_script_file_name.split('.')[0]).upper()
        if not(used_script_var_name in dict):
            print("ERROR - file {} included in {} was not loaded".format(used_script_file_name, script_file_name))
            print("ERROR - check the file exists and the name spelling")
            exit(1)
        if used_script_var_name in parents_history:
            #child file already visited
            # --> ensures termination in case some cyclic dependency exists
            # --> ensures no redundant includes
            continue
        build_task_script_recursive(script_file_name=used_script_file_name, dict=dict, script_var_names_list=script_var_names_list, parents_history=parents_history)

    script_var_names_list.append(script_variable_name)

