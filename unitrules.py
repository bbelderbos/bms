import ConfigParser 
from pprint import pprint as pp
import sys

config = ConfigParser.ConfigParser()
config.read("conf")

class UnitRules:
  
  def __init__(self, data):
    self.lines = data["lines"]
    self.args = data["args"]
    self.cleaned_lines = self._clean_lines()

  def _clean_lines(self):
    lines = []
    for li in self.lines:
      li = li.strip() 
      if li.startswith("def "):
        continue
      if not li:
        continue 
      if li.startswith(("#", '"""')):
        continue
      lines.append(li)
    return lines

  def short_units(self):
    loc = len(self.cleaned_lines)
    return loc, \
      loc < (int(config.get("unitrules", "unit_size")) + 1)

  def _add_count(self, branch_strings, li):
      for bs in branch_strings:
        if bs in (" and ", " or ") and li.startswith("if "):
          return 2
        if li.startswith(bs):
          return 1
      return 0

  def simple_units(self):
    branch_strings = config.get("constants", "branch_strings").split("|")
    count = 0
    for li in self.cleaned_lines:
      count += self._add_count(branch_strings, li)
    return count, \
      count < (int(config.get("unitrules", "branch_points")) + 1)

  def small_interfaces(self):
    num_ifs = len(self.args)
    return num_ifs, \
      num_ifs < (int(config.get("unitrules", "num_params")) + 1)
      
