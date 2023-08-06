'''
Created on Mar. 12, 2023

@author: wearo
'''
import unittest
from yopycalc.calc import Calc

# import sys
# for i in sys.path:
#     print(i)
    

class TestCalc(unittest.TestCase):        
    def setUp(self):
        self.calc = Calc(2, 3)

    def test_add_positive(self):
        # self.assertEqual(self.calc.add(), 5, "msg add Function is not working correctly")
        # self.assertEqual(self.calc.add(), 6, f"{__file__}: msg add Function is not working correctly")
        self.assertEqual(self.calc.add(), 5, f"{__file__}: msg add Function is not working correctly")

        # print("add Function works correctly")

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    suite = unittest.TestSuite()
    suite.addTest(TestCalc('test_add_positive')) 
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())