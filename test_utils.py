from pprint import pprint as pp
import sys
import unittest
from utils import Utils

class TestUtils(unittest.TestCase):
  
  def setUp(self):
    self.u = Utils()
    self.testfile = sys.argv[0]
    self.modfile = sys.argv[0].replace("test_", "")
    self.testfile_lines = self.u.file_to_list(self.testfile)
    self.modfile_lines = self.u.file_to_list(self.modfile)
    self.extfile = "countMethodLinesTestFile.py"
    self.extfile_lines = self.u.file_to_list(self.extfile)
 
  def test_file_to_list(self):
    self.assertIsInstance(self.testfile_lines, list)
    self.assertIn("import unittest\n", self.testfile_lines)
    self.assertEqual(self.u.file_to_list(self.testfile+"_"), [])
    try:
      self.u.file_to_list(self.testfile+"_")
    except IOError:
      self.fail("file_to_list() raised IOError unexpectedly!")

  def test_get_methods_signatures(self):
    self.assertIn("test_file_to_list", self.u.get_methods_signatures(self.testfile_lines))
    self.assertIn("get_methods_signatures", self.u.get_methods_signatures(self.modfile_lines))
    self.assertIsInstance(self.u.get_methods_signatures(self.testfile_lines), dict)
    self.assertEqual(len(self.u.get_methods_signatures(self.modfile_lines)["file_to_list"]), 1)
    self.assertEqual(len(self.u.get_methods_signatures(self.modfile_lines)["get_methods_signatures"]), 1)

  def test_count_method_loc(self):
    self.assertEqual(self.u.count_method_loc(self.modfile_lines, "file_to_list"), 5)
    self.assertEqual(self.u.count_method_loc(self.modfile_lines, "_next_line_number"), 1)


if __name__ == "__main__":
  unittest.main()
