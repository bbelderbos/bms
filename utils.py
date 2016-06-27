from pprint import pprint as pp
import re

class Utils:

  def file_to_list(self, fname, secondArg=None):
    try:
      with open(fname) as f:
        return f.readlines()
    except:
      raise
  
  def get_methods_signatures(self, lines):
    methods = {}
    for li in lines:
      li = li.strip()
      if li.startswith("def "):
        li = li.replace("def ", "").rstrip(":)")
        meth, args = li.split("(")
        methods[meth] = [arg.strip() for arg in args.split(",") if not arg == "self"]
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
      # assumes no empty lines in method (keep methods short!)
      if counting and self._line_is_comment(li):
        comments += 1 
      if counting and self._white_line(li):
        return i - start - comments
