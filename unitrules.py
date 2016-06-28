import ConfigParser 
from pprint import pprint as pp

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

  def simple_units(self):
    branch_strings = config.get("constants", "branch_strings").split("|")
    count = 0
    for li in self.cleaned_lines:
      for bs in branch_strings:
        if bs in li:
          count += 1
    return count, \
      count < (int(config.get("unitrules", "branch_points")) + 1)

  def small_interfaces(self):
    num_ifs = len(self.args)
    return num_ifs, \
      num_ifs < (int(config.get("unitrules", "num_params")) + 1)
      
