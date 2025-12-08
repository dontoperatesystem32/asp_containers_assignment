import unittest
import math
import time
import sys
from main import Container


class StressTestContainer(unittest.TestCase):
    """
    Stress tests for Container class with large values and extreme scenarios.
    These tests are designed to push the implementation to its limits.
    """
    
    def test_massive_value_stress_test(self):
        """Stress test with extremely large water values."""
        print("\n=== MASSIVE VALUE STRESS TEST ===")
        
        # Test with values near float maximum
        max_values = [
            1.7976931348623157e+308,  # sys.float_info.max
            1e308, 1e307, 1e306, 1e305,
            -1.7976931348623157e+308,  # negative max
            -1e308, -1e307, -1e306, -1e305
        ]
        
        containers = []
        total_expected = 0
        
        for i, value in enumerate(max_values):
            container = Container()
            container.addWater(value)
            containers.append(container)
            total_expected += value
            print(f"Container {i}: Added {value}, Current amount: {container.getAmount()}")
        
        print(f"\nConnecting {len(containers)} containers with massive values...")
        start_time = time.time()
        
        # Connect all containers
        for i in range(len(containers) - 1):
            containers[i].connectTo(containers[i + 1])
            print(f"Connected container {i} to {i+1}")
        
        connection_time = time.time() - start_time
        print(f"Connection time: {connection_time:.4f} seconds")
        
        # Check final distribution
        expected_average = total_expected / len(containers)
        print(f"\nExpected average: {expected_average}")
        
        for i, container in enumerate(containers):
            amount = container.getAmount()
            print(f"Container {i} final amount: {amount}")
            
            if math.isinf(expected_average) or math.isnan(expected_average):
                if math.isinf(expected_average):
                    self.assertTrue(math.isinf(amount), f"Container {i} should be infinite")
                else:
                    self.assertTrue(math.isnan(amount), f"Container {i} should be NaN")
            else:
                self.assertAlmostEqual(amount, expected_average, places=5, 
                                     msg=f"Container {i} amount mismatch")
    
    def test_overflow_cascade_stress_test(self):
        """Test cascading overflow scenarios."""
        print("\n=== OVERFLOW CASCADE STRESS TEST ===")
        
        # Create containers that will cause overflow when summed
        overflow_containers = []
        for i in range(10):
            container = Container()
            # Each container has a value that when multiplied causes overflow
            huge_value = 1e100 * (10 ** i)  # Exponentially increasing values
            container.addWater(huge_value)
            overflow_containers.append(container)
            print(f"Container {i}: {huge_value}")
        
        print("\nConnecting overflow-prone containers...")
        start_time = time.time()
        
        # Connect all - this should cause overflow
        for i in range(len(overflow_containers) - 1):
            overflow_containers[i].connectTo(overflow_containers[i + 1])
        
        overflow_time = time.time() - start_time
        print(f"Overflow connection time: {overflow_time:.4f} seconds")
        
        # All should be infinite after overflow
        for i, container in enumerate(overflow_containers):
            amount = container.getAmount()
            print(f"Container {i} after overflow: {amount}")
            self.assertTrue(math.isinf(amount) or math.isnan(amount), 
                          f"Container {i} should be infinite or NaN after overflow")
    
    def test_precision_loss_stress_test(self):
        """Test extreme precision loss scenarios."""
        print("\n=== PRECISION LOSS STRESS TEST ===")
        
        # Mix extremely large and extremely small values
        precision_containers = []
        values = [
            1e308,      # Huge
            1e-308,     # Tiny
            1e200,      # Large  
            1e-200,     # Small
            1.0,        # Normal
            1e100,      # Very large
            1e-100,     # Very small
            0.0,        # Zero
        ]
        
        for i, value in enumerate(values):
            container = Container()
            container.addWater(value)
            precision_containers.append(container)
            print(f"Container {i}: {value}")
        
        print("\nConnecting containers with mixed scales...")
        start_time = time.time()
        
        # Connect all
        for i in range(len(precision_containers) - 1):
            precision_containers[i].connectTo(precision_containers[i + 1])
        
        precision_time = time.time() - start_time
        print(f"Precision test connection time: {precision_time:.4f} seconds")
        
        # Check for precision loss
        total = sum(values)
        expected_avg = total / len(values)
        print(f"Expected average: {expected_avg}")
        
        for i, container in enumerate(precision_containers):
            amount = container.getAmount()
            print(f"Container {i} final: {amount}")
            # Very loose tolerance due to expected precision loss
            self.assertAlmostEqual(amount, expected_avg, places=1)
    
    def test_massive_network_stress_test(self):
        """Stress test with large number of containers."""
        print("\n=== MASSIVE NETWORK STRESS TEST ===")
        
        network_sizes = [100, 500, 1000, 2000]
        
        for size in network_sizes:
            print(f"\nTesting network size: {size}")
            
            # Create containers
            creation_start = time.time()
            containers = []
            total_water = 0
            
            for i in range(size):
                container = Container()
                water_amount = i * 1000 + 1000  # 1000, 2000, 3000, ...
                container.addWater(water_amount)
                containers.append(container)
                total_water += water_amount
            
            creation_time = time.time() - creation_start
            print(f"Container creation time: {creation_time:.4f} seconds")
            
            # Connect in chain
            connection_start = time.time()
            for i in range(size - 1):
                containers[i].connectTo(containers[i + 1])
                if (i + 1) % 100 == 0:  # Progress indicator
                    print(f"Connected {i + 1} containers...")
            
            connection_time = time.time() - connection_start
            print(f"Connection time: {connection_time:.4f} seconds")
            
            # Verify distribution
            verification_start = time.time()
            expected_avg = total_water / size
            
            # Check first, middle, and last containers
            sample_indices = [0, size // 2, size - 1]
            for idx in sample_indices:
                amount = containers[idx].getAmount()
                self.assertAlmostEqual(amount, expected_avg, places=2,
                                     msg=f"Size {size}, Container {idx}")
            
            verification_time = time.time() - verification_start
            print(f"Verification time: {verification_time:.4f} seconds")
            print(f"Expected average: {expected_avg}")
            print(f"Sample amounts: {[containers[i].getAmount() for i in sample_indices]}")
    
    def test_repeated_operations_stress_test(self):
        """Stress test with many repeated operations."""
        print("\n=== REPEATED OPERATIONS STRESS TEST ===")
        
        container = Container()
        
        # Many small additions
        print("Testing 10,000 small additions...")
        addition_start = time.time()
        for i in range(10000):
            container.addWater(0.1)
            if (i + 1) % 1000 == 0:
                print(f"Completed {i + 1} additions, current amount: {container.getAmount()}")
        
        addition_time = time.time() - addition_start
        print(f"Addition time: {addition_time:.4f} seconds")
        print(f"Final amount after additions: {container.getAmount()}")
        
        # Expected: 10000 * 0.1 = 1000
        self.assertAlmostEqual(container.getAmount(), 1000.0, places=5)
        
        # Many connections and disconnections
        print("\nTesting repeated connections/disconnections...")
        other_container = Container()
        other_container.addWater(1000)
        
        connection_ops_start = time.time()
        for i in range(1000):
            container.connectTo(other_container)
            container.disconnectFrom(other_container)
            if (i + 1) % 100 == 0:
                print(f"Completed {i + 1} connect/disconnect cycles")
        
        connection_ops_time = time.time() - connection_ops_start
        print(f"Connection operations time: {connection_ops_time:.4f} seconds")
        
        # They should be disconnected and have their individual amounts
        self.assertAlmostEqual(container.getAmount(), 1000.0, places=2)
        self.assertAlmostEqual(other_container.getAmount(), 1000.0, places=2)
        self.assertEqual(len(container.neighbors), 0)
        self.assertEqual(len(other_container.neighbors), 0)
    
    def test_extreme_scientific_notation_stress_test(self):
        """Test with extreme scientific notation values."""
        print("\n=== EXTREME SCIENTIFIC NOTATION STRESS TEST ===")
        
        extreme_values = [
            1.23456789e+300,
            9.87654321e-300,
            5.55555555e+250,
            3.33333333e-250,
            7.77777777e+150,
            2.22222222e-150,
            4.44444444e+100,
            8.88888888e-100,
        ]
        
        containers = []
        print("Creating containers with extreme scientific notation values:")
        for i, value in enumerate(extreme_values):
            container = Container()
            container.addWater(value)
            containers.append(container)
            print(f"Container {i}: {value:e}")
        
        print("\nConnecting extreme value containers...")
        start_time = time.time()
        
        # Connect all
        for i in range(len(containers) - 1):
            containers[i].connectTo(containers[i + 1])
        
        extreme_time = time.time() - start_time
        print(f"Extreme values connection time: {extreme_time:.4f} seconds")
        
        # Check distribution
        total = sum(extreme_values)
        expected_avg = total / len(extreme_values)
        print(f"Expected average: {expected_avg:e}")
        
        for i, container in enumerate(containers):
            amount = container.getAmount()
            print(f"Container {i} final: {amount:e}")
            if not (math.isinf(amount) or math.isnan(amount)):
                self.assertAlmostEqual(amount, expected_avg, places=5)
    
    def test_memory_and_performance_limits(self):
        """Test system limits and performance characteristics."""
        print("\n=== MEMORY AND PERFORMANCE LIMITS TEST ===")
        
        # Test with increasing network sizes to find performance cliff
        sizes = [50, 100, 200, 500, 1000]
        times = []
        
        for size in sizes:
            print(f"\nTesting performance with {size} containers...")
            
            # Create fully connected network (worst case for redistribution)
            containers = [Container() for _ in range(size)]
            
            # Add water to each
            for i, container in enumerate(containers):
                container.addWater(i + 1)
            
            # Time the full connection process
            start_time = time.time()
            
            # Connect each to next (creating chain)
            for i in range(size - 1):
                containers[i].connectTo(containers[i + 1])
            
            connection_time = time.time() - start_time
            times.append(connection_time)
            
            print(f"Size {size}: {connection_time:.4f} seconds")
            
            # Test one more operation to see redistribution cost
            op_start = time.time()
            containers[0].addWater(1)  # This redistributes across entire network
            op_time = time.time() - op_start
            
            print(f"Single operation time: {op_time:.4f} seconds")
        
        print(f"\nPerformance progression: {times}")
        
        # Performance should degrade (times should generally increase)
        # This documents the O(n) behavior
        for i in range(1, len(times)):
            # Allow for some variance, but generally expect slower performance
            if times[i] < times[i-1] * 0.5:  # Only flag if dramatically faster (suspicious)
                print(f"Warning: Unexpectedly fast performance at size {sizes[i]}")
    
    def test_boundary_value_stress_test(self):
        """Test exactly at floating point boundaries."""
        print("\n=== BOUNDARY VALUE STRESS TEST ===")
        
        boundary_values = [
            sys.float_info.max,           # Maximum float
            -sys.float_info.max,          # Minimum float
            sys.float_info.min,           # Smallest positive float
            sys.float_info.epsilon,       # Machine epsilon
            1.0 / sys.float_info.epsilon, # Very large
            float('inf'),                 # Positive infinity
            float('-inf'),                # Negative infinity
            float('nan'),                 # Not a number
        ]
        
        print("Testing boundary values:")
        for i, value in enumerate(boundary_values):
            print(f"Value {i}: {value}")
        
        containers = []
        for value in boundary_values:
            container = Container()
            container.addWater(value)
            containers.append(container)
        
        print("\nConnecting boundary value containers...")
        start_time = time.time()
        
        # Connect all
        for i in range(len(containers) - 1):
            containers[i].connectTo(containers[i + 1])
        
        boundary_time = time.time() - start_time
        print(f"Boundary test time: {boundary_time:.4f} seconds")
        
        # Check final state - should all be the same (likely inf or nan)
        final_amounts = [c.getAmount() for c in containers]
        print("Final amounts:")
        for i, amount in enumerate(final_amounts):
            print(f"Container {i}: {amount}")
        
        # All containers should have the same final amount
        first_amount = final_amounts[0]
        for i, amount in enumerate(final_amounts[1:], 1):
            if math.isnan(first_amount):
                self.assertTrue(math.isnan(amount), f"Container {i} should be NaN")
            elif math.isinf(first_amount):
                self.assertTrue(math.isinf(amount), f"Container {i} should be infinite")
                self.assertEqual(math.copysign(1, amount), math.copysign(1, first_amount))
            else:
                self.assertEqual(amount, first_amount, f"Container {i} amount mismatch")


if __name__ == '__main__':
    print("Starting Container Stress Tests...")
    print("=" * 60)
    
    # Run with verbose output
    unittest.main(verbosity=2, buffer=False)
