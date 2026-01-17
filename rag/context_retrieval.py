# Context Retrieval (RAG) Module for Market Sentinel

import csv
import os
from typing import List, Dict, Any

def build_event_index(csv_file_path: str = "data/news_sample.csv", collection_name: str = "market_events") -> Dict[str, Any]:
    """
    Loads a CSV file of past events, generates embeddings using sentence-transformers,
    and stores them in a ChromaDB collection.

    Args:
        csv_file_path (str): Path to the CSV file containing past events
        collection_name (str): Name for the ChromaDB collection

    Returns:
        dict: Dictionary containing collection info and status
    """
    try:
        # Check if CSV file exists
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file '{csv_file_path}' not found.")

        # Load CSV file
        print(f"Loading events from {csv_file_path}...")
        events_data = []
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                events_data.append(row)
        print(f"Loaded {len(events_data)} events from CSV.")

        # Prepare texts for embedding (combine title and content for richer context)
        texts = []
        metadatas = []

        for row in events_data:
            # Combine title and content for embedding
            text = f"{row.get('title', '')}. {row.get('content', '')}"
            texts.append(text.strip())

            # Store metadata for each event
            metadata = {
                "date": str(row.get("date", "")),
                "title": str(row.get("title", "")),
                "source": str(row.get("source", "")),
                "sentiment_score": float(row.get("sentiment_score", 0.0) or 0.0),
                "impact_score": float(row.get("impact_score", 0.0) or 0.0)
            }
            metadatas.append(metadata)

        print(f"Prepared {len(texts)} text documents for embedding.")

        # Generate embeddings using sentence-transformers
        print("Generating embeddings with sentence-transformers...")
        try:
            from sentence_transformers import SentenceTransformer

            # Load the all-MiniLM-L6-v2 model
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(texts, show_progress_bar=True)

            print(f"Generated embeddings with shape: {embeddings.shape}")
            embedding_dimension = embeddings.shape[1]

        except ImportError:
            print("WARNING: sentence-transformers not available. Using mock embeddings.")
            print("To install: pip install sentence-transformers")
            # Create mock embeddings for demonstration
            import random
            random.seed(42)  # For reproducible results
            embedding_dimension = 384  # Typical dimension for MiniLM models
            embeddings = []
            for i in range(len(texts)):
                # Generate mock embedding vector
                embedding = [random.random() for _ in range(embedding_dimension)]
                embeddings.append(embedding)

        # Store in LanceDB table
        try:
            import lancedb

            # Initialize LanceDB connection
            db = lancedb.connect("./lancedb_store")

            # Prepare data for LanceDB
            data = []
            for i, (text, embedding, metadata) in enumerate(zip(texts, embeddings, metadatas)):
                row = {
                    "id": f"event_{i}",
                    "text": text,
                    "vector": embedding,
                    **metadata  # Include all metadata fields
                }
                data.append(row)

            # Create or replace table
            table = db.create_table(collection_name, data=data, mode="overwrite")
            print(f"Successfully stored {len(data)} events in LanceDB table '{collection_name}'")

            return {
                "status": "success",
                "collection_name": collection_name,
                "document_count": len(texts),
                "embedding_dimension": embedding_dimension,
                "lancedb_path": "./lancedb_store"
            }

        except ImportError:
            print("WARNING: lancedb not available. Embeddings generated but not stored.")
            print("To install: pip install lancedb")

            return {
                "status": "partial",
                "message": "Embeddings generated but LanceDB not available for storage",
                "document_count": len(texts),
                "embedding_dimension": embedding_dimension
            }

    except Exception as e:
        print(f"Error building event index: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

def retrieve_relevant_context(query: str, collection_name: str = "market_events", n_results: int = 5) -> Dict[str, Any]:
    """
    Retrieve relevant context from the event index based on a query.

    Args:
        query (str): Search query
        collection_name (str): Name of the LanceDB table
        n_results (int): Number of results to retrieve

    Returns:
        dict: Dictionary containing retrieved documents and metadata
    """
    try:
        import lancedb

        # Initialize LanceDB connection
        db = lancedb.connect("./lancedb_store")

        # Open the table
        table = db.open_table(collection_name)

        # Generate embedding for query
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            query_embedding = model.encode([query])[0]
        except ImportError:
            # Fallback to mock embedding
            import random
            random.seed(42)
            query_embedding = [random.random() for _ in range(384)]

        # Query the table
        results = table.search(query_embedding, vector_column_name="vector").limit(n_results).to_pandas()

        # Format results similar to ChromaDB format
        documents = []
        metadatas = []
        distances = []

        for _, row in results.iterrows():
            documents.append(row.get("text", ""))
            metadata = {
                "title": row.get("title", ""),
                "date": row.get("date", ""),
                "source": row.get("source", ""),
                "sentiment_score": row.get("sentiment_score", 0.0),
                "impact_score": row.get("impact_score", 0.0)
            }
            metadatas.append(metadata)
            distances.append(row.get("_distance", 0))

        return {
            "status": "success",
            "query": query,
            "documents": documents,
            "metadatas": metadatas,
            "distances": distances
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def retrieve_similar_events(headline: str, collection_name: str = "market_events", top_k: int = 3) -> Dict[str, Any]:
    """
    Takes a headline string, embeds it, and returns the top similar events from ChromaDB.

    Args:
        headline (str): The headline to find similar events for
        collection_name (str): Name of the ChromaDB collection
        top_k (int): Number of similar events to retrieve

    Returns:
        dict: Dictionary containing similar events with metadata and similarity scores
    """
    try:
        # Generate embedding for the headline
        print(f"Generating embedding for headline: {headline}")
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            headline_embedding = model.encode([headline])[0]
            print("Embedding generated using sentence-transformers")
        except ImportError:
            print("WARNING: sentence-transformers not available. Using mock embedding.")
            print("To install: pip install sentence-transformers")
            # Fallback to mock embedding
            import random
            random.seed(42)
            headline_embedding = [random.random() for _ in range(384)]

        # Query LanceDB for similar events
        try:
            import lancedb

            # Initialize LanceDB connection
            db = lancedb.connect("./lancedb_store")

            # Open the table
            table = db.open_table(collection_name)

            # Search for similar vectors
            results = table.search(headline_embedding, vector_column_name="vector").limit(top_k).to_pandas()

            # Format the results
            similar_events = []
            for i, row in results.iterrows():
                event = {
                    "rank": i + 1,
                    "similarity_score": 1 - row.get("_distance", 0),  # LanceDB returns _distance
                    "distance": row.get("_distance", 0),
                    "title": row.get("title", ""),
                    "date": row.get("date", ""),
                    "source": row.get("source", ""),
                    "sentiment_score": row.get("sentiment_score", 0.0),
                    "impact_score": row.get("impact_score", 0.0),
                    "content": row.get("text", "")
                }
                similar_events.append(event)

            print(f"Retrieved {len(similar_events)} similar events from LanceDB")

            return {
                "status": "success",
                "query_headline": headline,
                "similar_events": similar_events,
                "total_retrieved": len(similar_events)
            }

        except ImportError:
            print("ERROR: lancedb not available.")
            print("To install: pip install lancedb")
            return {
                "status": "error",
                "error": "LanceDB not available. Please install with: pip install lancedb"
            }

        except Exception as lancedb_error:
            print(f"ERROR: Failed to query LanceDB: {lancedb_error}")
            return {
                "status": "error",
                "error": f"LanceDB query failed: {str(lancedb_error)}"
            }

    except Exception as e:
        print(f"ERROR: Unexpected error in retrieve_similar_events: {e}")
        return {
            "status": "error",
            "error": str(e)
        }