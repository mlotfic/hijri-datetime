"""
Hijri Month Calendar to Gregorian Converter

A simple utility to fetch complete Hijri month calendar data and convert each day 
to its Gregorian equivalent using the Aladhan API.

Usage
-----
Basic usage examples:

    from hijri_converter import fetch_hijri_month_data
    
    # Get full month calendar data for Hijri month
    result = fetch_hijri_month_data(9, 1445)  # Ramadan 1445
    if result:
        calendar_data = result['data']
        for day_data in calendar_data:
            hijri_date = day_data['hijri']['date']
            gregorian_date = day_data['gregorian']['date']
            print(f"Hijri: {hijri_date} -> Gregorian: {gregorian_date}")
    
    # Get month information and statistics
    data = fetch_hijri_month_data(1, 1446)  # Muharram 1446
    if data:
        first_day = data['data'][0]
        month_name = first_day['hijri']['month']['en']
        total_days = len(data['data'])
        print(f"{month_name} {1446}: {total_days} days")
        print(f"Starts on: {first_day['gregorian']['date']}")
        print(f"Ends on: {data['data'][-1]['gregorian']['date']}")
    
    # Find specific dates within a month
    ramadan_data = fetch_hijri_month_data(9, 1445)
    if ramadan_data:
        for day_data in ramadan_data['data']:
            if day_data['hijri']['day'] == '27':  # Laylat al-Qadr (27th night)
                gregorian_equivalent = day_data['gregorian']['date']
                print(f"27th Ramadan 1445: {gregorian_equivalent}")
                break
    
    # Process multiple months
    months_to_fetch = [(1, 1445), (6, 1445), (9, 1445), (12, 1445)]
    for month, year in months_to_fetch:
        calendar = fetch_hijri_month_data(month, year)
        if calendar:
            month_info = calendar['data'][0]['hijri']['month']['en']
            days_count = len(calendar['data'])
            print(f"{month_info} {year}: {days_count} days")
    
    # Error handling is built-in
    invalid_result = fetch_hijri_month_data(13, 1445)  # Invalid month
    # Will print error message and return None

Requirements
------------
- requests

API Reference
-------------
Uses the Aladhan API (https://aladhan.com/hijri-gregorian-calendar-api)
hToGCalendar endpoint with HJCoSA (Hijri Calendar of Saudi Arabia) calculation method.
"""

import requests


def fetch_hijri_month_data(month, year):
    """
    Fetch complete Hijri month calendar data and convert to Gregorian using the Aladhan API.
    
    Parameters
    ----------
    month : int
        Hijri month number (1-12, where 1=Muharram, 9=Ramadan, 12=Dhul Hijjah)
    year : int
        Hijri year (e.g., 1445, 1446)
        
    Returns
    -------
    dict or None
        JSON response containing full month calendar data if successful.
        Returns None if the request fails or encounters an error.
        
        Expected structure when successful:
        {
            'data': [
                {
                    'hijri': {
                        'date': 'DD-MM-YYYY',
                        'day': 'DD',
                        'month': {'number': int, 'en': 'name', 'ar': 'arabic_name'},
                        'year': 'YYYY',
                        'weekday': {'en': 'day_name', 'ar': 'arabic_day_name'},
                        ...
                    },
                    'gregorian': {
                        'date': 'DD-MM-YYYY',
                        'day': 'DD',
                        'month': {'number': int, 'en': 'name'},
                        'year': 'YYYY',
                        ...
                    }
                },
                ... (one entry for each day of the month, typically 29-30 days)
            ]
        }
        
    Raises
    ------
    None
        All exceptions are caught and handled internally.
        Error messages are printed to console.
        
    Examples
    --------
    >>> data = fetch_hijri_month_data(9, 1445)  # Ramadan 1445
    >>> if data:
    ...     first_day = data['data'][0]['gregorian']['date']
    ...     month_name = data['data'][0]['hijri']['month']['en']
    ...     print(f"{month_name} starts on: {first_day}")
    Ramadan starts on: 11-03-2024
    
    >>> # Get month statistics
    >>> calendar = fetch_hijri_month_data(12, 1445)  # Dhul Hijjah
    >>> if calendar:
    ...     days_count = len(calendar['data'])
    ...     month_name = calendar['data'][0]['hijri']['month']['en']
    ...     print(f"{month_name}: {days_count} days")
    Dhul Hijjah: 29 days
    
    >>> # Invalid month handling
    >>> result = fetch_hijri_month_data(13, 1445)
    Error fetching data for 13/1445: ...
    >>> print(result)
    None
    """
    # Construct API URL using hToGCalendar endpoint with separate month/year parameters
    url = f"https://api.aladhan.com/v1/hToGCalendar/{month}/{year}?calendarMethod=HJCoSA"
    
    try:
        # Make HTTP request with explicit JSON accept header
        response = requests.get(url, headers={'accept': 'application/json'})
        
        # Raise HTTPError for bad responses (4xx, 5xx)
        response.raise_for_status()
        
        # Return parsed JSON data containing full month calendar
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # Handle all requests-related exceptions (network, HTTP errors, etc.)
        print(f"Error fetching data for {month}/{year}: {e}")
        return None