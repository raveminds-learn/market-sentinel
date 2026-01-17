"""
Test script for analytics functionality.
"""

import sys
import os
import logging

# Add parent directory to path to allow importing from sibling modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics.historical_analytics import load_price_data, get_price_summary, compute_event_reaction

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('analytics_test')

def test_load_price_data():
    """
    Test the load_price_data function.
    """
    print("Testing load_price_data function...")
    print("=" * 40)

    # Test with the price_data.csv file
    csv_file = "data/price_data.csv"

    try:
        # First, let's show DuckDB schema and data directly
        import duckdb
        import os

        logger.info(f"Starting DuckDB analysis for file: {csv_file}")
        print("DuckDB Direct Analysis:")
        print("-" * 25)

        # Create DuckDB connection
        logger.info("Creating DuckDB in-memory connection")
        con = duckdb.connect(database=':memory:')

        # Determine table name
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        logger.info(f"Using table name: {table_name}")

        # Load CSV into DuckDB
        query = f"""
        CREATE TABLE {table_name} AS
        SELECT * FROM read_csv_auto('{csv_file}')
        """
        logger.info(f"Executing query: CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_file}')")
        con.execute(query)

        # Show schema
        logger.info("Retrieving table schema")
        print("Schema:")
        schema_result = con.execute(f"DESCRIBE {table_name}").fetchall()
        schema_info = []
        for col in schema_result:
            col_info = f"{col[0]}: {col[1]}"
            schema_info.append(col_info)
            print(f"  {col_info}")
        logger.info(f"Table schema: {', '.join(schema_info)}")
        print()

        # Show data
        logger.info("Retrieving first 5 rows of data")
        print("Data (first 5 rows):")
        data_result = con.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchall()
        headers = [col[0] for col in schema_result]

        # Print headers
        print(" | ".join(f"{h:<12}" for h in headers))
        print("-" * (len(headers) * 14))

        # Print data rows
        for i, row in enumerate(data_result):
            formatted_row = []
            for val in row:
                if isinstance(val, float):
                    formatted_row.append(f"{val:<12.2f}")
                else:
                    formatted_row.append(f"{str(val):<12}")
            row_str = " | ".join(formatted_row)
            print(row_str)
            logger.info(f"Row {i+1}: {row_str}")

        logger.info(f"Retrieved {len(data_result)} data rows")
        print()

        # Show some SQL aggregations
        logger.info("Running SQL aggregations by symbol")
        print("DuckDB SQL Aggregations:")
        agg_query = f"""
        SELECT
            symbol,
            COUNT(*) as records,
            ROUND(AVG(close), 2) as avg_close,
            ROUND(MIN(close), 2) as min_close,
            ROUND(MAX(close), 2) as max_close
        FROM {table_name}
        GROUP BY symbol
        ORDER BY symbol
        """
        logger.info(f"Executing aggregation query: {agg_query.strip()}")
        agg_result = con.execute(agg_query).fetchall()

        print("Ticker | Records | Avg Close | Min Close | Max Close")
        print("-" * 50)
        for row in agg_result:
            row_str = f"{row[0]:<8} | {row[1]:<8} | ${row[2]:<10} | ${row[3]:<10} | ${row[4]:<10}"
            print(row_str)
            logger.info(f"Aggregation result: {row_str}")

        logger.info(f"Completed aggregations for {len(agg_result)} symbols")
        con.close()
        logger.info("DuckDB connection closed")
        print()

        # Now test the pandas conversion
        df = load_price_data(csv_file)

        print("Pandas DataFrame Analysis:")
        print("-" * 30)
        print(f"DataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Sample data:")
        print(df.head(3))
        print()

        # Test summary function
        summary = get_price_summary(df)
        print("Price Data Summary:")
        print(f"Total rows: {summary.get('total_rows', 'N/A')}")
        print(f"Date range: {summary.get('date_range', {})}")

        if 'numeric_stats' in summary:
            print("Numeric column statistics:")
            for col, stats in summary['numeric_stats'].items():
                print(f"  {col}: mean={stats['mean']:.2f}, min={stats['min']:.2f}, max={stats['max']:.2f}")

        print("\nSUCCESS: Price data loaded successfully!")
        return True

    except Exception as e:
        print(f"ERROR: Failed to load price data: {e}")
        return False

