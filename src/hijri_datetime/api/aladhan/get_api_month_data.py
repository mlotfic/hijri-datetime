"""
API Data Processor for Single and Multiple Day Responses

A utility module for processing API responses containing single-day or multiple-day 
date and holiday information. Handles both individual date entries and arrays of 
date data from calendar APIs.

Usage
-----
Basic usage examples:

    from api_processor import get_api_month_data
    import requests
    
    # Process single day API response
    single_day_response = {
        'code': 200,
        'data': {
            'gregorian': {'date': '15-03-2024'},
            'hijri': {'date': '05-09-1445'},
            'holidays': ['Ramadan begins']
        }
    }
    
    result = get_api_month_data(single_day_response)
    if result:
        date_list, holidays_list = result
        print(f"Processed {len(date_list)} day(s)")
    
    # Process month calendar API response (array of days)
    month_response = {
        'code': 200,
        'data': [
            {
                'gregorian': {'date': '01-03-2024'},
                'hijri': {'date': '20-08-1445'},
                'holidays': []
            },
            {
                'gregorian': {'date': '02-03-2024'},
                'hijri': {'date': '21-08-1445'},
                'holidays': ['Islamic New Year']
            },
            # ... more days
        ]
    }
    
    result = get_api_month_data(month_response)
    if result:
        dates_data, holidays_data = result
        for i, (date_info, holiday_info) in enumerate(zip(dates_data, holidays_data)):
            print(f"Day {i+1}: {date_info}, Holidays: {holiday_info}")
    
    # Handle failed responses
    failed_response = {'code': 400, 'error': 'Invalid parameters'}
    result = get_api_month_data(failed_response)
    # Returns None for failed responses
    
    # Use with real API calls
    api_url = "https://api.aladhan.com/v1/hToGCalendar/9/1445"
    response = requests.get(api_url).json()
    processed_data = get_api_month_data(response)
    
    if processed_data:
        date_entries, holiday_entries = processed_data
        print(f"Successfully processed {len(date_entries)} days from Ramadan 1445")

Requirements
------------
- Custom module: utils.process_one_day_date_data

Dependencies
------------
This module depends on:
- process_one_day_date_data function from utils.process_one_day_date_data
"""

from .utils.process_one_day_date_data import process_one_day_date_data


# ===================== MAIN PROCESSING FUNCTIONS =====================

def get_api_month_data(api_response):
    """
    Process API response containing single or multiple day date data.
    
    This function handles both single-day responses and calendar responses 
    containing arrays of daily data. It validates the response, processes 
    each day's data, and returns structured lists of date and holiday information.
    
    Parameters
    ----------
    api_response : dict or None
        API response dictionary from date/calendar APIs.
        Expected structures:
        
        Single day response:
        {
            'code': 200,
            'data': {
                'gregorian': {...},
                'hijri': {...},
                'holidays': [...]
            }
        }
        
        Multiple days response (calendar):
        {
            'code': 200,
            'data': [
                {'gregorian': {...}, 'hijri': {...}, 'holidays': [...]},
                {'gregorian': {...}, 'hijri': {...}, 'holidays': [...]},
                ...
            ]
        }
        
    Returns
    -------
    tuple of (list, list) or None
        Returns tuple of (date_dict_list, holidays_dict_list) if successful.
        Returns None if API response is invalid or processing fails.
        
        - date_dict_list: List of processed date dictionaries
        - holidays_dict_list: List of processed holiday dictionaries
        
        Both lists have the same length, with corresponding indices 
        representing the same day's data.
        
    Raises
    ------
    None
        All exceptions are handled internally by the utility function.
        Invalid responses return None rather than raising exceptions.
        
    Examples
    --------
    >>> # Single day processing
    >>> single_resp = {
    ...     'code': 200,
    ...     'data': {
    ...         'gregorian': {'date': '15-03-2024'},
    ...         'hijri': {'date': '05-09-1445'},
    ...         'holidays': ['Ramadan']
    ...     }
    ... }
    >>> result = get_api_month_data(single_resp)
    >>> if result:
    ...     dates, holidays = result
    ...     print(f"Processed {len(dates)} day")
    Processed 1 day
    
    >>> # Multiple days processing (calendar month)
    >>> calendar_resp = {
    ...     'code': 200,
    ...     'data': [
    ...         {'gregorian': {'date': '01-03-2024'}, 'holidays': []},
    ...         {'gregorian': {'date': '02-03-2024'}, 'holidays': ['Holiday']}
    ...     ]
    ... }
    >>> result = get_api_month_data(calendar_resp)
    >>> if result:
    ...     dates, holidays = result
    ...     print(f"Processed {len(dates)} days")
    Processed 2 days
    
    >>> # Failed response handling
    >>> failed_resp = {'code': 404}
    >>> result = get_api_month_data(failed_resp)
    >>> print(result)
    None
    """
    # Initialize result lists for processed data
    date_dict_list = []
    holidays_dict_list = []
    
    # Validate API response exists and has successful status code
    if not api_response or api_response.get('code') != 200:
        return None
    
    # Extract data payload from API response
    data = api_response.get('data', {})
    
    # Handle both single day and multiple days (calendar array) responses
    if isinstance(data, list):
        # Process array of daily entries (calendar month response)
        for date_entry in data:
            processed_data = process_one_day_date_data(date_entry)
            if processed_data:  # Only add valid processed data
                date_dict, holidays_dict = processed_data
                date_dict_list.append(date_dict)
                holidays_dict_list.append(holidays_dict)
    else:
        # Process single day entry
        processed_data = process_one_day_date_data(data)
        if processed_data:  # Only add valid processed data
            date_dict, holidays_dict = processed_data
            date_dict_list.append(date_dict)
            holidays_dict_list.append(holidays_dict)
    
    # Return lists of processed data (empty lists if no valid data found)
    return date_dict_list, holidays_dict_list