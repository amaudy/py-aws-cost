"""AWS Cost Explorer client module for retrieving cost data."""

import boto3
import datetime
from typing import Dict, List, Optional, Any


class CostExplorerClient:
    """Client for interacting with AWS Cost Explorer."""

    def __init__(self, profile: Optional[str] = None, session: Optional[boto3.Session] = None):
        """
        Initialize the Cost Explorer client.
        
        Args:
            profile: AWS profile name to use
            session: Existing boto3 session (if provided, profile is ignored)
        """
        self.profile = profile
        
        if session:
            self.session = session
        else:
            self.session = boto3.Session(profile_name=profile) if profile else boto3.Session()
            
        self.ce_client = self.session.client('ce')
    
    def get_cost_and_usage(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = 'DAILY',
        metrics: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Query AWS Cost Explorer for cost data.
        
        Args:
            start_date: Start date in YYYY-MM-DD format. Defaults to 30 days ago.
            end_date: End date in YYYY-MM-DD format. Defaults to today.
            granularity: Time granularity (DAILY, MONTHLY, etc.)
            metrics: Cost metrics to retrieve.
            
        Returns:
            Cost data from AWS Cost Explorer
        """
        # Default to 30 days ago and today if dates not provided
        if not start_date:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if not metrics:
            metrics = ['BlendedCost', 'UnblendedCost', 'UsageQuantity']
        
        # Request cost data
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity=granularity,
            Metrics=metrics
        )
        
        return response