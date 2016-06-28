import csv
import glob
import os
from pprint import pprint as pp
import sys
from utils import Utils

u = Utils()
outfile = "results.csv"

def write_csv(lines):
  with open(outfile, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for li in lines:
      writer.writerow(li)

def get_source_files(files):
  sourcefiles = [fi for fi in files if not fi.startswith("test_")]
  testfiles = [fi for fi in files if fi not in sourcefiles]
  return sourcefiles, testfiles

def get_test_name(s):
  return "test_" + s

def main(codebase):
  files = glob.glob(os.path.join(codebase, "*.py"))
  (sourcefiles, testfiles) = get_source_files(files)
  header = ["file", "method", "loc", "args", "unittest"]
  clines = [header]
  for fi in sourcefiles:
    lines = u.file_to_list(fi)
    testlines = u.file_to_list(get_test_name(fi))
    methods = u.get_methods_signatures(lines)
    testmethods = u.get_methods_signatures(testlines)
    for method, args in methods.items():
      testmeth = get_test_name(method)
      loc = u.count_method_loc(lines, method)
      hastest = 1 if testmeth in testmethods else 0
      clines.append([fi, method, loc, len(args), hastest])
  write_csv(clines)
  
if __name__ == "__main__":
  if len(sys.argv) < 2: 
    print("specify codebase path in first arg")
    print("first arg not give, default to current dir")
    path = ""
  else:
    path = sys.argv[1]
  main(path)
  print "CSV %s written" % outfile 
