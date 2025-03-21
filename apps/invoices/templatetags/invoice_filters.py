from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def filter_by_currency(monthly_totals, currency):
    """Filter monthly totals by currency"""
    if not monthly_totals:
        print("Warning: monthly_totals is empty")
        return []
    
    filtered = [total for total in monthly_totals if total.get('currency_code') == currency]
    print(f"Filtering for {currency}:", filtered)  # Debug print
    return filtered

@register.filter
def sum_field(totals, field):
    """Sum a specific field from the totals"""
    if not totals:
        print(f"Warning: no totals to sum for field {field}")
        return 0
        
    try:
        total = sum(float(total.get(field, 0)) for total in totals)
        print(f"Sum for {field}:", total)  # Debug print
        return total
    except Exception as e:
        print(f"Error summing {field}:", str(e))  # Debug print
        return 0

@register.filter
def avg_field(totals, field):
    """Calculate average for a specific field"""
    try:
        if not totals:
            return 0
        values = [float(total.get(field, 0)) for total in totals]
        avg = sum(values) / len(values) if values else 0
        print(f"Average for {field}:", avg)  # Debug print
        return avg
    except Exception as e:
        print(f"Error averaging {field}:", e)  # Debug print
        return 0




