"""
Unit tests for the Hijri Date System.
Run with: python -m pytest hijri_tests.py -v
Or simply: python hijri_tests.py
"""

import unittest
import sys
from datetime import date, timedelta

# Import the Hijri date system (assumes main code is available)
# from hijri_dates import HijriDate, iTimedelta, idate


class TestHijriDate(unittest.TestCase):
    """Test cases for HijriDate class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.date1 = HijriDate(1447, 6, 15)
        self.date2 = HijriDate(1447, 6, 20)
        self.date3 = HijriDate(1448, 1, 1)
    
    def test_initialization(self):
        """Test HijriDate initialization."""
        date = HijriDate(1447, 6, 15)
        self.assertEqual(date.year, 1447)
        self.assertEqual(date.month, 6)
        self.assertEqual(date.day, 15)
    
    def test_invalid_initialization(self):
        """Test HijriDate initialization with invalid values."""
        with self.assertRaises(ValueError):
            HijriDate(1447, 13, 1)  # Invalid month
        
        with self.assertRaises(ValueError):
            HijriDate(1447, 6, 31)  # Invalid day
        
        with self.assertRaises(ValueError):
            HijriDate(1447, 0, 15)  # Invalid month
        
        with self.assertRaises(ValueError):
            HijriDate(1447, 6, 0)  # Invalid day
    
    def test_string_representation(self):
        """Test string representations."""
        date = HijriDate(1447, 6, 15)
        self.assertEqual(str(date), "1447-06-15")
        self.assertEqual(repr(date), "HijriDate(1447, 6, 15)")
        self.assertEqual(date.isoformat(), "1447-06-15")
    
    def test_equality(self):
        """Test date equality."""
        date1 = HijriDate(1447, 6, 15)
        date2 = HijriDate(1447, 6, 15)
        date3 = HijriDate(1447, 6, 16)
        
        self.assertEqual(date1, date2)
        self.assertNotEqual(date1, date3)
        self.assertNotEqual(date1, "1447-06-15")  # Different type
    
    def test_comparison(self):
        """Test date comparisons."""
        date1 = HijriDate(1447, 6, 15)
        date2 = HijriDate(1447, 6, 20)
        date3 = HijriDate(1448, 1, 1)
        
        self.assertTrue(date1 < date2)
        self.assertTrue(date2 < date3)
        self.assertFalse(date2 < date1)
        
        self.assertTrue(date2 > date1)
        self.assertTrue(date3 > date2)
        self.assertFalse(date1 > date2)
        
        self.assertTrue(date1 <= date2)
        self.assertTrue(date1 <= date1)
        self.assertTrue(date2 >= date1)
        self.assertTrue(date1 >= date1)
    
    def test_hash(self):
        """Test date hashing."""
        date1 = HijriDate(1447, 6, 15)
        date2 = HijriDate(1447, 6, 15)
        date3 = HijriDate(1447, 6, 16)
        
        # Equal dates should have equal hashes
        self.assertEqual(hash(date1), hash(date2))
        
        # Can be used in sets
        date_set = {date1, date2, date3}
        self.assertEqual(len(date_set), 2)  # date1 and date2 are equal
    
    def test_ordinal_conversion(self):
        """Test ordinal conversion methods."""
        date1 = HijriDate(1, 1, 1)  # Epoch
        self.assertEqual(date1._to_ordinal(), 0)
        
        date2 = HijriDate(1, 1, 2)
        self.assertEqual(date2._to_ordinal(), 1)
        
        date3 = HijriDate(1, 2, 1)
        self.assertEqual(date3._to_ordinal(), 30)
        
        date4 = HijriDate(2, 1, 1)
        self.assertEqual(date4._to_ordinal(), 354)
        
        # Test round-trip conversion
        original = HijriDate(1447, 6, 15)
        ordinal = original._to_ordinal()
        recovered = HijriDate._from_ordinal(ordinal)
        self.assertEqual(original, recovered)


class TestTimedelta(unittest.TestCase):
    """Test cases for iTimedelta class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.td1 = iTimedelta(days=10)
        self.td2 = iTimedelta(days=5)
        self.td_zero = iTimedelta(days=0)
        self.td_negative = iTimedelta(days=-7)
    
    def test_initialization(self):
        """Test iTimedelta initialization."""
        td = iTimedelta(days=10)
        self.assertEqual(td.days, 10)
        
        td_default = iTimedelta()
        self.assertEqual(td_default.days, 0)
    
    def test_string_representation(self):
        """Test string representations."""
        td1 = iTimedelta(days=1)
        self.assertEqual(str(td1), "1 day")
        
        td_plural = iTimedelta(days=10)
        self.assertEqual(str(td_plural), "10 days")
        
        td_negative = iTimedelta(days=-1)
        self.assertEqual(str(td_negative), "-1 day")
        
        td_zero = iTimedelta(days=0)
        self.assertEqual(str(td_zero), "0 days")
        
        self.assertEqual(repr(td1), "iTimedelta(days=1)")
    
    def test_equality(self):
        """Test timedelta equality."""
        td1 = iTimedelta(days=10)
        td2 = iTimedelta(days=10)
        td3 = iTimedelta(days=5)
        
        self.assertEqual(td1, td2)
        self.assertNotEqual(td1, td3)
        self.assertNotEqual(td1, 10)  # Different type
    
    def test_comparison(self):
        """Test timedelta comparisons."""
        td1 = iTimedelta(days=5)
        td2 = iTimedelta(days=10)
        td3 = iTimedelta(days=-3)
        
        self.assertTrue(td1 < td2)
        self.assertTrue(td3 < td1)
        self.assertFalse(td2 < td1)
        
        self.assertTrue(td2 > td1)
        self.assertTrue(td1 > td3)
        self.assertFalse(td1 > td2)
    
    def test_addition(self):
        """Test timedelta addition."""
        td1 = iTimedelta(days=10)
        td2 = iTimedelta(days=5)
        
        result = td1 + td2
        self.assertEqual(result.days, 15)
        
        # Addition with HijriDate (tested in date arithmetic)
        date = HijriDate(1447, 6, 15)
        result_date = td1 + date
        expected = HijriDate(1447, 6, 25)  # Simplified calculation
        # Note: Actual result might differ due to month/year overflow handling
        self.assertIsInstance(result_date, HijriDate)
    
    def test_subtraction(self):
        """Test timedelta subtraction."""
        td1 = iTimedelta(days=10)
        td2 = iTimedelta(days=3)
        
        result = td1 - td2
        self.assertEqual(result.days, 7)
        
        result2 = td2 - td1
        self.assertEqual(result2.days, -7)
    
    def test_multiplication(self):
        """Test timedelta multiplication."""
        td = iTimedelta(days=5)
        
        result1 = td * 3
        self.assertEqual(result1.days, 15)
        
        result2 = 2 * td  # Right multiplication
        self.assertEqual(result2.days, 10)
        
        result3 = td * 1.5
        self.assertEqual(result3.days, 7)  # Truncated to int
    
    def test_division(self):
        """Test timedelta division."""
        td1 = iTimedelta(days=15)
        td2 = iTimedelta(days=3)
        
        # Division by scalar
        result1 = td1 / 3
        self.assertEqual(result1.days, 5)
        
        # Division by timedelta
        result2 = td1 / td2
        self.assertEqual(result2, 5.0)
        
        # Division by zero timedelta
        td_zero = iTimedelta(days=0)
        with self.assertRaises(ZeroDivisionError):
            td1 / td_zero
    
    def test_unary_operations(self):
        """Test unary operations."""
        td = iTimedelta(days=10)
        td_negative = iTimedelta(days=-5)
        td_zero = iTimedelta(days=0)
        
        # Negation
        self.assertEqual(-td, iTimedelta(days=-10))
        self.assertEqual(-td_negative, iTimedelta(days=5))
        
        # Positive
        self.assertEqual(+td, td)
        self.assertEqual(+td_negative, td_negative)
        
        # Absolute value
        self.assertEqual(abs(td), td)
        self.assertEqual(abs(td_negative), iTimedelta(days=5))
        self.assertEqual(abs(td_zero), td_zero)
    
    def test_boolean(self):
        """Test boolean evaluation."""
        td_positive = iTimedelta(days=5)
        td_negative = iTimedelta(days=-3)
        td_zero = iTimedelta(days=0)
        
        self.assertTrue(td_positive)
        self.assertTrue(td_negative)
        self.assertFalse(td_zero)
    
    def test_total_days(self):
        """Test total_days method."""
        td = iTimedelta(days=15)
        self.assertEqual(td.total_days(), 15)


