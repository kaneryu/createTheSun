import unittest
from gameLogic import numberLogic

class numberLogicTests(unittest.TestCase):
    def test_magnitude(self):
        result = numberLogic.magnitude(1000)
        self.assertEqual(result, 1)
        
        result = numberLogic.magnitude(2000)
        self.assertEqual(result, 1)
        
        result = numberLogic.magnitude(10_000)
        self.assertEqual(result, 1)
        
        result = numberLogic.magnitude(100_000)
        self.assertEqual(result, 1)
        
        result = numberLogic.magnitude(1_000_000)
        self.assertEqual(result, 2)
        
        result = numberLogic.magnitude(1_000_000_000)
        self.assertEqual(result, 3)
        
        result = numberLogic.magnitude(1_000_000_000_000)
        self.assertEqual(result, 4)
        

if __name__ == '__main__':
    unittest.main()