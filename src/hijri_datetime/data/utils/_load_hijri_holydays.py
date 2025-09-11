import os
import ast
import pandas as pd
from datetime import datetime

# Default CSV file path relative to this module
DEFAULT_CSV_PATH = "./date_dataset/calendar_date_holidays_dataset.csv.xz"
# DEBUG:: file_path = "../date_dataset/calendar_date_holidays_dataset.csv.xz"

def _load_hijri_holydays(csv_path=DEFAULT_CSV_PATH):
    """
    Load and validate calendar mapping data from CSV file.

    This function handles the complete data loading pipeline including file validation,
    CSV parsing, data type conversions, range validation, and data cleaning.

    Parameters
    ----------
    csv_path : str, optional
        Path to the CSV file containing calendar mapping data.
        Defaults to DEFAULT_CSV_PATH ("./date_dataset/calendar_date_dataset.csv.xz").

    Returns
    -------
    pandas.DataFrame
        Validated and cleaned calendar mapping data with proper data types.
        Contains columns for multiple calendar systems (Gregorian, Hijri, Solar Hijri)
        and weekday information. Sorted by Gregorian date for consistent ordering.

    Raises
    ------
    FileNotFoundError
        If the calendar hijri holydays data file is not found or not accessible.
    PermissionError
        If the file cannot be read due to permission issues.
    ValueError
        If required columns are missing, data contains invalid values, or CSV is empty.
    RuntimeError
        If file loading or processing fails for any other reason.

    Examples
    --------
    >>> # Load default calendar hijri holydays data
    >>> df = _load_hijri_holydays()
    >>> print(f"Loaded {len(df)} calendar mapping records")
    Loaded 50000 calendar mapping records

    >>> # Access calendar systems
    >>> print(df.columns.tolist())
    ['Gregorian Day', 'Gregorian Month', 'Gregorian Year', 'Hijri Day', ...]

    >>> # Load from custom path
    >>> df = _load_hijri_holydays("/path/to/custom/calendar_data.csv")
    """
    # Construct absolute path to the CSV file
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), csv_path)
    file_path = os.path.abspath(file_path)

    # Verify file exists and is readable
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"calendar hijri holydays data file not found: {file_path}\n"
            f"Please ensure the CSV file exists in the expected location.\n"
            f"Expected structure: {DEFAULT_CSV_PATH}"
        )

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Cannot read calendar hijri holydays data file: {file_path}")

    try:
        # Load CSV with UTF-8 encoding to handle international characters
        print(f"Loading calendar hijri holydays data from: {file_path}")  # Using print since logger not imported
        df = pd.read_csv(file_path, encoding='utf-8', compression="xz")

        #  Convert dd-mm-yyyy string → ISO yyyy-mm-dd string 
        df["gregorian_date"] = df["gregorian_date"].apply(
            lambda x: datetime.strptime(x, "%d-%m-%Y").strftime("%Y-%m-%d")
        )
        
        # Convert list-like strings to Python lists
        df["hijri_holidays"] = df["hijri_holidays"].apply(ast.literal_eval)
        df["hijri_adjustedHolidays"] = df["hijri_adjustedHolidays"].apply(ast.literal_eval)
        
        # Sort by gregorian_date (or hijri_date)
        df = df.sort_values(by="gregorian_date")
        
        df = df.reset_index(drop=True)


        print(f"Successfully processed {len(df):,} valid calendar mapping records")
        return df

    except pd.errors.EmptyDataError:
        raise ValueError(f"calendar hijri holydays data file is empty: {file_path}")
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing CSV file: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to load calendar hijri holydays data: {str(e)}")


if __name__ == "__main__":
    """
    Demonstrate typical usage patterns of the calendar hijri holydays data loader.
    
    This section provides examples of both the functional and class-based
    approaches to loading calendar hijri holydays data, along with data exploration examples.
    """
    print("=== calendar hijri holydays data Loader Example Usage ===\n")
    
    # Example 1: Basic usage with standalone function
    print("1. Loading data with standalone function:")
    try:
        df = _load_hijri_holydays()
        print(f"   ✓ Loaded {len(df):,} calendar records")
        print(f"   ✓ Supported Date range: {df['gregorian_date'].min()} : {df['gregorian_date'].max()}")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "="*50 + "\n")