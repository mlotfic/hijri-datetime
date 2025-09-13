"""
Complete usage examples for the Hijri Date System with HijriDateMapper integration.
"""

import pandas as pd
from typing import Optional

# Import the Hijri date system (assumes the main code is in hijri_dates.py)
# from hijri_dates import HijriDate, iTimedelta, idate


# Sample data for demonstration
sample_data = {
    'g_year': [2024, 2024, 2024, 2024, 2024, 2025, 2025, 2025],
    'g_month': [1, 1, 1, 2, 2, 1, 1, 3],
    'g_day': [15, 16, 17, 10, 11, 5, 6, 20],
    'h_year': [1445, 1445, 1445, 1445, 1445, 1446, 1446, 1446],
    'h_month': [7, 7, 7, 8, 8, 7, 7, 9],
    'h_day': [4, 5, 6, 1, 2, 25, 26, 10],
    'hijri_method': ['ISNA', 'ISNA', 'ISNA', 'ISNA', 'ISNA', 'ISNA', 'ISNA', 'ISNA']
}


class HijriDateMapper:
    def __init__(self, data=None):
        if data is None:
            self.df = pd.DataFrame(sample_data)
        else:
            self.df = data
        print(f"Loaded {len(self.df)} date mappings")
        print("Sample data:")
        print(self.df.head())
    
    def get_dtype(self, year: int, month: Optional[int], day: Optional[int]):
        """Determine the precision level of the date query."""
        if year is not None and month is not None and day is not None:
            return "date"
        elif year is not None and month is not None:
            return "month_range"  
        elif year is not None:
            return "year_range"
        else:
            return "invalid"
    
    def to_hijri(self, year: int, month: Optional[int], day: Optional[int]):
        """
        Convert Gregorian date to Hijri equivalent with index tracking.
        
        Returns
        -------
        tuple
            (result_df, first_index, span) where:
            - result_df: pd.DataFrame with Hijri dates
            - first_index: int or None, DataFrame index of first match
            - span: int, number of rows spanned (last_index - first_index)
        """
        dtype = self.get_dtype(year, month, day)
        
        if dtype == "date":
            mask = ((self.df['g_year'] == year) & 
                    (self.df['g_month'] == month) & 
                    (self.df['g_day'] == day))
            result = self.df[mask]
        elif dtype == "month_range":
            mask = ((self.df['g_year'] == year) & 
                    (self.df['g_month'] == month))
            result = self.df[mask]
        elif dtype == "year_range":
            mask = (self.df['g_year'] == year)
            result = self.df[mask]
        else:
            result = pd.DataFrame()
        
        if result.empty:
            first_index = None
            span = 0
            print(f"   ℹ  Hijri date for Gregorian {year}-{month}-{day} not available in dataset")
        else:
            first_index = result.index[0]
            last_index = result.index[-1]
            span = last_index - first_index
        
        return result, first_index, span
    
    def to_greg(self, year: int, month: Optional[int], day: Optional[int]):
        """
        Convert Hijri date to Gregorian equivalent with index tracking.
        
        Returns
        -------
        tuple
            (result_df, first_index, span) where:
            - result_df: pd.DataFrame with Gregorian dates
            - first_index: int or None, DataFrame index of first match
            - span: int, number of rows spanned (last_index - first_index)
        """
        dtype = self.get_dtype(year, month, day)
        
        if dtype == "date":
            mask = ((self.df['h_year'] == year) &
                    (self.df['h_month'] == month) &
                    (self.df['h_day'] == day))
            result = self.df[mask]
        elif dtype == "month_range":
            mask = ((self.df['h_year'] == year) &
                    (self.df['h_month'] == month))
            result = self.df[mask]
        elif dtype == "year_range":
            mask = (self.df['h_year'] == year)
            result = self.df[mask]
        else:
            result = pd.DataFrame()
        
        if result.empty:
            first_index = None
            span = 0
            print(f"   ℹ  Gregorian date for Hijri {year}-{month}-{day} not available in dataset")
        else:
            first_index = result.index[0]
            last_index = result.index[-1]
            span = last_index - first_index
        
        return result, first_index, span
    
    def get_match_indexes(self, year: int, month: Optional[int], day: Optional[int], date_type: str = 'gregorian'):
        """Get only the indexes and count without loading full data."""
        dtype = self.get_dtype(year, month, day)
        
        if date_type == 'gregorian':
            year_col, month_col, day_col = 'g_year', 'g_month', 'g_day'
        else:  # hijri
            year_col, month_col, day_col = 'h_year', 'h_month', 'h_day'
        
        if dtype == "date":
            mask = ((self.df[year_col] == year) & 
                    (self.df[month_col] == month) & 
                    (self.df[day_col] == day))
        elif dtype == "month_range":
            mask = ((self.df[year_col] == year) & 
                    (self.df[month_col] == month))
        elif dtype == "year_range":
            mask = (self.df[year_col] == year)
        else:
            return None, None, 0
        
        matching_indexes = self.df.index[mask]
        
        if len(matching_indexes) == 0:
            return None, None, 0
        else:
            return matching_indexes[0], matching_indexes[-1], len(matching_indexes)


