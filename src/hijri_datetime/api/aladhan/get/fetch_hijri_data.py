"""
Gregorian to Hijri Date Converter

A simple utility to convert Gregorian dates to Hijri (Islamic) dates using the Aladhan API.

Usage
-----
Basic usage examples:

    from hijri_converter import fetch_hijri_data
    
    # Convert a Gregorian date (format: DD-MM-YYYY)
    result = fetch_hijri_data("15-03-2024")
    if result:
        hijri_date = result['data']['hijri']['date']
        gregorian_date = result['data']['gregorian']['date']
        print(f"Gregorian: {gregorian_date} -> Hijri: {hijri_date}")
    
    # Get detailed date information
    data = fetch_hijri_data("01-01-2024")
    if data:
        hijri = data['data']['hijri']
        print(f"Hijri date: {hijri['date']}")
        print(f"Month: {hijri['month']['en']} ({hijri['month']['ar']})")
        print(f"Year: {hijri['year']}")
        print(f"Weekday: {hijri['weekday']['en']}")
    
    # Handle multiple dates
    gregorian_dates = ["01-01-2024", "15-06-2024", "25-12-2024"]
    for date in gregorian_dates:
        data = fetch_hijri_data(date)
        if data:
            greg_readable = data['data']['gregorian']['date']
            hijri_readable = data['data']['hijri']['date']
            print(f"Gregorian: {greg_readable} -> Hijri: {hijri_readable}")
    
    # Error handling is built-in
    invalid_result = fetch_hijri_data("invalid-date")
    # Will print error message and return None

Requirements
------------
- requests

API Reference
-------------
Uses the Aladhan API (https://aladhan.com/hijri-gregorian-calendar-api)
gToH endpoint with HJCoSA (Hijri Calendar of Saudi Arabia) calculation method.
"""

import requests


def fetch_hijri_data(date_str):
    """
    Convert a Gregorian date to Hijri using the Aladhan API.
    
    Parameters
    ----------
    date_str : str
        Gregorian date in DD-MM-YYYY format (e.g., "15-03-2024")
        
    Returns
    -------
    dict or None
        JSON response containing date conversion data if successful.
        Returns None if the request fails or encounters an error.
        
        Expected structure when successful:
        {
            'data': {
                'hijri': {
                    'date': 'DD-MM-YYYY',
                    'month': {'number': int, 'en': 'name', 'ar': 'arabic_name'},
                    'year': 'YYYY',
                    'weekday': {'en': 'day_name', 'ar': 'arabic_day_name'},
                    ...
                },
                'gregorian': {
                    'date': 'DD-MM-YYYY',
                    'month': {'number': int, 'en': 'name'},
                    'year': 'YYYY',
                    ...
                }
            }
        }
        
    Raises
    ------
    None
        All exceptions are caught and handled internally.
        Error messages are printed to console.
        
    Examples
    --------
    >>> data = fetch_hijri_data("01-01-2024")
    >>> if data:
    ...     print(data['data']['hijri']['date'])
    19-06-1445
    
    >>> # Get month information
    >>> result = fetch_hijri_data("25-12-2024")
    >>> if result:
    ...     hijri_month = result['data']['hijri']['month']['en']
    ...     print(f"Hijri month: {hijri_month}")
    Hijri month: Jumada Al Akhirah
    
    >>> # Invalid date handling
    >>> result = fetch_hijri_data("invalid")
    Error fetching data for invalid: ...
    >>> print(result)
    None
    """
    # Construct API URL using gToH endpoint with HJCoSA calculation method (Saudi Arabia standard)
    url = f"https://api.aladhan.com/v1/gToH/{date_str}?calendarMethod=HJCoSA"
    
    try:
        # Make HTTP request to Aladhan API
        response = requests.get(url)
        
        # Raise HTTPError for bad responses (4xx, 5xx)
        response.raise_for_status()
        
        # Return parsed JSON data containing date conversion
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # Handle all requests-related exceptions (network, HTTP errors, etc.)
        print(f"Error fetching data for {date_str}: {e}")
        return None