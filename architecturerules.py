import ConfigParser 
from pprint import pprint as pp
import sys

config = ConfigParser.ConfigParser()
config.read("conf")

class ArchitectureRules:

  def __init__(self, code):
    self.code = code
    self.locs = {}
    for fi in self.code:
      self.locs[fi] = self._count_loc_file(fi)

  def _count_loc_file(self, fname):
    with open(fname) as f:
      return len([li for li in f.readlines() if li.strip() and not li.strip().startswith(("#", '"""'))])

  def num_files_codebase(self):
    num_files = len(self.code)
    return num_files, \
      num_files < config.get("archrules", "total_modules")

  def _gini(self, list_of_values):
    # http://planspace.org/2013/06/21/how-to-calculate-gini-coefficient-from-raw-data-in-python/
    sorted_list = sorted(list_of_values)
    height, area = 0, 0
    for value in sorted_list:
        height += value
        area += height - value / 2.
    fair_area = height * len(list_of_values) / 2.
    return (fair_area - area) / fair_area

  def similar_size_components(self):
    sizes = self.locs.values()
    gini = self._gini(sizes) 
    return gini, \
      gini < float(config.get("archrules", "gini_coefficient"))

  def total_size_code_base(self):
    tot_loc = sum(self.locs.values())
    return tot_loc, tot_loc < config.get("archrules", "total_loc")

if __name__ == "__main__":
  a = ArchitectureRules({})
  # 0.66
  print a._gini([0,0,1])
