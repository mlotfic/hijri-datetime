"""
Aladhan API Date Converter

A simple tool to fetch Hijri-Gregorian date conversions from the Aladhan API 
and export them as CSV. Supports bidirectional conversion and bulk processing.

Usage
-----
Basic usage:
    python aladhan_csv_converter.py

Custom date range (Gregorian to Hijri):
    from datetime import datetime
    from aladhan_csv_converter import CalendarConverter
    
    converter = CalendarConverter()
    converter.process_gregorian_range(
        start_date=datetime(2020, 1, 1),
        end_date=datetime(2025, 1, 1),
        output_file="custom_dates.csv"
    )

Single date conversions:
    converter = CalendarConverter()
    
    # Gregorian to Hijri
    hijri_data = converter.fetch_hijri_data("01-01-2025")
    print(hijri_data['data']['hijri']['date'])
    
    # Hijri to Gregorian
    gregorian_data = converter.fetch_gregorian_data("01-07-1446")
    print(gregorian_data['data']['gregorian']['date'])
"""

import requests
import csv
import time
from datetime import datetime, timedelta
import json


class CalendarConverter:
    """
    Bidirectional date converter between Hijri and Gregorian calendars using Aladhan API.
    
    This class provides methods to convert dates in both directions and process
    date ranges into structured CSV format containing both calendar systems.
    
    Parameters
    ----------
    calendar_method : str, default="HJCoSA"
        The Islamic calendar calculation method to use
    base_url : str, default="https://api.aladhan.com/v1"
        Base URL for the Aladhan API
    request_delay : float, default=0.1
        Delay between API requests in seconds to avoid rate limiting
        
    Examples
    --------
    >>> converter = CalendarConverter()
    >>> hijri_data = converter.fetch_hijri_data("01-01-2025")
    >>> gregorian_data = converter.fetch_gregorian_data("01-07-1446")
    """
    
    def __init__(self, calendar_method="HJCoSA", base_url="https://api.aladhan.com/v1", request_delay=0.1):
        self.calendar_method = calendar_method
        self.base_url = base_url
        self.request_delay = request_delay
        
        # CSV columns as required by the specification
        self.csv_columns = [
            "hijri.date", "hijri.format", "hijri.day", "hijri.month.number", "hijri.year",
            "hijri.weekday.ar", "hijri.weekday.en", "hijri.month.ar", "hijri.month.en",
            "hijri.month.days", "hijri.designation.abbreviated", "hijri.designation.expanded",
            "hijri.holidays", "hijri.adjustedHolidays", "hijri.method",
            "gregorian.date", "gregorian.format", "gregorian.day", "gregorian.month.number",
            "gregorian.year", "gregorian.weekday.en", "gregorian.month.en",
            "gregorian.designation.abbreviated", "gregorian.designation.expanded",
            "gregorian.lunarSighting"
        ]

    def fetch_hijri_data(self, gregorian_date_str):
        """
        Convert Gregorian date to Hijri using Aladhan API.
        
        Parameters
        ----------
        gregorian_date_str : str
            Gregorian date in DD-MM-YYYY format (e.g., "01-01-2025")
            
        Returns
        -------
        dict or None
            JSON response from the API, or None if request failed
            
        Examples
        --------
        >>> converter = CalendarConverter()
        >>> data = converter.fetch_hijri_data("01-01-2025")
        >>> print(data['data']['hijri']['date'])
        '01-07-1446'
        """
        url = f"{self.base_url}/gToH/{gregorian_date_str}?calendarMethod={self.calendar_method}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Hijri data for {gregorian_date_str}: {e}")
            return None

    def fetch_gregorian_data(self, hijri_date_str):
        """
        Convert Hijri date to Gregorian using Aladhan API.
        
        Parameters
        ----------
        hijri_date_str : str
            Hijri date in DD-MM-YYYY format (e.g., "01-07-1446")
            
        Returns
        -------
        dict or None
            JSON response from the API, or None if request failed
            
        Examples
        --------
        >>> converter = CalendarConverter()
        >>> data = converter.fetch_gregorian_data("01-07-1446")
        >>> print(data['data']['gregorian']['date'])
        '01-01-2025'
        """
        url = f"{self.base_url}/hToG/{hijri_date_str}?calendarMethod={self.calendar_method}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Gregorian data for {hijri_date_str}: {e}")
            return None

    def process_date_data(self, api_data):
        """
        Extract and structure date fields from API response.
        
        Parameters
        ----------
        api_data : dict
            Raw JSON response from the Aladhan API
            
        Returns
        -------
        dict or None
            Structured data matching CSV column requirements, or None if invalid data
            
        Examples
        --------
        >>> converter = CalendarConverter()
        >>> api_data = converter.fetch_hijri_data("01-01-2025")
        >>> row_data = converter.process_date_data(api_data)
        >>> print(row_data['hijri.date'])
        '01-07-1446'
        """
        # Validate API response
        if not api_data or api_data.get('code') != 200:
            return None
        
        data = api_data.get('data', {})
        hijri = data.get('hijri', {})
        gregorian = data.get('gregorian', {})
        
        return {
            # Hijri calendar fields
            'hijri.date': hijri.get('date', ''),
            'hijri.format': hijri.get('format', ''),
            'hijri.day': hijri.get('day', ''),
            'hijri.month.number': hijri.get('month', {}).get('number', ''),
            'hijri.year': hijri.get('year', ''),
            'hijri.weekday.ar': hijri.get('weekday', {}).get('ar', ''),
            'hijri.weekday.en': hijri.get('weekday', {}).get('en', ''),
            'hijri.month.ar': hijri.get('month', {}).get('ar', ''),
            'hijri.month.en': hijri.get('month', {}).get('en', ''),
            'hijri.month.days': hijri.get('month', {}).get('days', ''),
            'hijri.designation.abbreviated': hijri.get('designation', {}).get('abbreviated', ''),
            'hijri.designation.expanded': hijri.get('designation', {}).get('expanded', ''),
            'hijri.holidays': json.dumps(hijri.get('holidays', [])),  # Convert list to JSON string
            'hijri.adjustedHolidays': json.dumps(hijri.get('adjustedHolidays', [])),
            'hijri.method': hijri.get('method', ''),
            
            # Gregorian calendar fields
            'gregorian.date': gregorian.get('date', ''),
            'gregorian.format': gregorian.get('format', ''),
            'gregorian.day': gregorian.get('day', ''),
            'gregorian.month.number': gregorian.get('month', {}).get('number', ''),
            'gregorian.year': gregorian.get('year', ''),
            'gregorian.weekday.en': gregorian.get('weekday', {}).get('en', ''),
            'gregorian.month.en': gregorian.get('month', {}).get('en', ''),
            'gregorian.designation.abbreviated': gregorian.get('designation', {}).get('abbreviated', ''),
            'gregorian.designation.expanded': gregorian.get('designation', {}).get('expanded', ''),
            'gregorian.lunarSighting': gregorian.get('lunarSighting', '')
        }

    def generate_gregorian_date_range(self, start_date, end_date):
        """
        Generate Gregorian date strings for each day in the specified range.
        
        Parameters
        ----------
        start_date : datetime
            Starting date (inclusive)
        end_date : datetime  
            Ending date (inclusive)
            
        Yields
        ------
        str
            Date string in DD-MM-YYYY format
            
        Examples
        --------
        >>> converter = CalendarConverter()
        >>> dates = list(converter.generate_gregorian_date_range(datetime(2025, 1, 1), datetime(2025, 1, 3)))
        >>> print(dates)
        ['01-01-2025', '02-01-2025', '03-01-2025']
        """
        current = start_date
        while current <= end_date:
            yield current.strftime("%d-%m-%Y")  # API expects DD-MM-YYYY format
            current += timedelta(days=1)

    def process_gregorian_range(self, start_date, end_date, output_file="hijri_gregorian_dates.csv"):
        """
        Process a range of Gregorian dates and save results to CSV with DataFrame caching.
        
        This method loads existing data into DataFrame, identifies missing dates,
        fetches only new data from API, and saves the complete dataset.
        
        Parameters
        ----------
        start_date : datetime
            Starting Gregorian date for conversion
        end_date : datetime
            Ending Gregorian date for conversion  
        output_file : str, default="hijri_gregorian_dates.csv"
            Output CSV filename
            
        Returns
        -------
        int
            Number of successfully processed dates (new dates only)
            
        Examples
        --------
        >>> from datetime import datetime
        >>> converter = CalendarConverter()
        >>> count = converter.process_gregorian_range(
        ...     datetime(2024, 1, 1), 
        ...     datetime(2024, 1, 7),
        ...     "week_sample.csv"
        ... )
        Loading cache from week_sample.csv...
        Loaded 3 cached dates
        Cache date range: 01-01-2024 to 03-01-2024
        Processing 4 new dates from 04-01-2024 to 07-01-2024
        Completed! Processed 4 new dates. Total dataset: 7 dates saved to 'week_sample.csv'
        """
        # Load existing data into DataFrame cache
        if self.use_cache:
            print(f"Loading cache from {output_file}...")
            cached_count = self.load_cache(output_file)
            print(f"Loaded {cached_count} cached dates")
            
            # Show current cache range if available
            cache_range = self.get_cached_date_range()
            if cache_range:
                print(f"Cache date range: {cache_range[0]} to {cache_range[1]}")
        
        # Determine dates that need to be fetched
        total_days = (end_date - start_date).days + 1
        dates_to_fetch = []
        
        for date_str in self.generate_gregorian_date_range(start_date, end_date):
            if not self.use_cache or not self.is_date_cached(date_str):
                dates_to_fetch.append(date_str)
        
        if not dates_to_fetch:
            print(f"All {total_days} dates are already cached. No API calls needed!")
            # Still save to ensure file is up to date
            self.save_cache(output_file)
            return 0
        
        print(f"Processing {len(dates_to_fetch)} new dates from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}")
        print(f"Skipping {total_days - len(dates_to_fetch)} cached dates")
        
        processed = 0
        
        # Process only the dates that need to be fetched
        for date_str in dates_to_fetch:
            # Fetch data from API (Gregorian to Hijri conversion)
            api_data = self.fetch_hijri_data(date_str)
            
            if api_data:
                # Process and add to DataFrame cache
                row_data = self.process_date_data(api_data)
                if row_data:
                    self.add_to_cache(row_data)
                    processed += 1
                    
                    # Progress update every 100 records to avoid spam
                    if processed % 100 == 0:
                        print(f"Processed {processed}/{len(dates_to_fetch)} new dates...")
            
            # Simple rate limiting to avoid API bottlenecks
            time.sleep(self.request_delay)
        
        # Save the complete DataFrame to CSV
        total_saved = self.save_cache(output_file)
        print(f"Completed! Processed {processed} new dates. Total dataset: {total_saved} dates saved to '{output_file}'")
        
        return processed


