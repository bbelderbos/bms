import ConfigParser 
import glob
import os
from pprint import pprint as pp
import sys
from architecturerules import ArchitectureRules
from unitrules import UnitRules

config = ConfigParser.ConfigParser()
config.read("conf")

def load_files(path):
  files = glob.glob(os.path.join(path, "*"+config.get("constants", "ext")))
  return [fi for fi in files if not fi.startswith("test_")]

def file_to_list(fname):
  with open(fname) as f:
    return f.readlines()

def get_method_args(args):
  return [arg.strip() for arg in args.split(",") if not arg == "self"]

def get_methods(lines):
  methods = {}
  meth = False
  for li in lines:
    if li.lstrip().startswith("def "):
      method = li.replace("def ", "").rstrip().rstrip(":)") 
      meth, args = method.split("(")
      methods[meth] = {
        "lines" : [],
        "args"  : get_method_args(args), 
      }
    if "if __name__ == \"__main__\":" in li:
      break 
    elif meth:
      methods[meth]["lines"].append(li)
  return methods

def parse_files(files):
  code = {}
  for fi in files:
    code[fi] = get_methods(file_to_list(fi)) 
  return code

def apply_rules(code):
  for fi in code:
    print "=" * 50
    print "* file: " + fi
    print "=" * 50
    print "\nA. Unit checks"
    for method, method_details in code[fi].items():
      print "\n- method: " + method
      print " - rule 1: short units"
      ur = UnitRules(method_details)
      print "  - %s" % str(ur.short_units())
      print " - rule 2: simple units"
      print "  - %s" % str(ur.simple_units())
      print " - rule 3: duplicates"
      print "  - TODO"
      print " - rule 4: small interfaces"
      print "  - %s" % str(ur.small_interfaces())
    print "\nB. Module (file) checks"
    print " - rule 5: loose coupling modules"
    print "  - TODO"
    print " - rule 6: loose coupling component architecture"
    print "  - TODO"
  print "\nC. Overal architecture checks"
  ar = ArchitectureRules(code)
  print " - rule 7: balance components"
  print "  > a. max 9 components"
  print "  - %s" % str(ar.num_files_codebase())
  print "  > b. equally sized modules"
  print "  - %s" % str(ar.similar_size_components())
  print " - rule 8: small code base"
  print "  - %s" % str(ar.total_size_code_base())
  print "\nD. Overal best practices checks"
  print " - rule 9: test coverage"
  print "  - TODO"
  print " - rule 10: best practices"
  print "  - TODO"

if __name__ == "__main__":
  if len(sys.argv) < 2: 
    print("specify codebase path in first arg")
    print("first arg not give, default to current dir")
    path = ""
  else:
    pp(deviations)
    path = sys.argv[1]
  files = load_files(path)
  code = parse_files(files)
  scores = apply_rules(code)
