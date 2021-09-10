import unittest
from app import calculateSum

class myTest:

    def testFunction(unittest.TestCase):
        self.assertEqual(calculateSum(1,1) 2)
        self.assertEqual(calculateSum(1,-1), 0)
        
if __name__ == '__main__':
    unittest.main()
