"""
Hijri to Gregorian Date Converter

A simple utility to convert Hijri (Islamic) dates to Gregorian dates using the Aladhan API.

Usage
-----
Basic usage examples:

    from hijri_converter import fetch_gregorian_data
    
    # Convert a Hijri date (format: DD-MM-YYYY)
    result = fetch_gregorian_data("15-09-1445")
    if result:
        gregorian_date = result['data']['gregorian']['date']
        print(f"Gregorian date: {gregorian_date}")
    
    # Handle multiple dates
    hijri_dates = ["01-01-1445", "15-06-1445", "29-12-1445"]
    for date in hijri_dates:
        data = fetch_gregorian_data(date)
        if data:
            greg_date = data['data']['gregorian']['date']
            hijri_readable = data['data']['hijri']['date']
            print(f"Hijri: {hijri_readable} -> Gregorian: {greg_date}")
    
    # Error handling is built-in
    invalid_result = fetch_gregorian_data("invalid-date")
    # Will print error message and return None

Requirements
------------
- requests

API Reference
-------------
Uses the Aladhan API (https://aladhan.com/hijri-gregorian-calendar-api)
with HJCoSA (Hijri Calendar of Saudi Arabia) calculation method.
"""

import requests


def fetch_gregorian_data(date_str):
    """
    Convert a Hijri date to Gregorian using the Aladhan API.
    
    Parameters
    ----------
    date_str : str
        Hijri date in DD-MM-YYYY format (e.g., "15-09-1445")
        
    Returns
    -------
    dict or None
        JSON response containing date conversion data if successful.
        Returns None if the request fails or encounters an error.
        
        Expected structure when successful:
        {
            'data': {
                'hijri': {'date': 'DD-MM-YYYY', ...},
                'gregorian': {'date': 'DD-MM-YYYY', ...}
            }
        }
        
    Raises
    ------
    None
        All exceptions are caught and handled internally.
        Error messages are printed to console.
        
    Examples
    --------
    >>> data = fetch_gregorian_data("01-01-1445")
    >>> if data:
    ...     print(data['data']['gregorian']['date'])
    01-08-2023
    
    >>> # Invalid date handling
    >>> result = fetch_gregorian_data("invalid")
    Error fetching data for invalid: ...
    >>> print(result)
    None
    """
    # Construct API URL with HJCoSA calculation method (Saudi Arabia standard)
    url = f"https://api.aladhan.com/v1/hToG/{date_str}?calendarMethod=HJCoSA"
    
    try:
        # Make HTTP request to Aladhan API
        response = requests.get(url)
        
        # Raise HTTPError for bad responses (4xx, 5xx)
        response.raise_for_status()
        
        # Return parsed JSON data
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # Handle all requests-related exceptions (network, HTTP errors, etc.)
        print(f"Error fetching data for {date_str}: {e}")
        return None