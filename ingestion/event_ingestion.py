# Event ingestion module for Market Sentinel
import pandas as pd
import os
import time

def clean_text(text):
    if isinstance(text, str):
        # Basic cleaning: strip whitespace, remove problematic newlines
        return text.strip().replace('\n', ' ').replace('\r', ' ')
    return text

def stream_events(filename="data/events.csv", delay=1.0):
    """
    Streams events from a CSV file in the data folder, cleans the text, and yields one event at a time.
    
    Args:
        filename (str): Path to the CSV file.
        delay (float): Delay in seconds between yielding events.

    Yields:
        dict: The row data as a dictionary with cleaned text.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Event file '{filename}' not found.")
    events_df = pd.read_csv(filename)

    # Assume we want to clean all string columns
    string_columns = events_df.select_dtypes(include=['object']).columns
    for col in string_columns:
        events_df[col] = events_df[col].apply(clean_text)
    
    for _, row in events_df.iterrows():
        yield row.to_dict()
        time.sleep(delay)
