"""
Hijri Date System - A production-quality implementation mimicking datetime module behavior.

This module provides HijriDate and iTimedelta classes that behave similarly to
datetime.date and datetime.timedelta, along with a flexible idate() factory function.
"""

from typing import Union, Tuple, Optional
import functools


@functools.total_ordering
class HijriDate:
    """
    A Hijri date representation similar to datetime.date.
    
    Attributes:
        year (int): Hijri year
        month (int): Hijri month (1-12)
        day (int): Hijri day (1-30)
    """
    
    def __init__(self, year: int, month: int, day: int):
        """
        Initialize a HijriDate object.
        
        Args:
            year (int): Hijri year (positive integer)
            month (int): Hijri month (1-12)
            day (int): Hijri day (1-30)
            
        Raises:
            ValueError: If month or day values are out of valid range
        """
        if not (1 <= month <= 12):
            raise ValueError(f"Month must be between 1 and 12, got {month}")
        if not (1 <= day <= 30):
            raise ValueError(f"Day must be between 1 and 30, got {day}")
            
        self.year = year
        self.month = month
        self.day = day
    
    def __repr__(self) -> str:
        """Return string representation of HijriDate."""
        return f"HijriDate({self.year}, {self.month}, {self.day})"
    
    def __str__(self) -> str:
        """Return human-readable string representation."""
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
    
    def __eq__(self, other) -> bool:
        """Check equality with another HijriDate."""
        if not isinstance(other, HijriDate):
            return NotImplemented
        return (self.year, self.month, self.day) == (other.year, other.month, other.day)
    
    def __lt__(self, other) -> bool:
        """Check if this date is less than another HijriDate."""
        if not isinstance(other, HijriDate):
            return NotImplemented
        return (self.year, self.month, self.day) < (other.year, other.month, other.day)
    
    def __hash__(self) -> int:
        """Return hash value for use in sets and dictionaries."""
        return hash((self.year, self.month, self.day))
    
    def __add__(self, other) -> 'HijriDate':
        """
        Add a timedelta to this date.
        
        Args:
            other (iTimedelta): Timedelta to add
            
        Returns:
            HijriDate: New date after adding the timedelta
        """
        if not isinstance(other, iTimedelta):
            return NotImplemented
        return self._add_days(other.days)
    
    def __sub__(self, other) -> Union['HijriDate', 'iTimedelta']:
        """
        Subtract a timedelta or another date from this date.
        
        Args:
            other (iTimedelta or HijriDate): Object to subtract
            
        Returns:
            HijriDate: If subtracting timedelta, returns new date
            iTimedelta: If subtracting HijriDate, returns difference in days
        """
        if isinstance(other, iTimedelta):
            return self._add_days(-other.days)
        elif isinstance(other, HijriDate):
            days_diff = self._to_ordinal() - other._to_ordinal()
            return iTimedelta(days=days_diff)
        return NotImplemented
    
    def _to_ordinal(self) -> int:
        """
        Convert HijriDate to ordinal (days since Hijri epoch).
        
        This is a simplified calculation assuming:
        - 354 days per year
        - 30 days per month
        
        Returns:
            int: Days since Hijri year 1
        """
        # Simple calculation: (year-1)*354 + (month-1)*30 + (day-1)
        return (self.year - 1) * 354 + (self.month - 1) * 30 + (self.day - 1)
    
    @classmethod
    def _from_ordinal(cls, ordinal: int) -> 'HijriDate':
        """
        Create HijriDate from ordinal days since Hijri epoch.
        
        Args:
            ordinal (int): Days since Hijri year 1
            
        Returns:
            HijriDate: Corresponding Hijri date
        """
        # Reverse calculation
        year = ordinal // 354 + 1
        remaining = ordinal % 354
        month = remaining // 30 + 1
        day = remaining % 30 + 1
        
        # Handle edge cases for month/day overflow
        if month > 12:
            year += 1
            month = 1
        if day > 30:
            month += 1
            day = 1
            if month > 12:
                year += 1
                month = 1
        
        return cls(year, month, day)
    
    def _add_days(self, days: int) -> 'HijriDate':
        """
        Add days to this date.
        
        Args:
            days (int): Number of days to add (can be negative)
            
        Returns:
            HijriDate: New date after adding days
        """
        ordinal = self._to_ordinal() + days
        return self._from_ordinal(ordinal)
    
    def isoformat(self) -> str:
        """Return date in ISO-like format (YYYY-MM-DD)."""
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"


