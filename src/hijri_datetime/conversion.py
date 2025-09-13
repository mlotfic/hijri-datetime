"""
DateMapping - Gregorian ↔ Hijri Date Conversion

Usage
-----
Quick start example:

    from hijri_datetime.data import DatabaseLoader
    from your_module import DateMapping

    # Load your data
    loader = DatabaseLoader()
    mapper = DateMapping(loader)

    # Convert specific date
    hijri_date = mapper.to_hijri(2024, 1, 15)
    print(hijri_date)

    # Convert back to Gregorian
    greg_date = mapper.to_greg(1445, 7, 4)
    print(greg_date)

    # Get month range
    month_range = mapper.to_hijri(2024, 1, None)
    print(month_range)
"""

import pandas as pd
from typing import Optional
from hijri_datetime.data import DatabaseLoader


class DateMapping:
    """
    Bidirectional Gregorian ↔ Hijri date conversion using preloaded mapping data.

    Optimized for speed with large datasets using pandas MultiIndex lookups.

    Parameters
    ----------
    loader : DatabaseLoader
        Data loader containing the date mapping DataFrame.

    Examples
    --------
    >>> from hijri_datetime.data import DatabaseLoader
    >>> loader = DatabaseLoader()
    >>> mapper = DateMapping(loader)
    >>> hijri = mapper.to_hijri(2024, 1, 15)
    >>> gregorian = mapper.to_greg(1445, 7, 4)
    """

    def __init__(self, loader: DatabaseLoader):
        """
        Initialize DateMapping with data from DatabaseLoader.

        Parameters
        ----------
        loader : DatabaseLoader
            Data loader containing date mapping with required columns:
            ['day', 'month', 'year', 'h_day', 'h_month', 'h_year', 'hijri_method']
        """
        # Load data or create empty DataFrame with required columns
        self.df = (
            loader._data if isinstance(loader._data, pd.DataFrame)
            else pd.DataFrame(columns=[
                'day', 'month', 'year', 'h_day', 'h_month', 'h_year', 'hijri_method'
                ]
            ))

    def get_dtype(self, year: int, month: Optional[int], day: Optional[int]):
        """
        Determine date lookup type based on provided date components.

        Parameters
        ----------
        year : int
            Year value (required)
        month : int, optional
            Month value (1-12)
        day : int, optional
            Day value (1-31)

        Returns
        -------
        str or None
            Date type: "date" (exact), "month_range", "year_range", or None

        Examples
        --------
        >>> mapper.get_dtype(2024, 1, 15)
        'date'
        >>> mapper.get_dtype(2024, 1, None)
        'month_range'
        >>> mapper.get_dtype(2024, None, None)
        'year_range'
        """
        Allowed = ["datetime", "date", "month_range", "year_range"]

        # Exact date: year + month + day
        if year and month and day:
            return Allowed[1]
        # Month range: year + month (no day)
        if year and month and not day:
            return Allowed[2]
        # Year range: only year
        if year and not month and not day:
            return Allowed[3]
        return None

    def to_hijri(year: int, month: Optional[int], day: Optional[int]):
        """
        Convert Gregorian date to Hijri equivalent.

        Optimized for large datasets using MultiIndex for O(log n) lookups.

        Parameters
        ----------
        g_year : int
            Gregorian year
        g_month : int
            Gregorian month (1-12)
        g_day : int
            Gregorian day (1-31)

        Returns
        -------
        pd.DataFrame or pd.Series
            Hijri date with columns: ['h_day', 'h_month', 'h_year', 'hijri_method']
            Empty DataFrame if no matching dates found

        Examples
        --------
        >>> hijri = mapper.to_hijri(2024, 1, 15)
        >>> print(hijri[['h_year', 'h_month', 'h_day']])
        """
        # Set multi-index for efficient date-based lookups
        # This allows queries like df.loc[(2024, 1, 15)] for specific dates
        df = self.df.set_index(["year", "month", "day"])

        dtype = self.get_dtype(year, month, day)

        # Get Hijri equivalent based on date type
        if dtype == "date":
            result = df[(df['g_year']==year) and (df['g_month']==month) and (df['g_day']==day)]
        elif dtype == "month_range":
            result = df[(df['g_year']==year) and (df['g_month']==month)]
        elif dtype == "year_range":
            result = df[(df['g_year']==year)]
        result =  pd.DataFrame()
        
        if result.empty:
            print(f"   ℹ  Gregorian date for Hijri {year}-{month}-{day} not available in dataset")
        
        return result

    def to_greg(self, year: int, month: Optional[int], day: Optional[int]):
        """
        Convert Hijri date to Gregorian equivalent.

        Uses pandas boolean indexing for efficient filtering on large datasets.

        Parameters
        ----------
        h_year : int
            Hijri year
        h_month : int
            Hijri month (1-12)
        h_day : int
            Hijri day (1-30)

        Returns
        -------
        pd.DataFrame
            Gregorian date(s) with columns: ['year', 'month', 'day', 'hijri_method']
            Empty DataFrame if no matching dates found

        Examples
        --------
        >>> greg = mapper.to_greg(1445, 7, 4)
        >>> print(greg[['year', 'month', 'day']])
        """
        # Use vectorized boolean indexing for speed with large datasets
        mask = ((self.df['h_year'] == h_year) &
                (self.df['h_month'] == h_month) &
                (self.df['h_day'] == h_day))

        result = self.df[mask]

        if result.empty:
            print(f"   ℹ  Gregorian date for Hijri {h_year}-{h_month}-{h_day} not available in dataset")
            return pd.DataFrame()

        return result
