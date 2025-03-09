"""Unit tests for the formatters module."""

import unittest
import json
import io
from aws_cost_explorer.formatters import (
    CostFormatter, PrettyFormatter, JsonFormatter, get_formatter
)


class TestFormatters(unittest.TestCase):
    """Test the formatter classes and functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Sample cost data for testing
        self.sample_cost_data = {
            "ResultsByTime": [
                {
                    "TimePeriod": {
                        "Start": "2023-06-01",
                        "End": "2023-06-02"
                    },
                    "Total": {
                        "BlendedCost": {
                            "Amount": "10.50",
                            "Unit": "USD"
                        },
                        "UnblendedCost": {
                            "Amount": "10.50",
                            "Unit": "USD"
                        },
                        "UsageQuantity": {
                            "Amount": "120.0",
                            "Unit": "N/A"
                        }
                    },
                    "Estimated": True
                },
                {
                    "TimePeriod": {
                        "Start": "2023-06-02",
                        "End": "2023-06-03"
                    },
                    "Total": {
                        "BlendedCost": {
                            "Amount": "0.00",
                            "Unit": "USD"
                        },
                        "UnblendedCost": {
                            "Amount": "0.00",
                            "Unit": "USD"
                        },
                        "UsageQuantity": {
                            "Amount": "50.0",
                            "Unit": "N/A"
                        }
                    },
                    "Estimated": False
                }
            ]
        }

    def test_get_formatter(self):
        """Test the formatter factory function."""
        pretty_formatter = get_formatter('pretty')
        json_formatter = get_formatter('json')
        
        self.assertIsInstance(pretty_formatter, PrettyFormatter)
        self.assertIsInstance(json_formatter, JsonFormatter)
        
        # Test with invalid format type
        with self.assertRaises(ValueError):
            get_formatter('invalid_format')

    def test_pretty_formatter(self):
        """Test the PrettyFormatter class."""
        formatter = PrettyFormatter()
        result = formatter.format(self.sample_cost_data)
        
        # Check that formatted output contains expected content
        self.assertIn("===== AWS COST REPORT =====", result)
        self.assertIn("Period: 2023-06-01 to 2023-06-02", result)
        self.assertIn("BlendedCost: 10.50 USD", result)
        self.assertIn("UsageQuantity: 120.00 N/A", result)
        self.assertIn("(Estimated: Yes)", result)
        
        # Check that zero cost metrics are not shown (except UsageQuantity)
        self.assertIn("UsageQuantity: 50.00 N/A", result)
        self.assertNotIn("BlendedCost: 0.00 USD", result)

    def test_json_formatter(self):
        """Test the JsonFormatter class."""
        formatter = JsonFormatter(indent=2)
        result = formatter.format(self.sample_cost_data)
        
        # Check that JSON is valid and matches original data
        parsed_result = json.loads(result)
        self.assertEqual(parsed_result, self.sample_cost_data)
        
        # Test with custom indentation
        formatter = JsonFormatter(indent=4)
        result = formatter.format({"test": "value"})
        self.assertEqual(result, '{\n    "test": "value"\n}')

    def test_output_method(self):
        """Test the output method of CostFormatter."""
        formatter = JsonFormatter()
        
        # Test output to a string buffer
        output_buffer = io.StringIO()
        formatter.output({"test": "value"}, output_buffer)
        
        output_buffer.seek(0)
        result = output_buffer.read()
        self.assertEqual(json.loads(result), {"test": "value"})


if __name__ == '__main__':
    unittest.main()