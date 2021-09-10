import unittest
from app import calculateSum

class myTest(unittest.TestCase):

    def testFunction(self):
        self.assertEqual(calculateSum(1,1), 2)
        self.assertEqual(calculateSum(1,-1), 0)
        
if __name__ == '__main__':
    unittest.main()
