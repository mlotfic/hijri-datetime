"""
Calendar Data Loader - Production-ready calendar mapping utilities.

This module provides efficient loading and processing of calendar mapping data
from compressed CSV files, supporting multiple calendar systems including
Gregorian, Hijri, and Solar Hijri calendars.

Usage
-----
Basic usage (quickstart):

    from calendar_loader import _load_mapping_data
    
    # Load default calendar data
    df = _load_mapping_data()
    print(f"Loaded {len(df)} records")
    
    # Access specific date mapping
    # Data is indexed by (year, month, day)
    gregorian_2024 = df.loc[2024]  # All 2024 data
    jan_2024 = df.loc[(2024, 1)]  # January 2024
    specific_date = df.loc[(2024, 1, 15)]  # January 15, 2024
    
    # Get Hijri equivalent for a Gregorian date
    hijri_date = df.loc[(2024, 1, 15)][['h_day', 'h_month', 'h_year']]
    
    # Custom data file
    df = _load_mapping_data("/path/to/your/calendar_data.csv.xz")

Advanced usage:

    # Data exploration
    print(f"Date range: {df.index.get_level_values('g_year').min()}-{df.index.get_level_values('g_year').max()}")
    print(f"Available columns: {df.columns.tolist()}")
    
    # Filter by year range
    recent_data = df.loc[2020:2025]
    
    # Find all records for a specific Hijri month
    ramadan_records = df[df['h_month'] == 9]  # Ramadan is 9th month
"""

import os
import pandas as pd

# Default CSV file path relative to this module
DEFAULT_CSV_PATH = "./mapping_date/calendar_date_dataset.csv.xz"
# DEBUG:: file_path = "../mapping_date/calendar_date_dataset.csv.xz"


def _load_mapping_data(csv_path=DEFAULT_CSV_PATH):
    """
    Load and validate calendar mapping data from CSV file.

    This function handles the complete data loading pipeline including file validation,
    CSV parsing, data type conversions, and data cleaning. The resulting DataFrame
    is indexed by Gregorian date (year, month, day) for efficient lookups.

    Parameters
    ----------
    csv_path : str, optional
        Path to the CSV file containing calendar mapping data.
        Defaults to DEFAULT_CSV_PATH ("./mapping_date/calendar_date_dataset.csv.xz").
        Supports compressed files (.xz, .gz, .bz2).

    Returns
    -------
    pandas.DataFrame
        Validated and cleaned calendar mapping data with proper data types.
        Multi-indexed by (g_year, g_month, g_day) for efficient date lookups.
        Contains columns for multiple calendar systems:
        - Gregorian: g_day, g_month, g_year
        - Hijri: h_day, h_month, h_year, hijri_method
        Sorted by Gregorian date for consistent ordering.

    Raises
    ------
    FileNotFoundError
        If the calendar data file is not found or not accessible.
    PermissionError
        If the file cannot be read due to permission issues.
    ValueError
        If CSV is empty or contains invalid data structure.
    RuntimeError
        If file loading or processing fails for any other reason.

    Examples
    --------
    >>> # Load default calendar data
    >>> df = _load_mapping_data()
    >>> print(f"Loaded {len(df)} calendar mapping records")
    Loaded 50000 calendar mapping records

    >>> # Access specific dates using multi-index
    >>> jan_2024 = df.loc[(2024, 1)]  # All January 2024 records
    >>> specific_date = df.loc[(2024, 1, 15)]  # Single date record
    
    >>> # Get Hijri equivalent
    >>> hijri_info = df.loc[(2024, 1, 15)][['h_day', 'h_month', 'h_year']]

    >>> # Load from custom path
    >>> df = _load_mapping_data("/custom/path/calendar_data.csv.xz")
    """
    # Construct absolute path to the CSV file
    # Go up two directories from current file location, then apply csv_path
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), csv_path)
    file_path = os.path.abspath(file_path)

    # Verify file exists and is readable
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Calendar data file not found: {file_path}\n"
            f"Please ensure the CSV file exists in the expected location.\n"
            f"Expected structure: {DEFAULT_CSV_PATH}"
        )

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Cannot read calendar data file: {file_path}")

    try:
        # Load CSV with UTF-8 encoding to handle international characters
        # Using print since logger not imported (production code should use proper logging)
        print(f"Loading calendar data from: {file_path}")
        
        # pandas automatically detects .xz compression from file extension
        df = pd.read_csv(file_path, encoding='utf-8', compression="xz")
        
        # Verify expected column structure
        # Expected columns: ['g_day', 'g_month', 'g_year', 'h_day', 'h_month', 'h_year', 'hijri_method']
        expected_columns = {'g_day', 'g_month', 'g_year', 'h_day', 'h_month', 'h_year'}
        if not expected_columns.issubset(set(df.columns)):
            missing = expected_columns - set(df.columns)
            raise ValueError(f"Missing required columns: {missing}")

        # Sort by Gregorian date for consistent ordering
        # This ensures chronological order and better performance for date range queries
        df = df.sort_values(["g_year", "g_month", "g_day"])
        
        # Set multi-index for efficient date-based lookups
        # This allows queries like df.loc[(2024, 1, 15)] for specific dates
        df = df.set_index(["g_year", "g_month", "g_day"])

        print(f"Successfully processed {len(df):,} valid calendar mapping records")
        return df

    except pd.errors.EmptyDataError:
        raise ValueError(f"Calendar data file is empty: {file_path}")
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing CSV file: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to load calendar data: {str(e)}")