def demonstrate_hijri_system():
    """Comprehensive demonstration of the Hijri date system."""
    
    print("=" * 60)
    print("🌙 HIJRI DATE SYSTEM DEMONSTRATION 🌙")
    print("=" * 60)
    
    # Initialize the mapper
    mapper = HijriDateMapper()
    print()
    
    print("📅 BASIC HIJRI DATE OPERATIONS")
    print("-" * 40)
    
    # Example 1: Create specific dates using idate()
    print("1. Creating specific dates:")
    d = idate(1447, 2, 5)  
    print(f"   idate(1447, 2, 5) → {d}")
    print(f"   String format: {str(d)}")
    print(f"   ISO format: {d.isoformat()}")
    print()
    
    # Example 2: Create month ranges
    print("2. Creating month ranges:")
    m_start, m_delta = idate(1447, 2)
    print(f"   idate(1447, 2) → {m_start}, {m_delta}")
    print(f"   Month starts: {m_start}")
    print(f"   Duration: {m_delta}")
    print(f"   Month ends: {m_start + m_delta}")
    print()
    
    # Example 3: Create year ranges
    print("3. Creating year ranges:")
    y_start, y_delta = idate(1447)
    print(f"   idate(1447) → {y_start}, {y_delta}")
    print(f"   Year starts: {y_start}")
    print(f"   Duration: {y_delta}")
    print(f"   Year ends: {y_start + y_delta}")
    print()
    
    print("🔢 ARITHMETIC OPERATIONS")
    print("-" * 40)
    
    # Date arithmetic examples
    base_date = idate(1447, 6, 15)
    delta_10 = iTimedelta(days=10)
    delta_30 = iTimedelta(days=30)
    
    print(f"4. Date arithmetic with {base_date}:")
    print(f"   {base_date} + 10 days = {base_date + delta_10}")
    print(f"   {base_date} + 30 days = {base_date + delta_30}")
    print(f"   {base_date} - 5 days = {base_date - iTimedelta(days=5)}")
    print()
    
    # Timedelta arithmetic
    print("5. Timedelta arithmetic:")
    td1 = iTimedelta(days=15)
    td2 = iTimedelta(days=7)
    print(f"   {td1} + {td2} = {td1 + td2}")
    print(f"   {td1} - {td2} = {td1 - td2}")
    print(f"   {td1} * 2 = {td1 * 2}")
    print(f"   {td1} / 3 = {td1 / 3}")
    print()
    
    # Date differences
    print("6. Date differences:")
    date1 = idate(1447, 3, 1)
    date2 = idate(1447, 3, 15)
    date3 = idate(1447, 4, 1)
    
    print(f"   {date2} - {date1} = {date2 - date1}")
    print(f"   {date3} - {date1} = {date3 - date1}")
    print()
    
    print("📊 COMPARISON OPERATIONS")
    print("-" * 40)
    
    print("7. Date comparisons:")
    dates = [
        idate(1447, 2, 15),
        idate(1447, 2, 20),
        idate(1447, 3, 1),
        idate(1446, 12, 29)
    ]
    
    print("   Dates:", [str(d) for d in dates])
    print("   Sorted:", [str(d) for d in sorted(dates)])
    
    print(f"   {dates[0]} < {dates[1]} = {dates[0] < dates[1]}")
    print(f"   {dates[2]} > {dates[0]} = {dates[2] > dates[0]}")
    print(f"   {dates[0]} == {dates[0]} = {dates[0] == dates[0]}")
    print()
    
    print("🔄 INTEGRATION WITH HIJRIDATEMAPPER")
    print("-" * 40)
    
    print("8. Converting Gregorian to Hijri using mapper:")
    # Find a Gregorian date in our sample data
    greg_year, greg_month, greg_day = 2024, 1, 15
    
    result_df, first_idx, span = mapper.to_hijri(greg_year, greg_month, greg_day)
    
    if not result_df.empty:
        row = result_df.iloc[0]
        hijri_date = idate(row['h_year'], row['h_month'], row['h_day'])
        print(f"   Gregorian {greg_year}-{greg_month:02d}-{greg_day:02d}")
        print(f"   → Hijri {hijri_date}")
        print(f"   → Index: {first_idx}, Span: {span}")
    print()
    
    print("9. Converting Hijri to Gregorian using mapper:")
    # Find a Hijri date in our sample data  
    hijri_year, hijri_month, hijri_day = 1445, 7, 4
    
    result_df, first_idx, span = mapper.to_greg(hijri_year, hijri_month, hijri_day)
    
    if not result_df.empty:
        row = result_df.iloc[0]
        hijri_date = idate(hijri_year, hijri_month, hijri_day)
        print(f"   Hijri {hijri_date}")
        print(f"   → Gregorian {row['g_year']}-{row['g_month']:02d}-{row['g_day']:02d}")
        print(f"   → Index: {first_idx}, Span: {span}")
    print()
    
    print("📋 PRACTICAL WORKFLOW EXAMPLES")
    print("-" * 40)
    
    print("10. Working with date ranges:")
    
    # Create a month range and iterate through it
    month_start, month_duration = idate(1447, 6)  # Ramadan example
    print(f"    Month range: {month_start} for {month_duration}")
    
    # Calculate some dates within the month
    week_1 = month_start + iTimedelta(days=7)
    week_2 = month_start + iTimedelta(days=14) 
    mid_month = month_start + iTimedelta(days=15)
    month_end = month_start + month_duration
    
    print(f"    Week 1: {week_1}")
    print(f"    Week 2: {week_2}")
    print(f"    Mid-month: {mid_month}")
    print(f"    Month end: {month_end}")
    print()
    
    print("11. Date validation and error handling:")
    try:
        valid_date = idate(1447, 6, 15)
        print(f"    Valid date: {valid_date}")
        
        # This will raise an error
        invalid_date = HijriDate(1447, 13, 1)  # Invalid month
    except ValueError as e:
        print(f"    Error caught: {e}")
    
    try:
        invalid_day = HijriDate(1447, 6, 31)  # Invalid day
    except ValueError as e:
        print(f"    Error caught: {e}")
    print()
    
    print("🧮 ADVANCED CALCULATIONS")
    print("-" * 40)
    
    print("12. Calculate age in Hijri years:")
    birth_date = idate(1400, 3, 15)
    current_date = idate(1447, 6, 20)
    age_days = current_date - birth_date
    age_years = age_days.days // 354  # Approximate Hijri years
    
    print(f"    Birth date: {birth_date}")
    print(f"    Current date: {current_date}")
    print(f"    Age: {age_days} ({age_years} Hijri years)")
    print()
    
    print("13. Find next occurrence of a specific day:")
    today = idate(1447, 6, 15)
    target_day = 1  # First of month
    
    # Calculate days until next first of month
    days_in_month = 30
    current_day = today.day
    if current_day <= target_day:
        days_until = target_day - current_day
    else:
        days_until = (days_in_month - current_day) + target_day
    
    next_occurrence = today + iTimedelta(days=days_until)
    print(f"    Today: {today}")
    print(f"    Next 1st of month: {next_occurrence}")
    print(f"    Days until: {days_until}")
    print()
    
    print("📚 COLLECTIONS AND SORTING")
    print("-" * 40)
    
    print("14. Working with collections of dates:")
    date_list = [
        idate(1447, 6, 15),
        idate(1447, 6, 1),
        idate(1447, 5, 29),
        idate(1447, 6, 10),
        idate(1447, 7, 1)
    ]
    
    print("    Original list:")
    for i, date in enumerate(date_list):
        print(f"      {i+1}. {date}")
    
    print("    Sorted chronologically:")
    sorted_dates = sorted(date_list)
    for i, date in enumerate(sorted_dates):
        print(f"      {i+1}. {date}")
    
    print("    Using dates as dictionary keys:")
    date_events = {
        idate(1447, 6, 1): "Start of Ramadan",
        idate(1447, 6, 27): "Laylat al-Qadr (estimated)",
        idate(1447, 7, 1): "Eid al-Fitr"
    }
    
    for date, event in sorted(date_events.items()):
        print(f"      {date}: {event}")
    print()
    
    print("⚡ PERFORMANCE AND MEMORY")
    print("-" * 40)
    
    print("15. Bulk date operations:")
    import time
    
    # Create many dates
    start_time = time.time()
    dates = [idate(1447, month, day) 
             for month in range(1, 13) 
             for day in range(1, 31)]
    creation_time = time.time() - start_time
    
    print(f"    Created {len(dates)} dates in {creation_time:.4f} seconds")
    
    # Perform arithmetic on all dates
    start_time = time.time()
    future_dates = [d + iTimedelta(days=100) for d in dates[:100]]  # Sample
    arithmetic_time = time.time() - start_time
    
    print(f"    Performed 100 date additions in {arithmetic_time:.4f} seconds")
    
    # Sort large number of dates
    start_time = time.time()
    sorted_sample = sorted(dates[:100])
    sort_time = time.time() - start_time
    
    print(f"    Sorted 100 dates in {sort_time:.4f} seconds")
    print()
    
    print("🔧 INTEGRATION PATTERNS")
    print("-" * 40)
    
    print("16. Integration with pandas:")
    # Create a pandas Series with HijriDates
    hijri_dates = [idate(1447, 6, day) for day in range(1, 11)]
    df = pd.DataFrame({
        'hijri_date': hijri_dates,
        'event': [f'Day {i}' for i in range(1, 11)],
        'is_weekend': [(d.day % 7 in [5, 6]) for d in hijri_dates]  # Example logic
    })
    
    print("    Sample DataFrame with HijriDates:")
    print(df.head())
    
    # Filter dates
    filtered = df[df['hijri_date'] >= idate(1447, 6, 5)]
    print(f"    Filtered to {len(filtered)} dates >= 1447-06-05")
    print()
    
    print("17. Custom date ranges:")
    def hijri_date_range(start_date, end_date, step_days=1):
        """Generate a range of HijriDates."""
        current = start_date
        while current <= end_date:
            yield current
            current = current + iTimedelta(days=step_days)
    
    start = idate(1447, 6, 1)
    end = idate(1447, 6, 10)
    date_range = list(hijri_date_range(start, end, step_days=2))
    
    print(f"    Date range from {start} to {end} (step=2):")
    for date in date_range:
        print(f"      {date}")
    print()
    
    print("=" * 60)
    print("✅ DEMONSTRATION COMPLETE")
    print("=" * 60)
    
    print("\n📖 SUMMARY OF FEATURES:")
    print("   ✓ HijriDate objects with full comparison support")
    print("   ✓ iTimedelta for duration arithmetic")
    print("   ✓ idate() factory with flexible signatures")
    print("   ✓ Full arithmetic operations (+, -, *, /)")
    print("   ✓ Integration with pandas and collections")
    print("   ✓ Production-ready error handling")
    print("   ✓ Memory efficient and performant")
    print("   ✓ Extensible for real Hijri calendar systems")


if __name__ == "__main__":
    demonstrate_hijri_system()