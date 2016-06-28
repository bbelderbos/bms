import ConfigParser 
import glob
import os
from pprint import pprint as pp
import sys
from architecturerules import ArchitectureRules
from unitrules import UnitRules

config = ConfigParser.ConfigParser()
config.read("conf")
COL_WIDTH = int(config.get("constants", "col_width"))

def load_files(path):
  files = glob.glob(os.path.join(path, "*"+config.get("constants", "ext")))
  return [fi for fi in files if not os.path.basename(fi).startswith("test_")]

def file_to_list(fname):
  with open(fname) as f:
    return f.readlines()

def get_method_args(args):
  return [arg.strip() for arg in args.split(",") if not arg == "self"]

def get_methods(lines):
  methods = {}
  meth = False
  for li in lines:
    li = li.strip()
    if li.startswith("def "):
      meth, args = li.replace("def ", "").rstrip(":)") .split("(")
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

def create_big_header(s):
  s = " " + s + " "
  h = []
  h.append( "*" * COL_WIDTH )
  h.append( "*" * COL_WIDTH )
  h.append(s.center(COL_WIDTH,'*'))
  h.append( "*" * COL_WIDTH )
  h.append( "*" * COL_WIDTH )
  return "\n".join(h)

def create_header(s):
  h = [ "=" * COL_WIDTH ]
  h.append("* " + s)
  h.append("=" * COL_WIDTH)
  return "\n".join(h)

def create_separator(s, sep="-"):
  return "\n" + s + "\n" + sep * COL_WIDTH 
  
def apply_rules(code):
  out = []
  out.append("\n" + create_header("A. Unit checks / B. Module checks"))
  for fi in code:
    if not code[fi]: 
      continue
    out.append(create_separator(">> File: " +fi, sep="="))
    out.append(create_separator("A. units"))
    for method, method_details in code[fi].items():
      out.append("\n- method: %s()" % method)
      if method_details["args"]:
        out.append(" > args: %s" % ", ".join(method_details["args"]))
      else:
        out.append(" > no args")
      out.append(" - rule 1: short units (max 15 loc)")
      ur = UnitRules(method_details)
      out.append("  - %s" % str(ur.short_units()))
      out.append(" - rule 2: simple units (max 4 branch points)")
      out.append("  - %s" % str(ur.simple_units()))
      out.append(" - rule 3: duplicates")
      out.append("  - #TODO")
      out.append(" - rule 4: small interfaces (max 4 params)")
      out.append("  - %s" % str(ur.small_interfaces()))
    out.append(create_separator("B. modules"))
    out.append(" - rule 5: loose coupling modules")
    out.append("  - #TODO")
    out.append(" - rule 6: loose coupling component architecture")
    out.append("  - #TODO")
    out.append("\n")
  out.append("\n" + create_header("C. Overall architecture checks"))
  ar = ArchitectureRules(code)
  out.append(" - rule 7: balance components")
  out.append("  > a. max 9 files / components")
  out.append("  - %s" % str(ar.num_files_codebase()))
  out.append("  > b. +/- equally sized modules (max dev 0.71)")
  out.append("  - %s" % str(ar.similar_size_components()))
  out.append(" - rule 8: small code base (< 40K loc)")
  out.append("  - %s" % str(ar.total_size_code_base()))
  out.append("\n" + create_header("D. Overall best practices checks"))
  out.append(" - rule 9: test coverage")
  out.append("  - #TODO")
  out.append(" - rule 10: best practices")
  out.append("  - #TODO (if measurable)")
  return out

def print_output(path):
  print "\n" + create_big_header("Code quality of %s" % path)
  num_warnings = 0
  for o in out:
    print o,
    if ", False)" in o:
      num_warnings += 1
      print " " * (COL_WIDTH/2) + "<"*(COL_WIDTH/3),
    print
  print "\n\n" + create_header("SUMMARY")
  print "%d warning%s to review" % (num_warnings, ("s" if num_warnings != 1 else ""))


if __name__ == "__main__":
  if len(sys.argv) < 2: 
    print("specify codebase path in first arg")
    print("first arg not give, default to current dir")
    path = "."
  else:
    path = sys.argv[1]
  files = load_files(path)
  code = parse_files(files)
  #pp(code); sys.exit()
  out = apply_rules(code)
  print_output(path)