@functools.total_ordering
class iTimedelta:
    """
    A time duration representation similar to datetime.timedelta.
    
    Attributes:
        days (int): Number of days in the duration
    """
    
    def __init__(self, days: int = 0):
        """
        Initialize an iTimedelta object.
        
        Args:
            days (int): Number of days (can be negative)
        """
        self.days = days
    
    def __repr__(self) -> str:
        """Return string representation of iTimedelta."""
        return f"iTimedelta(days={self.days})"
    
    def __str__(self) -> str:
        """Return human-readable string representation."""
        if self.days == 1:
            return "1 day"
        elif self.days == -1:
            return "-1 day"
        else:
            return f"{self.days} days"
    
    def __eq__(self, other) -> bool:
        """Check equality with another iTimedelta."""
        if not isinstance(other, iTimedelta):
            return NotImplemented
        return self.days == other.days
    
    def __lt__(self, other) -> bool:
        """Check if this duration is less than another iTimedelta."""
        if not isinstance(other, iTimedelta):
            return NotImplemented
        return self.days < other.days
    
    def __hash__(self) -> int:
        """Return hash value for use in sets and dictionaries."""
        return hash(self.days)
    
    def __add__(self, other) -> Union['iTimedelta', 'HijriDate']:
        """
        Add another timedelta or add to a HijriDate.
        
        Args:
            other (iTimedelta or HijriDate): Object to add
            
        Returns:
            iTimedelta: If adding timedelta, returns combined duration
            HijriDate: If adding to HijriDate, returns new date
        """
        if isinstance(other, iTimedelta):
            return iTimedelta(days=self.days + other.days)
        elif isinstance(other, HijriDate):
            return other + self
        return NotImplemented
    
    def __sub__(self, other) -> 'iTimedelta':
        """
        Subtract another timedelta.
        
        Args:
            other (iTimedelta): Timedelta to subtract
            
        Returns:
            iTimedelta: Resulting duration
        """
        if not isinstance(other, iTimedelta):
            return NotImplemented
        return iTimedelta(days=self.days - other.days)
    
    def __mul__(self, other) -> 'iTimedelta':
        """
        Multiply duration by a scalar.
        
        Args:
            other (int or float): Scalar multiplier
            
        Returns:
            iTimedelta: Multiplied duration
        """
        if isinstance(other, (int, float)):
            return iTimedelta(days=int(self.days * other))
        return NotImplemented
    
    def __rmul__(self, other) -> 'iTimedelta':
        """Right multiplication (scalar * timedelta)."""
        return self.__mul__(other)
    
    def __truediv__(self, other) -> Union['iTimedelta', float]:
        """
        Divide duration by scalar or another timedelta.
        
        Args:
            other (int, float, or iTimedelta): Divisor
            
        Returns:
            iTimedelta: If dividing by scalar, returns new duration
            float: If dividing by timedelta, returns ratio
        """
        if isinstance(other, (int, float)):
            return iTimedelta(days=int(self.days / other))
        elif isinstance(other, iTimedelta):
            if other.days == 0:
                raise ZeroDivisionError("Cannot divide by zero timedelta")
            return self.days / other.days
        return NotImplemented
    
    def __neg__(self) -> 'iTimedelta':
        """Return negative duration."""
        return iTimedelta(days=-self.days)
    
    def __pos__(self) -> 'iTimedelta':
        """Return positive duration (copy)."""
        return iTimedelta(days=self.days)
    
    def __abs__(self) -> 'iTimedelta':
        """Return absolute duration."""
        return iTimedelta(days=abs(self.days))
    
    def __bool__(self) -> bool:
        """Return True if duration is non-zero."""
        return self.days != 0
    
    def total_days(self) -> int:
        """Return total number of days (for compatibility)."""
        return self.days


