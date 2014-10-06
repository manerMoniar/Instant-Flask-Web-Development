import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../sched'))
import app as m


class TestApp(unittest.TestCase):

    def test_to_delete(self):
        self.assertRaises(NotImplementedError, m.appointment_delete, 8)

if __name__ == '__main__':
    unittest.main()