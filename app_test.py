import unittest
from app import calculateSum

class myTest(unittest.TestCase):

    def testFunction(self):
        self.assertEqual(calculateSum(1,1), 2)
        self.assertEqual(calculateSum(1,-1), 0)
        
if __name__ == '__main__':
<<<<<<< HEAD
    unittest.main()
=======
    unittest.main()
>>>>>>> 0f871c7b4a87710fade838ff481300d8efbad838