def main():
    """
    Main function to run the full Gregorian date range conversion.
    
    Converts dates from the beginning of the Islamic calendar (July 19, 622 CE)
    to the current date and saves to CSV.
    """
    # Initialize converter with default settings
    converter = CalendarConverter()
    
    # Define the full date range
    start_date = datetime(622, 7, 19)  # Beginning of Islamic calendar
    end_date = datetime.now()          # Current date
    
    # Process the entire range
    converter.process_gregorian_range(start_date, end_date)


if __name__ == "__main__":
    main()
    
'''
columns = [
    # Hijri
    "hijri.date",
    "hijri.format",
    "hijri.day",
    "hijri.month.number",
    "hijri.year",

    "hijri.weekday.ar",
    "hijri.weekday.en",
    "hijri.month.ar",
    "hijri.month.en",    
    "hijri.month.days",

    "hijri.designation.abbreviated",
    "hijri.designation.expanded",

    "hijri.holidays",
    "hijri.adjustedHolidays",
    "hijri.method",

    # Gregorian
    "gregorian.date",
    "gregorian.format",
    "gregorian.day",
    "gregorian.month.number",
    "gregorian.year",
    "gregorian.weekday.en",
    "gregorian.month.en",
    "gregorian.designation.abbreviated",
    "gregorian.designation.expanded",
    "gregorian.lunarSighting"
]

'''