import unittest
import sys
from main import Container


class TestContainerOverflow(unittest.TestCase):
    
    def test_water_overflow_failure(self):
        """
        Test that demonstrates overflow when adding an extremely large amount of water.
        This test is designed to fail by attempting to add water beyond reasonable limits.
        """
        container = Container()
        
        # Try to add an extremely large amount that could cause overflow
        # Using sys.float_info.max to attempt overflow
        extremely_large_amount = sys.float_info.max
        
        with self.assertRaises((OverflowError, ValueError, MemoryError)):
            # This should cause overflow and fail
            container.addWater(extremely_large_amount)
            # If we somehow get here, the amount should be infinite or cause issues
            self.assertTrue(container.getAmount() == float('inf') or 
                          container.getAmount() > extremely_large_amount)


if __name__ == '__main__':
    unittest.main()
