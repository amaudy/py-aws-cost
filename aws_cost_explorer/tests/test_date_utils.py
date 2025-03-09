"""Unit tests for the date_utils module."""

import unittest
from datetime import datetime, timedelta
from freezegun import freeze_time
from aws_cost_explorer.date_utils import get_date_range


@freeze_time("2023-06-15")
class TestDateUtils(unittest.TestCase):
    """Test date utilities functions."""
    
    def test_get_date_range_default(self):
        """Test get_date_range with default parameters."""
        start_date, end_date = get_date_range()
        
        # Default should be 30 days ago to today+1
        expected_start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        expected_end = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        self.assertEqual(start_date, expected_start)
        self.assertEqual(end_date, expected_end)

    def test_get_date_range_explicit(self):
        """Test get_date_range with explicit dates."""
        start_date, end_date = get_date_range(
            start_date="2023-01-01",
            end_date="2023-01-31"
        )
        
        # End date should be exclusive (day after the provided date)
        self.assertEqual(start_date, "2023-01-01")
        self.assertEqual(end_date, "2023-02-01")

    def test_get_date_range_days(self):
        """Test get_date_range with days parameter."""
        start_date, end_date = get_date_range(days=7)
        
        expected_start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        expected_end = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        self.assertEqual(start_date, expected_start)
        self.assertEqual(end_date, expected_end)

    def test_get_date_range_current_month(self):
        """Test get_date_range with current month flag."""
        start_date, end_date = get_date_range(month=True)
        
        # First day of current month to tomorrow
        expected_start = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        expected_end = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        self.assertEqual(start_date, expected_start)
        self.assertEqual(end_date, expected_end)

    def test_get_date_range_previous_month(self):
        """Test get_date_range with previous month flag."""
        with freeze_time("2023-06-15"):
            start_date, end_date = get_date_range(previous_month=True)
            
            # May 1st to June 1st
            self.assertEqual(start_date, "2023-05-01")
            self.assertEqual(end_date, "2023-06-01")  # June 1 (exclusive)


if __name__ == '__main__':
    unittest.main()