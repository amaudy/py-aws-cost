#!/usr/bin/env python3
"""
AWS Daily Cost Query Script
--------------------------
This script uses the AWS Cost Explorer API to fetch daily costs for your AWS account.
It requires the boto3 library and proper AWS credentials configured.
"""

import boto3
import datetime
import argparse
import json
from dateutil.relativedelta import relativedelta


def get_daily_costs(start_date=None, end_date=None, granularity='DAILY', metrics=None, profile=None):
    """
    Query AWS Cost Explorer for cost data.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date (str): End date in YYYY-MM-DD format. Defaults to today.
        granularity (str): Time granularity (DAILY, MONTHLY, etc.)
        metrics (list): Cost metrics to retrieve.
        profile (str): AWS profile name to use.
        
    Returns:
        dict: Cost data from AWS Cost Explorer
    """
    # Default to yesterday and today if dates not provided
    if not start_date:
        start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    if not metrics:
        metrics = ['BlendedCost', 'UnblendedCost', 'UsageQuantity']
    
    # Create session with optional profile
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    ce_client = session.client('ce')
    
    # Request cost data
    response = ce_client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity=granularity,
        Metrics=metrics
    )
    
    return response


def pretty_print_costs(cost_data):
    """
    Format and print cost data in a readable way.
    
    Args:
        cost_data (dict): Cost data from AWS Cost Explorer
    """
    print("\n===== AWS COST REPORT =====\n")
    
    for result in cost_data.get('ResultsByTime', []):
        start_date = result['TimePeriod']['Start']
        end_date = result['TimePeriod']['End']
        
        print(f"Period: {start_date} to {end_date}")
        print("Costs:")
        
        for metric_name, metric_data in result['Total'].items():
            amount = float(metric_data['Amount'])
            unit = metric_data['Unit']
            
            # Only show cost metrics with non-zero amounts or if it's a usage quantity
            if amount > 0 or metric_name == "UsageQuantity":
                print(f"  {metric_name}: {amount:.2f} {unit}")
        
        if result.get('Estimated', False):
            print("  (Estimated: Yes)")
        
        print("")
    
    print("=========================\n")


def main():
    """Main function to parse arguments and call the cost query function."""
    parser = argparse.ArgumentParser(description='Query AWS Cost Explorer for daily costs')
    parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    parser.add_argument('--profile', help='AWS profile name')
    parser.add_argument('--days', type=int, help='Number of days to look back')
    parser.add_argument('--month', action='store_true', help='View current month to date')
    parser.add_argument('--previous-month', action='store_true', help='View previous month')
    parser.add_argument('--output', choices=['pretty', 'json'], default='pretty',
                       help='Output format (pretty or json)')
    
    args = parser.parse_args()
    
    start_date = args.start
    end_date = args.end
    
    # Handle specific time periods
    today = datetime.datetime.now().date()
    
    if args.days:
        start_date = (today - datetime.timedelta(days=args.days)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
    
    if args.month:
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
    
    if args.previous_month:
        first_of_month = today.replace(day=1)
        last_month = first_of_month - relativedelta(months=1)
        start_date = last_month.strftime('%Y-%m-%d')
        end_date = (first_of_month - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Calculate tomorrow for cost explorer end date (which is exclusive)
    if end_date:
        end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        end_date = (end_date_obj + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Query costs
    response = get_daily_costs(
        start_date=start_date,
        end_date=end_date,
        profile=args.profile
    )
    
    # Output results
    if args.output == 'pretty':
        pretty_print_costs(response)
    else:
        print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    main()