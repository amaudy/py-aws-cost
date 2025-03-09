"""Formatters for AWS Cost Explorer data."""

import json
from typing import Dict, Any, TextIO, Optional
import sys


class CostFormatter:
    """Base class for cost data formatters."""
    
    def format(self, cost_data: Dict[str, Any]) -> str:
        """Format the cost data into a string representation."""
        raise NotImplementedError("Subclasses must implement format()")
    
    def output(self, cost_data: Dict[str, Any], output_stream: Optional[TextIO] = None) -> None:
        """
        Format and output the cost data.
        
        Args:
            cost_data: The cost data to format and output
            output_stream: Stream to write the output to (defaults to sys.stdout)
        """
        output_stream = output_stream or sys.stdout
        output_stream.write(self.format(cost_data))


class PrettyFormatter(CostFormatter):
    """Pretty-prints cost data in a human-readable format."""
    
    def format(self, cost_data: Dict[str, Any]) -> str:
        """Format cost data as pretty-printed text."""
        result = ["\n===== AWS COST REPORT =====\n"]
        
        for period in cost_data.get('ResultsByTime', []):
            start_date = period['TimePeriod']['Start']
            end_date = period['TimePeriod']['End']
            
            result.append(f"Period: {start_date} to {end_date}")
            result.append("Costs:")
            
            for metric_name, metric_data in period['Total'].items():
                amount = float(metric_data['Amount'])
                unit = metric_data['Unit']
                
                # Only show cost metrics with non-zero amounts or if it's a usage quantity
                if amount > 0 or metric_name == "UsageQuantity":
                    result.append(f"  {metric_name}: {amount:.2f} {unit}")
            
            if period.get('Estimated', False):
                result.append("  (Estimated: Yes)")
            
            result.append("")
        
        result.append("=========================\n")
        return "\n".join(result)


class JsonFormatter(CostFormatter):
    """Formats cost data as JSON."""
    
    def __init__(self, indent: int = 2):
        """
        Initialize the JSON formatter.
        
        Args:
            indent: Number of spaces for JSON indentation
        """
        self.indent = indent
    
    def format(self, cost_data: Dict[str, Any]) -> str:
        """Format cost data as JSON."""
        return json.dumps(cost_data, indent=self.indent, default=str)


def get_formatter(format_type: str) -> CostFormatter:
    """
    Factory function to get the appropriate formatter.
    
    Args:
        format_type: Type of formatter ('pretty', 'json')
        
    Returns:
        An instance of the requested formatter
    
    Raises:
        ValueError: If format_type is not recognized
    """
    formatters = {
        'pretty': PrettyFormatter,
        'json': JsonFormatter
    }
    
    if format_type not in formatters:
        raise ValueError(f"Unknown format type: {format_type}. Valid types: {', '.join(formatters.keys())}")
    
    return formatters[format_type]()