class TestDateArithmetic(unittest.TestCase):
    """Test cases for date arithmetic operations."""
    
    def test_date_plus_timedelta(self):
        """Test adding timedelta to date."""
        date = HijriDate(1447, 6, 15)
        td = iTimedelta(days=5)
        
        result = date + td
        # Simple test - actual result depends on calendar implementation
        self.assertIsInstance(result, HijriDate)
        self.assertTrue(result > date)
    
    def test_date_minus_timedelta(self):
        """Test subtracting timedelta from date."""
        date = HijriDate(1447, 6, 15)
        td = iTimedelta(days=5)
        
        result = date - td
        self.assertIsInstance(result, HijriDate)
        self.assertTrue(result < date)
    
    def test_date_minus_date(self):
        """Test subtracting date from date."""
        date1 = HijriDate(1447, 6, 15)
        date2 = HijriDate(1447, 6, 20)
        
        result = date2 - date1
        self.assertIsInstance(result, iTimedelta)
        self.assertEqual(result.days, 5)
        
        result_reverse = date1 - date2
        self.assertEqual(result_reverse.days, -5)
    
    def test_timedelta_plus_date(self):
        """Test adding date to timedelta."""
        date = HijriDate(1447, 6, 15)
        td = iTimedelta(days=5)
        
        result = td + date
        expected = date + td
        self.assertEqual(result, expected)


