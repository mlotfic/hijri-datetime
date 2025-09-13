"""Core Hijri date and time classes."""

from datetime import date, datetime, time
from typing import Optional, Union, Tuple
import calendar
import pandas as pd

from .exceptions import InvalidHijriDate
from .constants import HIJRI_MONTHS, HIJRI_WEEKDAYS

from hijri_datetime.data import DatabaseLoader

loader = DatabaseLoader()

'''
def __init__(self, loader: DatabaseLoader): 
        self.year = None
        self.month = None
        self.day = None
        

'''

class HijriDate:
    """Represents a Hijri calendar date."""
 
    def init(self, year: int, month: int, day: int):
        """Initialize a Hijri date.
 
        Args:
            year: Hijri year
            month: Hijri month (1-12)
            day: Hijri day (1-30)
 
        Raises:
            InvalidHijriDate: If the date is invalid
        """        
        try:
            # Load the calendar mapping data
            self.db = loader._data            
            self._data_loaded = True
            self._date_ranges = loader.date_ranges()  # Initialize cache for date ranges
            if not self._is_valid_date(year, month, day):
                raise InvalidHijriDate(f"Invalid Hijri date: {year}-{month}-{day}")    
        except Exception as e:
            self._data_loaded = False
            self.db = None
            self._date_ranges = None
            # Don't re-raise to allow graceful degradation   
        
        self.db = loader._data
        self.selected_db = 
        self._h_year = year
        self._h_month = month
        self._h_day = day
        self.method = None # Allowed: "HJCoSA" ┃ "UAQ" ┃ "DIYANET" ┃ "MATHEMATICAL"
        self.dtype = None  # Allowed: "datetime" ┃ "date" ┃ "month_range" ┃ "year_range"

    def _h_get_valid_dates(self, year: int, month: Optional[int], day: Optional[int]) -> Optional[pd.DataFrame]:
        """Check if the given Hijri date is valid."""
        if not isinstance(year, int):
            return None
        if month and not (1 <= month <= 12):
            return None
        if day and not (1 <= day <= 30):
            return None
        
        # Add more sophisticated validation here - checking database
        self.dtype = self.get_dtype(year, month, day)
        # Get Hijri equivalent
        if self._data_loaded:
            # Get all records
            if self.dtype == "date":
                try:
                    hijri_info = self.db.loc[(year, month, day)][['h_day', 'h_month', 'h_year', 'hijri_method']]
                    return hijri_info
                except KeyError:
                    print(f"   ℹ  Hijri date: {year}-{month}-{day} not available in dataset")
            elif self.dtype == "month_range":
                try:
                    hijri_info = self.db.loc[(year, month, day)][['h_day', 'h_month', 'h_year', 'hijri_method']]
                    return hijri_info
                except KeyError:
                    print(f"   ℹ  Hijri date: {year}-{month} not available in dataset")
                    
            elif self.dtype == "year_range":
                try:
                    hijri_info = self.db.loc[(year, month, day)][['h_day', 'h_month', 'h_year', 'hijri_method']]
                    return hijri_info
                except KeyError:
                    print(f"   ℹ  Hijri date: {year} not available in dataset")
                
        return None
    
    def _g_get_valid_dates(self, year: int, month: Optional[int], day: Optional[int]) -> Optional[pd.DataFrame]:
        """Check if the given Gregorian date is valid."""
        if not isinstance(year, int):
            return None
        if month and not (1 <= month <= 12):
            return None
        if day and not (1 <= day <= 31):
            return None
        
        # Add more sophisticated validation here - checking database
        self.dtype = self.get_dtype(year, month, day)
        # Get Hijri equivalent
        if self._data_loaded:
            # Get all records
            if self.dtype == "date":
                try:
                    hijri_info = self.db.loc[(year, month, day)][['h_day', 'h_month', 'h_year', 'hijri_method']]
                    return hijri_info
                except KeyError:
                    print(f"   ℹ  Hijri date: {year}-{month}-{day} not available in dataset")
            elif self.dtype == "month_range":
                try:
                    hijri_info = self.db.loc[(year, month, day)][['h_day', 'h_month', 'h_year', 'hijri_method']]
                    return hijri_info
                except KeyError:
                    print(f"   ℹ  Hijri date: {year}-{month} not available in dataset")
                    
            elif self.dtype == "year_range":
                try:
                    hijri_info = self.db.loc[(year, month, day)][['h_day', 'h_month', 'h_year', 'hijri_method']]
                    return hijri_info
                except KeyError:
                    print(f"   ℹ  Hijri date: {year} not available in dataset")
                
        return None
    
    def get_dtype(self, year: int, month: Optional[int], day: Optional[int]):
        Allowed= ["datetime", "date", "month_range", "year_range"]
        if year and month and day:
            return Allowed[1]
        if year and month and not day:
            return Allowed[2]
        if year and not month and not day:
            return Allowed[3]
        
        return None
 
    def __repr__(self) -> str:
        return f"datetime.date({self.year}, {self.month}, {self.day}, 'hijri')"
 
    def __str__(self) -> str:
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}-AH"
 
    @property
    def month_name(self) -> str:
        """Get the name of the Hijri month."""
        return HIJRI_MONTHS[self.month - 1]
 
    def to_gregorian(self) -> date:
        """Convert to Gregorian date."""
        from .converter import hijri_to_gregorian
        return hijri_to_gregorian(self)
 
    def to_jalali(self):
        """Convert to Jalali date."""
        from .converter import hijri_to_jalali
        return hijri_to_jalali(self)


