import unittest

from src.config import *
from src.functions import *
from src.plot import plotNumericalChecks


class TestContinuity(unittest.TestCase):
    
    def test_continuity_random_velocities_false(self):
        """Test that continuity is not zero for random velocity fields."""
        N = 32
        vx = np.random.rand(N, N)
        vy = np.random.rand(N, N)
        
        absolute_divergence = np.abs(ddx(vx) + ddy(vy))
        
        self.assertGreater(np.max(absolute_divergence), 1e-10, "Divergence should not be zero for random velocities")
    
    def test_continuity_from_stream_function_true(self):
        """Test that continuity is approximately zero when velocities are derived from a stream function."""
        N = 32
        sigma = 1.0
        psi = getRandomStreamFunction(N, sigma)
        
        vx = ddy(psi)
        vy = -ddx(psi)
        
        divergence = ddx(vx) + ddy(vy)
        max_divergence = np.max(np.abs(divergence))
        
        # For velocities from stream function, divergence should be very small (numerical precision)
        self.assertLess(max_divergence, 1e-10, "Divergence should be close to zero for stream function derived velocities")
    

class TestNumericalChecks(unittest.TestCase):
    
    def test_numerical_checks_random_false(self):
        """Test that numerical checks are not zero for random fields."""
        N = 32
        psi = getRandomStreamFunction(N, 1.0)  # Random psi
        vx = np.random.rand(N, N)
        vy = np.random.rand(N, N)
        
        A = vx * ddx(psi) + vy * ddy(psi)
        B = vx**2 + vy**2 - ddx(psi)**2 - ddy(psi)**2
        
        max_A = np.max(np.abs(A))
        max_B = np.max(np.abs(B))
        
        # For random fields, checks should not be close to zero
        self.assertGreater(max_A, 1e-10, "Check A should not be zero for random fields")
        self.assertGreater(max_B, 1e-10, "Check B should not be zero for random fields")
    
    def test_numerical_checks_from_stream_function_true(self):
        """Test that numerical checks are approximately zero when velocities are derived from a stream function."""
        N = 32
        sigma = 1.0
        psi = getRandomStreamFunction(N, sigma)
        
        vx = ddy(psi)
        vy = -ddx(psi)
        
        A = vx * ddx(psi) + vy * ddy(psi)
        B = vx**2 + vy**2 - ddx(psi)**2 - ddy(psi)**2
        
        max_A = np.max(np.abs(A))
        max_B = np.max(np.abs(B))
        
        # For velocities from stream function, checks should be very small
        self.assertLess(max_A, 1e-10, "Check A should be close to zero for stream function derived velocities")
        self.assertLess(max_B, 1e-10, "Check B should be close to zero for stream function derived velocities")
    
    def test_plotNumericalChecks_runs(self):
        """Test that plotNumericalChecks runs without errors."""
        N = 10
        psi = getRandomStreamFunction(N, 1.0)
        vx = np.random.rand(N, N)
        vy = np.random.rand(N, N)
        
        # This should not raise an exception
        plotNumericalChecks(psi, vx, vy)


if __name__ == '__main__':
    unittest.main()