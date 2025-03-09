# AWS Cost Query Tool

A Python utility for querying AWS Cost Explorer API to retrieve daily, monthly, or custom date range cost information for your AWS accounts.

## Features

- Query costs for specific date ranges
- Support for multiple AWS profiles
- View costs for the current month, previous month, or specific number of days
- Output in either pretty-printed format or JSON
- Uses AWS Cost Explorer API via boto3

## Prerequisites

- Python 3.6+
- AWS CLI configured with valid credentials
- Required Python packages:
  - boto3
  - python-dateutil

## Installation

1. Clone this repository
2. Set up a virtual environment (recommended)

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install required packages
pip install boto3 python-dateutil
```

## Usage

```bash
# Basic usage - shows costs for the last 30 days
python query_aws_costs.py

# View costs from a specific date range
python query_aws_costs.py --start 2023-01-01 --end 2023-01-31

# View costs for the current month to date
python query_aws_costs.py --month

# View costs for the previous month
python query_aws_costs.py --previous-month

# View costs for the last N days
python query_aws_costs.py --days 7

# Use a specific AWS profile
python query_aws_costs.py --profile my-aws-profile

# Output in JSON format
python query_aws_costs.py --output json
```

## Example Output

```
===== AWS COST REPORT =====

Period: 2023-03-01 to 2023-03-02
Costs:
  BlendedCost: 12.34 USD
  UnblendedCost: 12.34 USD
  UsageQuantity: 3203.42 N/A
  (Estimated: Yes)

...

=========================
```

## AWS Permissions

The IAM user or role associated with the profile must have permissions to access Cost Explorer data. At minimum, you need the following IAM permission:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage"
      ],
      "Resource": "*"
    }
  ]
}
```

## How It Works

The script uses the AWS SDK for Python (boto3) to interact with the AWS Cost Explorer API. It formats queries based on your parameters and displays the results in a readable format or as raw JSON data.

## License

MIT