"""
Test script for RAG (Retrieval-Augmented Generation) functionality.
"""

import sys
import os

# Add parent directory to path to allow importing from sibling modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.context_retrieval import build_event_index, retrieve_relevant_context, retrieve_similar_events

def test_build_event_index():
    """
    Test the build_event_index function.
    """
    print("Testing build_event_index function...")
    print("=" * 50)

    # Test with the news_sample.csv file
    csv_file = "data/news_sample.csv"

    try:
        result = build_event_index(csv_file_path=csv_file, collection_name="test_market_events")

        print("Build Event Index Result:")
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Collection Name: {result.get('collection_name', 'N/A')}")
        print(f"Document Count: {result.get('document_count', 'N/A')}")
        print(f"Embedding Dimension: {result.get('embedding_dimension', 'N/A')}")

        if result.get('status') == 'success':
            print("\nSUCCESS: Event index built successfully!")
        elif result.get('status') == 'partial':
            print(f"\nPARTIAL SUCCESS: {result.get('message', 'Some features not available')}")
        else:
            print(f"\nERROR: {result.get('error', 'Unknown error')}")

        return result

    except Exception as e:
        print(f"Unexpected error during testing: {e}")
        return {"status": "error", "error": str(e)}

def test_retrieve_relevant_context():
    """
    Test the retrieve_relevant_context function.
    """
    print("\nTesting retrieve_relevant_context function...")
    print("=" * 50)

    # Test query
    query = "Tesla investigation"

    try:
        result = retrieve_relevant_context(
            query=query,
            collection_name="test_market_events",
            n_results=3
        )

        print("Retrieve Context Result:")
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Query: {result.get('query', 'N/A')}")

        if result.get('status') == 'success':
            documents = result.get('documents', [])
            metadatas = result.get('metadatas', [])
            distances = result.get('distances', [])

            print(f"\nRetrieved {len(documents)} relevant documents:")

            for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
                print(f"\nDocument {i+1} (distance: {distance:.4f}):")
                print(f"Title: {metadata.get('title', 'N/A')}")
                print(f"Date: {metadata.get('date', 'N/A')}")
                print(f"Source: {metadata.get('source', 'N/A')}")
                print(f"Sentiment: {metadata.get('sentiment_score', 'N/A')}")
                print(f"Content: {doc[:100]}..." if len(doc) > 100 else f"Content: {doc}")

            print("\nSUCCESS: Context retrieval completed successfully!")
        else:
            print(f"\nERROR: {result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"Unexpected error during context retrieval: {e}")

def test_retrieve_similar_events():
    """
    Test the retrieve_similar_events function.
    """
    print("\nTesting retrieve_similar_events function...")
    print("=" * 50)

    # Test headline
    headline = "Apple announces major product recall"

    try:
        result = retrieve_similar_events(
            headline=headline,
            collection_name="test_market_events",
            top_k=3
        )

        print("Retrieve Similar Events Result:")
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Query Headline: {result.get('query_headline', 'N/A')}")

        if result.get('status') == 'success':
            similar_events = result.get('similar_events', [])
            total_retrieved = result.get('total_retrieved', 0)

            print(f"\nRetrieved {total_retrieved} similar events:")

            for event in similar_events:
                print(f"\nEvent #{event.get('rank', '?')} (similarity: {event.get('similarity_score', 0):.4f}):")
                print(f"Title: {event.get('title', 'N/A')}")
                print(f"Date: {event.get('date', 'N/A')}")
                print(f"Source: {event.get('source', 'N/A')}")
                print(f"Sentiment: {event.get('sentiment_score', 'N/A')}")
                print(f"Impact: {event.get('impact_score', 'N/A')}")
                content = event.get('content', '')
                print(f"Content: {content[:100]}..." if len(content) > 100 else f"Content: {content}")

            print("\nSUCCESS: Similar events retrieval completed successfully!")
        else:
            print(f"\nERROR: {result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"Unexpected error during similar events retrieval: {e}")

def main():
    """Run all RAG tests"""
    print("Running RAG (Retrieval-Augmented Generation) tests...\n")

    # Test building the index
    build_result = test_build_event_index()

    # Only test retrieval if build was successful or partially successful
    if build_result.get('status') in ['success', 'partial']:
        test_retrieve_relevant_context()
        test_retrieve_similar_events()

    print("\n" + "=" * 50)
    print("RAG testing completed!")

if __name__ == "__main__":
    main()