#!/usr/bin/python


import getopt
import sys
from mod_pbxproj import XcodeProject

def help():
  print """    xcodemod.py options

    --help                   Show help information

    --addsubp                add sub project to project.
    --addfile                add file to project

    --pbxproj                project's project.pbxproj

    Params with addsubp
    --subpath                sub project path which should be the path of sub project's *.xcodeproj. Only be used with -addsubp
    --header_paths           add header paths to project. Only be used with -addsubp
    --sdk_dependencies       add sdk dependencies which are localed in iPhone's framework. Only be used with -addsubp
    --dev_dependencies       add develop dependencies wich are localed in Mac's framework. Only be used with -addsubp

    Params with addfile
    --filepath               file's localtion. Only be used with addfile
    --parent                 Which group will the file be added into, default is root_group
    --tree                   sourceTree.
    --create_build_files=    create build files which defined in mod_pbxproj for each PBX* object
    --weak
    --ignore_unknown_type    ignore unknown type
  """

def check_and_get_params_for_add_file(opts_dict):
  try:
    args = []
    opts = {}
    ret = False
    args.append(opts_dict["filepath"])
    for key in ["parent", "tree"]:
      if opts_dict.has_key(key):
        opts[key] = opts_dict[key]

    for key in ["create_build_files", "weak", "ignore_unknown_type"]:
      if opts_dict.has_key(key):
        opts[key] = True

    ret = True
  except TypeError as e:
    print "Invalid arguments"
  finally:
    return args, opts, ret



#--subpath                sub project path which should be the path of sub project's *.xcodeproj. Only be used with -addsubp
#--header_paths           add header paths to project, seperate by ":". Only be used with -addsubp
#--sdk_dependencies       add sdk dependencies which are localed in iPhone's framework, seperate by ":". Only be used with -addsubp
#--dev_dependencies       add develop dependencies wich are localed in Mac's framework, seperate by ":". Only be used with -addsubp
def check_and_get_params_for_add_subp(opts_dict):
  try:
    args = []
    opts = {}
    ret = False
    args.append(opts_dict["subpath"])
    for key in ["header_paths", "sdk_dependencies", "dev_dependencies"]:
      if opts_dict.has_key(key):
        opts[key] = opts_dict[key].split(":")

    ret = True
  except TypeError as e:
    print "Invalid arguments"
  finally:
    return args, opts, ret




def get_action_name(opts):
  has_help = False
  has_add_file = False
  has_add_subp = False
  for k, v in opts:
    if k == "--help":
      has_help = True

    if k == "--addsubp":
      has_add_subp = True

    if k == "--addfile":
      has_add_file = True

  return has_help and "help" or has_add_file and "add_file" or has_add_subp and "add_subproject_as_dependency"


if __name__ == "__main__":
  add_subprojects = ["addsubp", "subpath=", "header_paths=", "sdk_dependencies=", "dev_dependencies="]
  add_file = ["addfile", "filepath=", "parent=", "tree=", "create_build_files=", "weak=", "ignore_unknwon_type="]
  commons = ["xcode"]

  try:
    opts, args = getopt.getopt(sys.argv[1:], [], add_subprojects + add_file)
  except getopt.GetoptError as err:
    help()
    sys.exit(2)

  action = get_action_name(opts)

  if action == "help":
    help()
    exit(0)


  opts_dict = dict((k.lstrip("--"),v) for k, v in opts)
  pbxproj = opts_dict.get("pbxproj")

  if pbxproj is None or not os.path.isfile(pbxproj):
    help()
    exit(1)


  if action == "add_file":
    args, opts, ret = check_and_get_params_for_add_file(opts_dict)

  elif action == "add_subp":
    args, opts, ret = check_and_get_params_for_add_subp(opts_dict)

  else:
    help()
    exit(1)

  project = XcodeProject.Create(pbxproj)
  method = getattr(project, action)
  method(args, opts)