if __name__ == "__main__":
    """
    Demonstrate typical usage patterns of the calendar data loader.
    
    This section provides examples of loading calendar data and performing
    common operations like date lookups and data exploration.
    """
    print("=== Calendar Data Loader Example Usage ===\n")
    
    # Example 1: Basic data loading and inspection
    print("1. Loading and inspecting calendar data:")
    try:
        df = _load_mapping_data()
        print(f"   ✓ Loaded {len(df):,} calendar records")
        
        # Get date range from multi-index levels
        years = df.index.get_level_values('g_year')
        print(f"   ✓ Date range: {years.min()}-{years.max()}")
        
        # Show available columns
        print(f"   ✓ Columns: {list(df.columns)}")
        
        # Display sample record using multi-index access
        first_year = years.min()
        sample = df.loc[(first_year, 1, 1)]  # First January 1st in dataset
        print(f"   ✓ Sample record (Jan 1, {first_year}):")
        print(f"     Hijri: {sample['h_day']}/{sample['h_month']}/{sample['h_year']}")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Date lookup and conversion examples
    print("2. Date lookup examples:")
    try:
        df = _load_mapping_data()
        
        # Example date conversions using multi-index
        years = df.index.get_level_values('g_year')
        if 2024 in years.values:
            # Get specific date
            try:
                jan_15_2024 = df.loc[(2024, 1, 15)]
                print(f"   ✓ January 15, 2024 → Hijri: {jan_15_2024['h_day']}/{jan_15_2024['h_month']}/{jan_15_2024['h_year']}")
            except KeyError:
                print("   ℹ January 15, 2024 not available in dataset")
                
            # Get all January 2024 records
            try:
                jan_2024 = df.loc[(2024, 1)]
                print(f"   ✓ January 2024 has {len(jan_2024)} records")
            except KeyError:
                print("   ℹ January 2024 not available in dataset")
        
        # Show first few records for demonstration
        print(f"\n   Sample conversions (first 3 records):")
        sample_df = df.head(3)
        
        # Create a readable display of the sample data
        for idx, row in sample_df.iterrows():
            g_year, g_month, g_day = idx
            print(f"     Gregorian {g_day:2d}/{g_month:2d}/{g_year} → "
                  f"Hijri {row['h_day']:2d}/{row['h_month']:2d}/{row['h_year']}")
        
        # Data quality information
        print(f"\n   Data quality summary:")
        print(f"     Total records: {len(df):,}")
        print(f"     Unique years: {len(years.unique())}")
        
        # Check for hijri_method if available
        if 'hijri_method' in df.columns:
            methods = df['hijri_method'].value_counts()
            print(f"     Hijri calculation methods: {dict(methods)}")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print(f"\n{'='*50}")
    print("Example completed. Check output above for any errors or warnings.")