"""Date utilities for AWS Cost Explorer."""

import datetime
from typing import Tuple, Optional
from dateutil.relativedelta import relativedelta


def get_date_range(
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None,
    days: Optional[int] = None,
    month: bool = False,
    previous_month: bool = False
) -> Tuple[str, str]:
    """
    Calculate the date range based on provided parameters.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        days: Number of days to look back from today
        month: Whether to use current month to date
        previous_month: Whether to use the previous month
        
    Returns:
        Tuple of (start_date, end_date) in YYYY-MM-DD format
    
    Note:
        End date is inclusive when passed in but will be converted to exclusive
        for AWS Cost Explorer which requires the end date to be exclusive.
    """
    today = datetime.datetime.now().date()
    
    # Process special date range options
    if days is not None:
        start_date = (today - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
    
    if month:
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
    
    if previous_month:
        first_of_month = today.replace(day=1)
        last_month = first_of_month - relativedelta(months=1)
        start_date = last_month.strftime('%Y-%m-%d')
        end_date = (first_of_month - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Default to 30 days ago and today if no dates or special options provided
    if not start_date and not end_date:
        start_date = (today - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
    
    # Make end date exclusive for AWS Cost Explorer
    if end_date:
        end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        end_date = (end_date_obj + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    return start_date, end_date