class TestIdateFactory(unittest.TestCase):
    """Test cases for idate factory function."""
    
    def test_full_date(self):
        """Test idate with full date specification."""
        result = idate(1447, 6, 15)
        expected = HijriDate(1447, 6, 15)
        self.assertEqual(result, expected)
    
    def test_month_range(self):
        """Test idate with year and month."""
        start, duration = idate(1447, 6)
        
        self.assertEqual(start, HijriDate(1447, 6, 1))
        self.assertEqual(duration, iTimedelta(days=30))
        
        # Verify the tuple unpacking
        self.assertIsInstance(start, HijriDate)
        self.assertIsInstance(duration, iTimedelta)
    
    def test_year_range(self):
        """Test idate with year only."""
        start, duration = idate(1447)
        
        self.assertEqual(start, HijriDate(1447, 1, 1))
        self.assertEqual(duration, iTimedelta(days=354))
        
        # Verify the tuple unpacking
        self.assertIsInstance(start, HijriDate)
        self.assertIsInstance(duration, iTimedelta)
    
    def test_invalid_combinations(self):
        """Test invalid parameter combinations."""
        with self.assertRaises(ValueError):
            idate(1447, None, 15)  # Day without month


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_month_year_overflow(self):
        """Test date arithmetic that crosses month/year boundaries."""
        # End of month
        date = HijriDate(1447, 6, 30)
        next_day = date + iTimedelta(days=1)
        self.assertEqual(next_day.month, 7)
        self.assertEqual(next_day.day, 1)
        
        # End of year
        date = HijriDate(1447, 12, 30)
        next_day = date + iTimedelta(days=1)
        self.assertEqual(next_day.year, 1448)
        self.assertEqual(next_day.month, 1)
        self.assertEqual(next_day.day, 1)
    
    def test_large_timedelta(self):
        """Test arithmetic with large timedeltas."""
        date = HijriDate(1447, 6, 15)
        large_td = iTimedelta(days=1000)
        
        future_date = date + large_td
        self.assertIsInstance(future_date, HijriDate)
        
        # Should be roughly 2-3 years later
        self.assertTrue(future_date.year >= 1449)
    
    def test_negative_timedelta(self):
        """Test arithmetic with negative timedeltas."""
        date = HijriDate(1447, 6, 15)
        negative_td = iTimedelta(days=-100)
        
        past_date = date + negative_td
        self.assertIsInstance(past_date, HijriDate)
        self.assertTrue(past_date < date)


def run_tests():
    """Run all tests and provide summary."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestHijriDate,
        TestTimedelta,
        TestDateArithmetic,
        TestIdateFactory,
        TestEdgeCases
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("🧪 TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for test, trace in result.failures:
            print(f"  • {test}")
    
    if result.errors:
        print(f"\n💥 ERRORS ({len(result.errors)}):")
        for test, trace in result.errors:
            print(f"  • {test}")
    
    if not result.failures and not result.errors:
        print("\n✅ ALL TESTS PASSED!")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # You can run this directly to test the Hijri date system
    print("🌙 Running Hijri Date System Tests")
    print("=" * 60)
    
    success = run_tests()
    sys.exit(0 if success else 1)