def test_load_nonexistent_file():
    """
    Test error handling for non-existent files.
    """
    print("\nTesting error handling for non-existent files...")
    print("=" * 50)

    try:
        df = load_price_data("data/nonexistent_file.csv")
        print("ERROR: Should have raised FileNotFoundError")
        return False
    except FileNotFoundError:
        print("SUCCESS: Correctly raised FileNotFoundError for non-existent file")
        return True
    except Exception as e:
        print(f"ERROR: Unexpected exception: {e}")
        return False

def test_compute_event_reaction():
    """
    Test the compute_event_reaction function.
    """
    print("\nTesting compute_event_reaction function...")
    print("=" * 50)

    try:
        # Load price data
        df = load_price_data("data/price_data.csv")

        # Test with AAPL on 2024-01-17 (last date in our data range)
        ticker = "AAPL"
        event_date = "2024-01-17"

        result = compute_event_reaction(df, ticker, event_date)

        if 'error' in result:
            print(f"ERROR: {result['error']}")
            return False

        print("Event Reaction Analysis Result:")
        print(f"Ticker: {result.get('ticker', 'N/A')}")
        print(f"Event Date: {result.get('event_date', 'N/A')}")
        print(f"Event Date Found: {result.get('event_date_found', 'N/A')}")
        print(f"Event Price: ${result.get('event_price', 'N/A'):.2f}")

        # Print returns
        for days in [1, 3, 5]:
            return_key = f'{days}_day_return'
            if return_key in result and result[return_key] is not None:
                ret = result[return_key] * 100  # Convert to percentage
                price_key = f'{days}_day_price'
                date_key = f'{days}_day_date'
                print(f"{days}-day return: {ret:.2f}%")
                print(f"  Price: ${result.get(price_key, 'N/A'):.2f} on {result.get(date_key, 'N/A')}")
            else:
                print(f"{days}-day return: No data available")

        # Print volatility
        vol_data = result.get('volatility_20_day', {})
        if 'daily_volatility' in vol_data:
            daily_vol = vol_data['daily_volatility'] * 100  # Convert to percentage
            ann_vol = vol_data['annualized_volatility'] * 100
            print(f"20-day volatility: Daily={daily_vol:.2f}%, Annualized={ann_vol:.2f}%")
            print(f"  Sample Size: {vol_data.get('sample_size', 'N/A')} trading days")
            print(f"  Period: {vol_data.get('period_start', 'N/A')} to {vol_data.get('period_end', 'N/A')}")
        else:
            print(f"20-day volatility: {vol_data.get('error', 'No data available')}")

        print("\nSUCCESS: Event reaction analysis completed successfully!")
        return True

    except Exception as e:
        print(f"ERROR: Failed to compute event reaction: {e}")
        return False

def main():
    """Run all analytics tests"""
    print("Running Analytics Module tests...\n")

    # Test successful loading
    success1 = test_load_price_data()

    # Test error handling
    success2 = test_load_nonexistent_file()

    # Test event reaction computation
    success3 = test_compute_event_reaction()

    print("\n" + "=" * 50)
    print("Analytics Test Summary:")
    print(f"Load price data: {'PASS' if success1 else 'FAIL'}")
    print(f"Error handling: {'PASS' if success2 else 'FAIL'}")
    print(f"Event reaction: {'PASS' if success3 else 'FAIL'}")

    if success1 and success2 and success3:
        print("SUCCESS: All analytics tests passed!")
    else:
        print("FAILURE: Some tests failed!")

if __name__ == "__main__":
    main()