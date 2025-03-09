#!/usr/bin/env python3
"""
AWS Daily Cost Query Script
--------------------------
This script uses the AWS Cost Explorer API to fetch daily costs for your AWS account.
It requires the boto3 library and proper AWS credentials configured.
"""

import argparse
import sys

from aws_cost_explorer.cost_client import CostExplorerClient
from aws_cost_explorer.formatters import get_formatter
from aws_cost_explorer.date_utils import get_date_range


def parse_args(args=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Query AWS Cost Explorer for daily costs')
    parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    parser.add_argument('--profile', help='AWS profile name')
    parser.add_argument('--days', type=int, help='Number of days to look back')
    parser.add_argument('--month', action='store_true', help='View current month to date')
    parser.add_argument('--previous-month', action='store_true', help='View previous month')
    parser.add_argument(
        '--output', 
        choices=['pretty', 'json'], 
        default='pretty',
        help='Output format (pretty or json)'
    )
    parser.add_argument(
        '--granularity',
        choices=['DAILY', 'MONTHLY'],
        default='DAILY',
        help='Cost data granularity (DAILY or MONTHLY)'
    )
    
    return parser.parse_args(args)


def main(args=None):
    """Main function to parse arguments and call the cost query function."""
    parsed_args = parse_args(args)
    
    # Calculate date range based on parameters
    start_date, end_date = get_date_range(
        start_date=parsed_args.start,
        end_date=parsed_args.end,
        days=parsed_args.days,
        month=parsed_args.month,
        previous_month=parsed_args.previous_month
    )
    
    # Create cost explorer client and get cost data
    client = CostExplorerClient(profile=parsed_args.profile)
    response = client.get_cost_and_usage(
        start_date=start_date,
        end_date=end_date,
        granularity=parsed_args.granularity
    )
    
    # Format and output results
    formatter = get_formatter(parsed_args.output)
    formatter.output(response)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())