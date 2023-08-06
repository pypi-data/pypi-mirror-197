'''
Created on Mar. 16, 2023

@author: wearo
'''
import unittest
from yopycalc.calc import Calc

# import sys
# for i in sys.path:
#     print(i)
    

class TestCalc(unittest.TestCase):        
    def setUp(self):
        self.calc = Calc(4, 3)

    def test_add_positive(self):
        # self.assertEqual(self.calc.add(), 6, f"{__file__}: msg add Function is not working correctly")
        '''
        The __file__ in the above gives absolute path D:\RAVI\DynamicData_Projects\Study\WorkspaceOne\python_new_1\yopycalc\test\test_calc.py
        Not sure how to get relative path like test\test_calc.py
        '''
        self.assertEqual(self.calc.add(), 7, f"{__file__}: msg add Function is not working correctly")
        #the msg message only gets printed in case of test failure
        # print("add Function works correctly")

    def test_add_negative(self):
        self.assertNotEqual(self.calc.add(), 6, f"{__file__}: msg add Function is not working correctly")
    
    def test_mul_positive(self):
        self.assertEqual(self.calc.mul(), 12, f"{__file__}: msg mul Function is not working correctly")

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    suite = unittest.TestSuite()
    suite.addTest(TestCalc('test_add_positive')) 
    suite.addTest(TestCalc('test_add_negative')) 
    suite.addTest(TestCalc('test_mul_positive')) 
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())