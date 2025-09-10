import os
import pandas as pd
from typing import Optional, Dict, List, Union
from dataclasses import dataclass

from utils._load_mapping_data import _load_mapping_data
from utils._load_hijri_holydays import _load_hijri_holydays

class DateLoader:
    """
    Calendar data loader with caching and validation capabilities.

    This class provides a convenient interface for loading and caching calendar
    mapping data, supporting multiple calendar systems with validation and
    error handling.

    Parameters
    ----------
    csv_path : str, optional
        Path to the CSV file containing calendar mapping data.
        Defaults to DEFAULT_CSV_PATH.

    Attributes
    ----------
    csv_path : str
        Path to the calendar data CSV file.

    Examples
    --------
    >>> loader = DateLoader()
    >>> data = loader.load_data()
    >>> print(f"Loaded {len(data)} calendar records")

    >>> # Use custom CSV file
    >>> loader = DateLoader("/path/to/custom/data.csv")
    >>> data = loader.load_data()
    """

    def __init__(self):
        """
        Initialize the calendar data loader.

        Parameters
        ----------
        csv_path : str, optional
            Path to the CSV file containing calendar mapping data.
        """
        self._data = None  # Cache for loaded data

    def load_data(self):
        """
        Load and return the calendar mapping data with caching.

        Returns
        -------
        pandas.DataFrame
            Validated and cleaned calendar mapping data. Subsequent calls
            return cached data without reloading from disk.

        Raises
        ------
        FileNotFoundError
            If the calendar data file is not found.
        ValueError
            If the data contains invalid values or missing columns.
        RuntimeError
            If loading fails for any other reason.

        Examples
        --------
        >>> loader = DateLoader()
        >>> data = loader.load_data()  # Loads from disk
        >>> data2 = loader.load_data()  # Returns cached data
        >>> assert data is data2  # Same object reference
        """
        if self._data is None:
            self._data = _load_mapping_data()
        return self._data

    def reload_data(self):
        """
        Force reload of calendar data from disk, bypassing cache.

        Returns
        -------
        pandas.DataFrame
            Freshly loaded calendar mapping data.

        Examples
        --------
        >>> loader = DateLoader()
        >>> data1 = loader.load_data()
        >>> # ... CSV file is updated externally ...
        >>> data2 = loader.reload_data()  # Loads fresh data
        """
        self._data = None  # Clear cache
        return self.load_data()
    
    def date_ranges(self) -> Dict[str, Dict[str, int]]:
        """
        Get the valid date ranges for each supported calendar system.

        Returns
        -------
        dict
            Dictionary with calendar names as keys and dictionaries with
            'min_year' and 'max_year' as values.

        Examples
        --------
        >>> loader = DateLoader()
        >>> ranges = loader.date_ranges()
        >>> print(ranges)
        {
            'gregorian': {'min': 622, 'max': 9999},
            'hijri': {'min': 1, 'max': 1500}
        }
        """
        data = self.load_data()
        # Get date range from multi-index levels
        years = data.index.get_level_values('g_year')
        date_ranges = {
            'gregorian': {
                'min': years.min(), 
                'max': years.max()
            },
            'hijri': {
                'min': data['h_year'].min(), 
                'max': data['h_year'].max()
            }
        }
        return date_ranges
    
    def __str__(self):
        return f"Date Database : Range ({self.date_ranges()})"



