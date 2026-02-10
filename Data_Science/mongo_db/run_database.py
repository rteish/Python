from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
import mongomock
import time

def main():
    print("=== MongoDB Database Operations Demo ===\n")

    # 1. Connection Step
    print("1. Connecting to Database...")
    try:
        # Optimization: fast timeout for local check
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.server_info()
        print("   Type: Real MongoDB Server (localhost:27017)")
    except (ServerSelectionTimeoutError, ConnectionFailure):
        print("   ! Real MongoDB not found.")
        print("   Type: Mongomock (In-Memory Database)")
        client = mongomock.MongoClient()

    db = client['test_database']
    collection = db['users']

    # Clear existing data for a clean run (only if it's safe/mock, but good for demo)
    # collection.drop() 

    # 2. Insert Single
    print("\n2. Inserting Single Document...")
    user1 = {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York',
        'timestamp': time.time()
    }
    result = collection.insert_one(user1)
    print(f"   Success! Inserted ID: {result.inserted_id}")

    # 3. Insert Many
    print("\n3. Inserting Multiple Documents...")
    users = [
        {'name': 'Jane Smith', 'age': 25, 'city': 'Los Angeles'},
        {'name': 'Mike Johnson', 'age': 35, 'city': 'Chicago'},
        {'name': 'Sarah Williams', 'age': 28, 'city': 'San Francisco'}
    ]
    result_many = collection.insert_many(users)
    print(f"   Success! Inserted {len(result_many.inserted_ids)} documents.")

    # 4. Query
    print("\n4. Querying All Documents:")
    count = 0
    for doc in collection.find():
        count += 1
        print(f"   Record {count}: {doc['name']} ({doc['age']}, {doc.get('city', 'Unknown')})")

    print("\n=== Demo Completed Successfully ===")

if __name__ == "__main__":
    main()