class HijriDateTime:
    """Represents a Hijri calendar datetime."""
 
    def __init__(self, year: int, month: int, day: int, 
                 hour: int = 0, minute: int = 0, second: int = 0):
        """Initialize a Hijri datetime."""
        self.date = HijriDate(year, month, day)
        self.time = HijriTime(hour, minute, second)
 
    @property
    def year(self) -> int:
        return self.date.year
 
    @property
    def month(self) -> int:
        return self.date.month
 
    @property
    def day(self) -> int:
        return self.date.day
 
    def __repr__(self) -> str:
        return f"HijriDateTime({self.year}, {self.month}, {self.day}, {self.time.hour}, {self.time.minute}, {self.time.second})"


class HijriTime:
    """Represents a time in the Hijri calendar context."""
 
    def __init__(self, hour: int = 0, minute: int = 0, second: int = 0):
        """Initialize a Hijri time."""
        if not (0 <= hour <= 23):
            raise ValueError("Hour must be between 0 and 23")
        if not (0 <= minute <= 59):
            raise ValueError("Minute must be between 0 and 59")
        if not (0 <= second <= 59):
            raise ValueError("Second must be between 0 and 59")
 
        self.hour = hour
        self.minute = minute
        self.second = second


class HijriDateRange:
    """Represents a range of Hijri dates."""
 
    def __init__(self, start: HijriDate, end: HijriDate):
        """Initialize a Hijri date range."""
        if start > end:
            raise ValueError("Start date must be before or equal to end date")
        self.start = start
        self.end = end
 
    def __contains__(self, date: HijriDate) -> bool:
        """Check if a date is within the range."""
        return self.start <= date <= self.end
 
    def __iter__(self):
        """Iterate over dates in the range."""
        current = self.start
        while current <= self.end:
            yield current
            # Add one day (simplified)
            current = self._add_one_day(current)
 
    def _add_one_day(self, date: HijriDate) -> HijriDate:
        """Add one day to a Hijri date (simplified implementation)."""
        # This is a simplified version - you'd need proper calendar logic
        if date.day < 30:  # Assuming max 30 days per month for simplicity
            return HijriDate(date.year, date.month, date.day + 1)
        elif date.month < 12:
            return HijriDate(date.year, date.month + 1, 1)
        else:
            return HijriDate(date.year + 1, 1, 1)