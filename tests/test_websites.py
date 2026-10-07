import unittest
import sys
import os

plugins_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Plugins'))
if plugins_dir not in sys.path:
    sys.path.insert(0, plugins_dir)

from websites import websites_dict

class TestWebsites(unittest.TestCase):
    def test_websites_dict(self):
        self.assertIsInstance(websites_dict, dict)
        self.assertIn("google", websites_dict)

if __name__ == "__main__":
    unittest.main()
