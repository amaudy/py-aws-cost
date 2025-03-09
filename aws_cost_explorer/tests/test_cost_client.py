"""Unit tests for the cost_client module."""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from aws_cost_explorer.cost_client import CostExplorerClient


class TestCostExplorerClient(unittest.TestCase):
    """Test the CostExplorerClient class."""
    
    @patch('boto3.Session')
    def test_init_with_profile(self, mock_session):
        """Test initializing with AWS profile name."""
        # Setup mock
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        mock_ce_client = MagicMock()
        mock_session_instance.client.return_value = mock_ce_client
        
        # Create client with profile
        client = CostExplorerClient(profile='test-profile')
        
        # Verify session was created with the profile
        mock_session.assert_called_once_with(profile_name='test-profile')
        mock_session_instance.client.assert_called_once_with('ce')
        self.assertEqual(client.profile, 'test-profile')
        self.assertEqual(client.session, mock_session_instance)
        self.assertEqual(client.ce_client, mock_ce_client)
    
    @patch('boto3.Session')
    def test_init_with_session(self, mock_session):
        """Test initializing with existing boto3 session."""
        # Setup mock
        mock_session_instance = MagicMock()
        mock_ce_client = MagicMock()
        mock_session_instance.client.return_value = mock_ce_client
        
        # Create client with session
        client = CostExplorerClient(session=mock_session_instance)
        
        # Verify a new session wasn't created
        mock_session.assert_not_called()
        mock_session_instance.client.assert_called_once_with('ce')
        self.assertEqual(client.session, mock_session_instance)
    
    @patch('boto3.Session')
    def test_get_cost_and_usage_with_defaults(self, mock_session):
        """Test get_cost_and_usage with default parameters."""
        # Setup mock
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        mock_ce_client = MagicMock()
        mock_session_instance.client.return_value = mock_ce_client
        
        # Mock response
        mock_response = {'ResultsByTime': []}
        mock_ce_client.get_cost_and_usage.return_value = mock_response
        
        # Create client and call method
        client = CostExplorerClient()
        result = client.get_cost_and_usage()
        
        # Verify result and method calls
        self.assertEqual(result, mock_response)
        
        # Verify the parameters were correctly calculated (30 days ago to today)
        today = datetime.now()
        expected_start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        expected_end_date = today.strftime('%Y-%m-%d')
        
        mock_ce_client.get_cost_and_usage.assert_called_once()
        call_args = mock_ce_client.get_cost_and_usage.call_args[1]
        self.assertEqual(call_args['TimePeriod']['Start'], expected_start_date)
        self.assertEqual(call_args['TimePeriod']['End'], expected_end_date)
        self.assertEqual(call_args['Granularity'], 'DAILY')
        self.assertEqual(call_args['Metrics'], ['BlendedCost', 'UnblendedCost', 'UsageQuantity'])
    
    @patch('boto3.Session')
    def test_get_cost_and_usage_with_parameters(self, mock_session):
        """Test get_cost_and_usage with custom parameters."""
        # Setup mock
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        mock_ce_client = MagicMock()
        mock_session_instance.client.return_value = mock_ce_client
        
        # Mock response
        mock_response = {'ResultsByTime': []}
        mock_ce_client.get_cost_and_usage.return_value = mock_response
        
        # Create client and call method with custom parameters
        client = CostExplorerClient()
        result = client.get_cost_and_usage(
            start_date='2023-01-01',
            end_date='2023-01-31',
            granularity='MONTHLY',
            metrics=['BlendedCost']
        )
        
        # Verify result and method calls
        self.assertEqual(result, mock_response)
        
        mock_ce_client.get_cost_and_usage.assert_called_once()
        call_args = mock_ce_client.get_cost_and_usage.call_args[1]
        self.assertEqual(call_args['TimePeriod']['Start'], '2023-01-01')
        self.assertEqual(call_args['TimePeriod']['End'], '2023-01-31')
        self.assertEqual(call_args['Granularity'], 'MONTHLY')
        self.assertEqual(call_args['Metrics'], ['BlendedCost'])


if __name__ == '__main__':
    unittest.main()