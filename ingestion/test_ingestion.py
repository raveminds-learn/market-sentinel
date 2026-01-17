"""
Test script that loads news_sample.csv and prints the first 3 streamed events.
"""

import csv
import os
import time

def stream_news_events(filename="data/news_sample.csv", delay=1.0):
    """
    Streams events from news_sample.csv and yields one event at a time.

    Args:
        filename (str): Path to the CSV file
        delay (float): Delay in seconds between yielding events

    Yields:
        dict: The row data as a dictionary
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"News file '{filename}' not found.")

    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row
            time.sleep(delay)

def main():
    """
    Load news_sample.csv and print the first 3 streamed events.
    """
    print("Loading news_sample.csv and streaming first 3 events...")
    print("=" * 55)

    try:
        event_count = 0
        for event in stream_news_events(delay=0.5):
            event_count += 1
            print(f"\nEvent #{event_count}:")
            print(f"Date: {event.get('date', 'N/A')}")
            print(f"Title: {event.get('title', 'N/A')}")
            content = event.get('content', 'N/A')
            print(f"Content: {content[:100]}..." if len(content) > 100 else f"Content: {content}")
            print(f"Source: {event.get('source', 'N/A')}")
            print(f"Sentiment Score: {event.get('sentiment_score', 'N/A')}")
            print(f"Impact Score: {event.get('impact_score', 'N/A')}")

            if event_count >= 3:
                print(f"\nStopped after {event_count} events (as requested)")
                break

        print(f"\nSuccessfully streamed {event_count} events from news_sample.csv")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure the data/news_sample.csv file exists")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()