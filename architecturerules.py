import ConfigParser 
from pprint import pprint as pp

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

  def similar_size_components(self):
    sizes = self.locs.values()
    mean = float(sum(sizes)) / len(sizes)
    deviations = []
    for s in sizes:
      dev = abs((s - mean)) / mean
      deviations.append(dev)
    for dev in sorted(deviations):
      if dev > float(config.get("archrules", "mod_size_deviation")):
        return dev, False
    return dev, True

  def total_size_code_base(self):
    tot_loc = sum(self.locs.values())
    return tot_loc, tot_loc < config.get("archrules", "total_loc")