def idate(year: int, month: Optional[int] = None, day: Optional[int] = None) -> Union[HijriDate, Tuple[HijriDate, iTimedelta]]:
    """
    Factory function for creating HijriDate objects or date ranges.
    
    This function provides flexible signatures similar to how pandas handles date ranges:
    
    Args:
        year (int): Hijri year
        month (Optional[int]): Hijri month (1-12). If None, returns year range.
        day (Optional[int]): Hijri day (1-30). If None, returns month range.
    
    Returns:
        HijriDate: If all three parameters provided, returns a single date
        Tuple[HijriDate, iTimedelta]: If month or day omitted, returns (start_date, duration)
            - For year only: (HijriDate(year, 1, 1), iTimedelta(days=354))
            - For year+month: (HijriDate(year, month, 1), iTimedelta(days=30))
    
    Examples:
        >>> idate(1447, 2, 5)
        HijriDate(1447, 2, 5)
        
        >>> start, duration = idate(1447, 2)
        >>> print(start, duration)
        HijriDate(1447, 2, 1) iTimedelta(days=30)
        
        >>> start, duration = idate(1447)
        >>> print(start, duration)
        HijriDate(1447, 1, 1) iTimedelta(days=354)
    """
    if day is not None:
        # Full date specified: return HijriDate
        if month is None:
            raise ValueError("Month must be specified when day is provided")
        return HijriDate(year, month, day)
    
    elif month is not None:
        # Year and month specified: return month range
        start_date = HijriDate(year, month, 1)
        duration = iTimedelta(days=30)  # Assuming 30 days per month
        return start_date, duration
    
    else:
        # Only year specified: return year range
        start_date = HijriDate(year, 1, 1)
        duration = iTimedelta(days=354)  # Assuming 354 days per year
        return start_date, duration


# Example usage and demonstration
if __name__ == "__main__":
    print("=== Hijri Date System Demo ===\n")
    
    # Basic HijriDate creation
    print("1. Creating HijriDate objects:")
    date1 = HijriDate(1447, 2, 5)
    date2 = HijriDate(1447, 2, 15)
    print(f"   date1 = {date1}")
    print(f"   date2 = {date2}")
    print()
    
    # Using idate factory function
    print("2. Using idate() factory function:")
    
    # Single date
    d = idate(1447, 2, 5)
    print(f"   idate(1447, 2, 5) = {d}")
    
    # Month range
    m_start, m_delta = idate(1447, 2)
    print(f"   idate(1447, 2) = {m_start}, {m_delta}")
    
    # Year range
    y_start, y_delta = idate(1447)
    print(f"   idate(1447) = {y_start}, {y_delta}")
    print()
    
    # Date arithmetic
    print("3. Date arithmetic:")
    delta = iTimedelta(days=10)
    future_date = date1 + delta
    print(f"   {date1} + {delta} = {future_date}")
    
    difference = date2 - date1
    print(f"   {date2} - {date1} = {difference}")
    
    end_of_month = m_start + m_delta
    print(f"   {m_start} + {m_delta} = {end_of_month}")
    print()
    
    # Comparisons
    print("4. Date comparisons:")
    print(f"   {date1} < {date2} = {date1 < date2}")
    print(f"   {date1} == {date1} = {date1 == date1}")
    print(f"   {future_date} > {date1} = {future_date > date1}")
    print()
    
    # Timedelta operations
    print("5. Timedelta operations:")
    td1 = iTimedelta(days=10)
    td2 = iTimedelta(days=5)
    print(f"   {td1} + {td2} = {td1 + td2}")
    print(f"   {td1} - {td2} = {td1 - td2}")
    print(f"   {td1} * 3 = {td1 * 3}")
    print(f"   {td1} / 2 = {td1 / 2}")
    print()
    
    # Formatting
    print("6. String formatting:")
    print(f"   str(date1) = {str(date1)}")
    print(f"   repr(date1) = {repr(date1)}")
    print(f"   date1.isoformat() = {date1.isoformat()}")
    print()
    
    print("=== Integration with HijriDateMapper (Conceptual) ===")
    print("# This would work with the provided HijriDateMapper class:")
    print("# mapper = HijriDateMapper()")
    print("# result, first_idx, span = mapper.to_hijri(2024, 1, 15)")
    print("# hijri_date = idate(result.iloc[0]['h_year'], result.iloc[0]['h_month'], result.iloc[0]['h_day'])")