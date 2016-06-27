from pprint import pprint as pp
import re
import sys

class Utils:

  def file_to_list(self, fname):
    try:
      with open(fname) as f:
        return f.readlines()
    except:
      return []

  def _strip_method_name(self, li):
    return li.replace("def ", "").rstrip(":)")

  def _split_args(self, args):
    return [arg.strip() for arg in args.split(",") if not arg == "self"]

  def get_methods_signatures(self, lines):
    methods = {}
    for li in lines:
      li = li.strip()
      if li.startswith("def "):
        method = self._strip_method_name(li)
        meth, args = method.split("(")
        methods[meth] = self._split_args(args)
    return methods

  def _next_line_number(self, lineno):
    # trick from clean code book: use methods instead of comments
    return lineno + 1

  def _white_line(self, li):
    return not li

  def _line_is_comment(self, li):
    return li.startswith("#") or li.startswith('"""')

  def count_method_loc(self, lines, method):
    counting = False
    comments = 0
    for i, li in enumerate(lines, 1):
      li = li.strip()
      if li.startswith("def") and method in li:
        counting = True
        start = self._next_line_number(i)
      if counting and self._line_is_comment(li):
        comments += 1 
      # assumes no empty lines in method (keep methods short!)
      if counting and self._white_line(li):
        return i - start - comments


if __name__ == "__main__":
  u = Utils()
  lines = u.file_to_list(sys.argv[0])
  print u.count_method_loc(lines, "count_method_loc") == 11

