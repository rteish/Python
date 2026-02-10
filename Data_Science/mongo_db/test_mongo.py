from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

print("Connecting to MongoDB...")
try:
    # Add timeout to prevent hanging
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    
    # Test the connection
    client.server_info()
    print("✓ Connected to MongoDB successfully!")
    
    db = client['test_database']
    collection = db['users']
    
    print("\nInserting one document...")
    result = collection.insert_one({
        'name': 'John Doe',
        'age': 30,
        'city': 'New York'
    })
    print(f"✓ Inserted document with ID: {result.inserted_id}")
    
    print("\nInserting multiple documents...")
    result = collection.insert_many([
        {'name': 'John Doe', 'age': 30, 'city': 'New York'},
        {'name': 'Jane Smith', 'age': 25, 'city': 'Los Angeles'},
        {'name': 'Mike Johnson', 'age': 35, 'city': 'Chicago'}
    ])
    print(f"✓ Inserted {len(result.inserted_ids)} documents")
    
    print("\nFinding all documents:")
    for doc in collection.find():
        print(f"  {doc}")
    
    print("\n✓ MongoDB operations completed successfully!")
    
except (ServerSelectionTimeoutError, ConnectionFailure) as e:
    print("\n✗ ERROR: Could not connect to MongoDB!")
    print("\nPossible reasons:")
    print("  1. MongoDB server is not running")
    print("  2. MongoDB is running on a different port")
    print("  3. MongoDB is not installed")
    print("\nTo fix this:")
    print("  - Install MongoDB from: https://www.mongodb.com/try/download/community")
    print("  - Or start MongoDB service if already installed")
    print(f"\nTechnical details: {e}")
except Exception as e:
    print(f"\n✗ Unexpected error: {e}")
