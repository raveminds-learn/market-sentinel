# Historical Analytics Module for Market Sentinel

import duckdb
import pandas as pd
from typing import Optional

def load_price_data(csv_file_path: str, table_name: Optional[str] = None) -> pd.DataFrame:
    """
    Load price data from a CSV file using DuckDB and return as pandas DataFrame.

    Args:
        csv_file_path (str): Path to the CSV file containing price data
        table_name (Optional[str]): Optional table name for the data (defaults to filename)

    Returns:
        pd.DataFrame: DataFrame containing the loaded price data

    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        Exception: For other loading errors
    """
    try:
        # Create DuckDB connection
        con = duckdb.connect(database=':memory:')

        # If no table name provided, use filename without extension
        if table_name is None:
            import os
            table_name = os.path.splitext(os.path.basename(csv_file_path))[0]

        # Load CSV into DuckDB
        query = f"""
        CREATE TABLE {table_name} AS
        SELECT * FROM read_csv_auto('{csv_file_path}')
        """

        con.execute(query)

        # Convert to pandas DataFrame
        df = con.execute(f"SELECT * FROM {table_name}").fetchdf()

        # Close connection
        con.close()

        print(f"Successfully loaded {len(df)} rows from {csv_file_path} using DuckDB")
        return df

    except Exception as e:
        error_msg = str(e)
        if "No files found" in error_msg or "file does not exist" in error_msg.lower():
            raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
        else:
            raise Exception(f"Error loading CSV with DuckDB: {error_msg}")

def get_price_summary(df: pd.DataFrame) -> dict:
    """
    Generate basic summary statistics for price data.

    Args:
        df (pd.DataFrame): DataFrame containing price data

    Returns:
        dict: Summary statistics
    """
    try:
        summary = {
            'total_rows': len(df),
            'columns': list(df.columns),
            'date_range': {
                'start': df['date'].min() if 'date' in df.columns else None,
                'end': df['date'].max() if 'date' in df.columns else None
            }
        }

        # Add numeric column statistics
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            summary['numeric_stats'] = {}
            for col in numeric_cols:
                summary['numeric_stats'][col] = {
                    'mean': df[col].mean(),
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'std': df[col].std()
                }

        return summary

    except Exception as e:
        return {'error': f'Failed to generate summary: {str(e)}'}

def compute_event_reaction(price_df: pd.DataFrame, ticker: str, event_date: str, days_before: int = 30, days_after: int = 30) -> dict:
    """
    Compute event reaction metrics including returns and volatility for a given ticker and event date.

    Args:
        price_df (pd.DataFrame): DataFrame containing price data with columns: date, symbol, close (and others)
        ticker (str): Stock ticker symbol (e.g., 'AAPL')
        event_date (str): Event date in 'YYYY-MM-DD' format
        days_before (int): Number of days before event to include in analysis
        days_after (int): Number of days after event to include in analysis

    Returns:
        dict: Dictionary containing return calculations and volatility metrics
    """
    try:
        # Convert event_date to datetime
        event_dt = pd.to_datetime(event_date)

        # Filter data for the specific ticker
        ticker_data = price_df[price_df['symbol'].str.upper() == ticker.upper()].copy()

        if len(ticker_data) == 0:
            return {'error': f'No data found for ticker: {ticker}'}

        # Ensure date column is datetime
        ticker_data['date'] = pd.to_datetime(ticker_data['date'])

        # Sort by date
        ticker_data = ticker_data.sort_values('date')

        # Define analysis window
        start_date = event_dt - pd.Timedelta(days=days_before)
        end_date = event_dt + pd.Timedelta(days=days_after)

        # Filter data within the analysis window
        window_data = ticker_data[
            (ticker_data['date'] >= start_date) &
            (ticker_data['date'] <= end_date)
        ].copy()

        if len(window_data) < 2:
            return {'error': f'Insufficient data for analysis. Need at least 2 data points, got {len(window_data)}'}

        # Calculate daily returns
        window_data['daily_return'] = window_data['close'].pct_change()

        # Find event date in the data (or closest trading day)
        event_mask = window_data['date'] >= event_dt
        if event_mask.any():
            event_idx = event_mask.idxmax()
            event_row = window_data.loc[event_idx]
        else:
            return {'error': f'Event date {event_date} not found in data range'}

        # Get event date index
        event_date_in_data = event_row['date']

        # Calculate returns from event date
        results = {
            'ticker': ticker,
            'event_date': event_date,
            'event_date_found': event_date_in_data.strftime('%Y-%m-%d'),
            'event_price': event_row['close']
        }

        # Calculate N-day returns (1, 3, 5 days after event)
        for days in [1, 3, 5]:
            try:
                future_date = event_date_in_data + pd.Timedelta(days=days)

                # Find the closest trading day within a reasonable range
                future_mask = (window_data['date'] >= future_date - pd.Timedelta(days=2)) & \
                             (window_data['date'] <= future_date + pd.Timedelta(days=2))

                if future_mask.any():
                    future_row = window_data[future_mask].iloc[0]  # Take the first match
                    future_price = future_row['close']
                    n_day_return = (future_price - event_row['close']) / event_row['close']

                    results[f'{days}_day_return'] = n_day_return
                    results[f'{days}_day_price'] = future_price
                    results[f'{days}_day_date'] = future_row['date'].strftime('%Y-%m-%d')
                else:
                    results[f'{days}_day_return'] = None
                    results[f'{days}_day_note'] = f'No trading data found around {future_date.strftime("%Y-%m-%d")}'

            except Exception as e:
                results[f'{days}_day_return'] = None
                results[f'{days}_day_error'] = str(e)

        # Calculate 20-day volatility (standard deviation of daily returns)
        # Use data from 20 trading days before to 20 trading days after event
        try:
            # Get data around event date (±20 trading days)
            vol_start_idx = max(0, event_idx - 20)
            vol_end_idx = min(len(window_data), event_idx + 21)  # +21 to include event day

            vol_data = window_data.iloc[vol_start_idx:vol_end_idx]

            if len(vol_data) >= 10:  # Need reasonable amount of data
                # Calculate volatility (annualized by multiplying by sqrt(252))
                daily_volatility = vol_data['daily_return'].std()
                annualized_volatility = daily_volatility * (252 ** 0.5)  # 252 trading days in a year

                results['volatility_20_day'] = {
                    'daily_volatility': daily_volatility,
                    'annualized_volatility': annualized_volatility,
                    'sample_size': len(vol_data),
                    'period_start': vol_data['date'].min().strftime('%Y-%m-%d'),
                    'period_end': vol_data['date'].max().strftime('%Y-%m-%d')
                }
            else:
                results['volatility_20_day'] = {
                    'error': f'Insufficient data for volatility calculation. Need at least 10 data points, got {len(vol_data)}'
                }

        except Exception as e:
            results['volatility_20_day'] = {'error': f'Failed to calculate volatility: {str(e)}'}

        return results

    except Exception as e:
        return {'error': f'Failed to compute event reaction: {str(e)}'}
