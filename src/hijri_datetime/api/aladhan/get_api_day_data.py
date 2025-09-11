"""
API Response Processor for Date Data

A utility module for processing API responses containing date and holiday information.
Extracts and transforms single-day date data from API responses into structured formats.

Usage
-----
Basic usage examples:

    from api_processor import get_api_day_data
    import requests
    
    # Process API response from date conversion API
    api_response = requests.get("https://api.example.com/date/convert").json()
    result = get_api_day_data(api_response)
    
    if result:
        date_dict, holidays_dict = result
        print(f"Date info: {date_dict}")
        print(f"Holidays: {holidays_dict}")
    else:
        print("Failed to process API response")
    
    # Handle successful API response
    successful_response = {
        'code': 200,
        'data': {
            'gregorian': {'date': '15-03-2024', 'month': {'en': 'March'}},
            'hijri': {'date': '05-09-1445', 'month': {'en': 'Ramadan'}},
            'holidays': ['Ramadan']
        }
    }
    
    result = get_api_day_data(successful_response)
    if result:
        date_info, holiday_info = result
        # Use processed data in your application
    
    # Handle failed API response
    failed_response = {'code': 400, 'error': 'Invalid date'}
    result = get_api_day_data(failed_response)
    # Returns None for failed responses
    
    # Handle missing or malformed data
    empty_response = None
    result = get_api_day_data(empty_response)
    # Returns None safely

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


def get_api_day_data(api_response):
    """
    Extract and process date and holiday data from a single-day API response.
    
    This function validates the API response, extracts the data payload, and 
    processes it through the utility function to return structured date and 
    holiday information.
    
    Parameters
    ----------
    api_response : dict or None
        API response dictionary containing date conversion data.
        Expected structure:
        {
            'code': 200,  # Success code
            'data': {     # Date and holiday data to be processed
                'gregorian': {...},
                'hijri': {...},
                'holidays': [...]
            }
        }
        
    Returns
    -------
    tuple of (dict, dict) or None
        Returns tuple of (date_dict, holidays_dict) if processing successful.
        Returns None if API response is invalid or processing fails.
        
        - date_dict: Processed date information
        - holidays_dict: Processed holiday information
        
    Raises
    ------
    None
        All exceptions are handled internally by the utility function.
        Invalid responses return None rather than raising exceptions.
        
    Examples
    --------
    >>> # Successful processing
    >>> api_resp = {
    ...     'code': 200,
    ...     'data': {
    ...         'gregorian': {'date': '15-03-2024'},
    ...         'hijri': {'date': '05-09-1445'},
    ...         'holidays': ['Ramadan']
    ...     }
    ... }
    >>> result = get_api_day_data(api_resp)
    >>> if result:
    ...     date_info, holidays = result
    ...     print("Processing successful")
    Processing successful
    
    >>> # Failed API response
    >>> failed_resp = {'code': 400, 'error': 'Bad request'}
    >>> result = get_api_day_data(failed_resp)
    >>> print(result)
    None
    
    >>> # Handle None input
    >>> result = get_api_day_data(None)
    >>> print(result)
    None
    """
    # Validate API response exists and has successful status code
    if not api_response or api_response.get('code') != 200:
        return None
    
    # Extract data payload from API response
    data = api_response.get('data', {})
    
    # Process the raw data through utility function
    processed_data = process_one_day_date_data(data)
    
    # Return processed data if valid, None otherwise
    if processed_data:
        date_dict, holidays_dict = processed_data
        return date_dict, holidays_dict
    
    return None
