# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 14:17:48 2025

@author: m
"""

import pandas as pd
from typing import Optional

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

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def main():
    # Initialize the mapper
    mapper = HijriDateMapper()
    
    print("\n" + "="*80)
    print("EXAMPLE 1: Convert Specific Gregorian Date to Hijri")
    print("="*80)
    
    # Convert January 15, 2024 to Hijri
    hijri_df, first_idx, last_idx = mapper.to_hijri(2024, 1, 15)
    
    if not hijri_df.empty:
        print(f"✅ Found {len(hijri_df)} match(es)")
        print(f"📍 DataFrame indexes: {first_idx} to {last_idx}")
        print(f"🗓️  Gregorian 2024-01-15 = Hijri {hijri_df.iloc[0]['h_year']}-{hijri_df.iloc[0]['h_month']}-{hijri_df.iloc[0]['h_day']}")
        print(f"📊 Result DataFrame:")
        print(hijri_df[['h_year', 'h_month', 'h_day', 'hijri_method']])
    else:
        print("❌ No matches found")
    
    print("\n" + "="*80)
    print("EXAMPLE 2: Convert Specific Hijri Date to Gregorian")
    print("="*80)
    
    # Convert Rajab 4, 1445 to Gregorian
    greg_df, first_idx, last_idx = mapper.to_greg(1445, 7, 4)
    
    if not greg_df.empty:
        print(f"✅ Found {len(greg_df)} match(es)")
        print(f"📍 DataFrame indexes: {first_idx} to {last_idx}")
        print(f"🗓️  Hijri 1445-07-04 = Gregorian {greg_df.iloc[0]['g_year']}-{greg_df.iloc[0]['g_month']:02d}-{greg_df.iloc[0]['g_day']:02d}")
        print(f"📊 Result DataFrame:")
        print(greg_df[['g_year', 'g_month', 'g_day', 'hijri_method']])
    else:
        print("❌ No matches found")
    
    print("\n" + "="*80)
    print("EXAMPLE 3: Get All Dates for a Specific Month")
    print("="*80)
    
    # Get all dates for January 2024
    hijri_df, first_idx, last_idx = mapper.to_hijri(2024, 1, None)
    
    print(f"🗓️  All Hijri dates for Gregorian January 2024:")
    print(f"✅ Found {len(hijri_df)} match(es)")
    print(f"📍 DataFrame indexes: {first_idx} to {last_idx}")
    if not hijri_df.empty:
        print(f"📊 Results:")
        display_df = hijri_df[['g_year', 'g_month', 'g_day', 'h_year', 'h_month', 'h_day']]
        for _, row in display_df.iterrows():
            print(f"   Gregorian {row['g_year']}-{row['g_month']:02d}-{row['g_day']:02d} = Hijri {row['h_year']}-{row['h_month']:02d}-{row['h_day']:02d}")
    
    print("\n" + "="*80)
    print("EXAMPLE 4: Get All Dates for a Specific Year")
    print("="*80)
    
    # Get all dates for 2024
    hijri_df, first_idx, last_idx = mapper.to_hijri(2024, None, None)
    
    print(f"🗓️  All Hijri dates for Gregorian year 2024:")
    print(f"✅ Found {len(hijri_df)} match(es)")
    print(f"📍 DataFrame indexes: {first_idx} to {last_idx}")
    if not hijri_df.empty:
        print(f"📊 Year 2024 spans Hijri years: {hijri_df['h_year'].min()} to {hijri_df['h_year'].max()}")
        print(f"   First date: Gregorian {hijri_df.iloc[0]['g_year']}-{hijri_df.iloc[0]['g_month']:02d}-{hijri_df.iloc[0]['g_day']:02d}")
        print(f"   Last date:  Gregorian {hijri_df.iloc[-1]['g_year']}-{hijri_df.iloc[-1]['g_month']:02d}-{hijri_df.iloc[-1]['g_day']:02d}")
    
    print("\n" + "="*80)
    print("EXAMPLE 5: Performance Optimization - Get Only Indexes")
    print("="*80)
    
    # Just get index information without loading full data
    first_idx, last_idx, count = mapper.get_match_indexes(2024, 1, None, 'gregorian')
    
    print(f"🚀 Quick index lookup for January 2024:")
    print(f"📍 Indexes: {first_idx} to {last_idx}")
    print(f"🔢 Count: {count} matches")
    print(f"💡 This is faster when you only need to know the range/count")
    
    print("\n" + "="*80)
    print("EXAMPLE 6: Error Handling - Non-existent Date")
    print("="*80)
    
    # Try to find a date that doesn't exist in our dataset
    hijri_df, first_idx, last_idx = mapper.to_hijri(2030, 12, 25)
    print(f"Indexes returned: first={first_idx}, last={last_idx}")
    print(f"DataFrame empty: {hijri_df.empty}")
    
    print("\n" + "="*80)
    print("EXAMPLE 7: Working with Index Ranges for Data Processing")
    print("="*80)
    
    # Get a range and then process specific rows
    hijri_df, first_idx, last_idx = mapper.to_hijri(2024, None, None)
    
    if not hijri_df.empty:
        print(f"📊 Processing rows {first_idx} to {last_idx} from the original dataset:")
        
        # You can now use these indexes to work with the original DataFrame
        original_slice = mapper.df.iloc[first_idx:last_idx+1]
        
        print(f"   Original DataFrame slice:")
        print(original_slice)
        
        # Calculate some statistics
        print(f"\n📈 Statistics for 2024:")
        print(f"   Gregorian months covered: {sorted(original_slice['g_month'].unique())}")
        print(f"   Hijri months covered: {sorted(original_slice['h_month'].unique())}")
        print(f"   Total days: {len(original_slice)}")
    
    print("\n" + "="*80)
    print("EXAMPLE 8: Batch Processing with Index Information")
    print("="*80)
    
    # Process multiple date queries and collect index information
    queries = [
        (2024, 1, 15),   # Specific date
        (2024, 2, None), # Whole month
        (2025, None, None), # Whole year
    ]
    
    results = []
    for year, month, day in queries:
        hijri_df, first_idx, last_idx = mapper.to_hijri(year, month, day)
        results.append({
            'query': f"{year}-{month}-{day}",
            'matches': len(hijri_df),
            'first_index': first_idx,
            'last_index': last_idx,
            'span': last_idx - first_idx + 1 if first_idx is not None else 0
        })
    
    print("📊 Batch processing results:")
    for result in results:
        print(f"   Query {result['query']}: {result['matches']} matches, "
              f"indexes {result['first_index']}-{result['last_index']}, "
              f"span {result['span']} rows")
        
# =============================================================================
# USAGE EXAMPLES WITH SPAN TRACKING
# =============================================================================

def run_examples():
    print("🚀 Initializing Hijri Date Mapper...")
    mapper = HijriDateMapper()
    
    print("\n" + "="*70)
    print("EXAMPLE 1: Single Date Conversion with Span")
    print("="*70)
    
    # Convert specific date
    result, first_idx, span = mapper.to_hijri(2024, 1, 15)
    print(f"Query: Gregorian 2024-01-15")
    print(f"Results: {len(result)} matches")
    print(f"First index: {first_idx}")
    print(f"Span: {span} rows")
    if not result.empty:
        print(f"Hijri equivalent: {result.iloc[0]['h_year']}-{result.iloc[0]['h_month']:02d}-{result.iloc[0]['h_day']:02d}")
    
    print("\n" + "="*70)
    print("EXAMPLE 2: Month Range with Span Analysis")
    print("="*70)
    
    # Get all January 2024 dates
    result, first_idx, span = mapper.to_hijri(2024, 1, None)
    print(f"Query: All of January 2024")
    print(f"Results: {len(result)} matches")
    print(f"First index: {first_idx}")
    print(f"Span: {span} rows (from index {first_idx} to {first_idx + span})")
    print(f"Data coverage: {span + 1} total positions in DataFrame")
    
    if not result.empty:
        print("\nDate mappings found:")
        for _, row in result.iterrows():
            print(f"  {row['g_year']}-{row['g_month']:02d}-{row['g_day']:02d} → "
                  f"{row['h_year']}-{row['h_month']:02d}-{row['h_day']:02d}")
    
    print("\n" + "="*70)
    print("EXAMPLE 3: Year Range Analysis")
    print("="*70)
    
    # Get all 2024 dates
    result, first_idx, span = mapper.to_hijri(2024, None, None)
    print(f"Query: All of year 2024")
    print(f"Results: {len(result)} matches")
    print(f"First index: {first_idx}")
    print(f"Span: {span} rows")
    
    if not result.empty:
        print(f"Year 2024 data distribution:")
        print(f"  Covers DataFrame positions: {first_idx} to {first_idx + span}")
        print(f"  Percentage of dataset: {((span + 1) / len(mapper.df)) * 100:.1f}%")
        
        # Show distribution by months
        month_counts = result.groupby('g_month').size()
        print(f"  Monthly distribution:")
        for month, count in month_counts.items():
            print(f"    Month {month:02d}: {count} days")
    
    print("\n" + "="*70)
    print("EXAMPLE 4: Comparing Span vs Count")
    print("="*70)
    
    # Demonstrate the difference between span and count
    test_cases = [
        (2024, 1, None),    # Month range
        (2024, None, None), # Year range
        (1445, 7, None),    # Hijri month
    ]
    
    print("Understanding Span vs Count:")
    print("- Span = last_index - first_index (DataFrame position difference)")
    print("- Count = actual number of matching records")
    print()
    
    for i, (year, month, day) in enumerate(test_cases, 1):
        if i <= 2:  # Gregorian queries
            result, first_idx, span = mapper.to_hijri(year, month, day)
            query_type = "Gregorian"
        else:  # Hijri query
            result, first_idx, span = mapper.to_greg(year, month, day)
            query_type = "Hijri"
        
        count = len(result)
        print(f"Query {i}: {query_type} {year}-{month}-{day}")
        print(f"  Count: {count} actual matches")
        print(f"  Span:  {span} index positions")
        print(f"  Efficiency: {count/(span+1) if span >= 0 else 'N/A':.2f} " +
              f"(matches per position)")
    
    print("\n" + "="*70)
    print("EXAMPLE 5: Using Range Info Helper Function")
    print("="*70)
    
    # Use the helper function for detailed range analysis
    range_info = mapper.get_date_range_info(2024, 1, None, 'gregorian')
    
    print(f"Range analysis for January 2024:")
    print(f"  Query type: {range_info['query_type']}")
    print(f"  First index: {range_info['first_index']}")
    print(f"  Last index: {range_info['last_index']}")
    print(f"  Span: {range_info['span']}")
    print(f"  Count: {range_info['count']}")
    
    if range_info['count'] > 0:
        density = range_info['count'] / (range_info['span'] + 1)
        print(f"  Data density: {density:.2f} (how packed the matches are)")
    
    print("\n" + "="*70)
    print("EXAMPLE 6: Practical Applications of Span")
    print("="*70)
    
    print("Practical uses of span information:")
    print()
    
    # Memory estimation
    result, first_idx, span = mapper.to_hijri(2024, None, None)
    if first_idx is not None:
        print(f"1. Memory Planning:")
        print(f"   - To slice original data: df.iloc[{first_idx}:{first_idx + span + 1}]")
        print(f"   - Memory footprint: {span + 1} rows × {len(mapper.df.columns)} columns")
    
    # Performance optimization
    print(f"\n2. Performance Optimization:")
    print(f"   - Small span ({span}) = Efficient slicing operations")
    print(f"   - Large span = Consider filtering instead of slicing")
    
    # Data validation
    print(f"\n3. Data Quality Check:")
    count = len(result)
    if span >= 0:
        coverage = count / (span + 1)
        print(f"   - Data coverage: {coverage:.2f} (1.0 = no gaps, <1.0 = sparse data)")
        if coverage < 0.5:
            print(f"   - ⚠️  Warning: Sparse data detected - many gaps in date sequence")
        else:
            print(f"   - ✅ Good: Dense data with few gaps")


if __name__ == "__main__":
    main()