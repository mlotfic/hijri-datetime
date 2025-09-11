from .safe_get import safe_get
import json


def process_one_day_date_data(date_entry):
    # Validate date entry structure
    if (
        not date_entry or
        'hijri' not in date_entry or
        'gregorian' not in date_entry
    ):
        return None
    
    # Extract hijri and gregorian data directly from date entry
    hijri = date_entry.get('hijri', {})
    gregorian = date_entry.get('gregorian', {})    

    # Holiday information (serialize lists to JSON strings)
    holidays_dict = {
        'gregorian_date': gregorian.get('date', ''),
        'hijri_holidays': json.dumps(hijri.get('holidays', [])),
        'hijri_adjustedHolidays': json.dumps(hijri.get('adjustedHolidays', [])),
    }
    
    date_dict = {        
        'g_day': gregorian.get('day', ''),
        'g_month': safe_get(gregorian, 'month.number', ''),
        'g_year': gregorian.get('year', ''),
        'h_day': hijri.get('day', ''),
        'h_month': safe_get(hijri, 'month.number', ''),
        'h_year': hijri.get('year', ''),
        'hijri_method': hijri.get('method', '')
    }
    
    # ===================== RETURN STRUCTURED DATA =====================
    # Combine all three calendar systems into single dictionary
    return date_dict, holidays_dict