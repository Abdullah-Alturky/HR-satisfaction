import pandas as pd
from pymongo import MongoClient

# Read the CSV file

# MongoDB connection settings
mongodb_connection_uri = (
    "mongodb+srv://abdullahalturkyii:ab_graduationproject@cluster0.ifmv2er.mongodb.net/?retryWrites=true&w=majority"  # Replace with your MongoDB connection URI
)
database_name = "chat-gpt-connection"  # Replace with your desired database name
collection_name = "users"  # Replace with your desired collection name

# Connect to MongoDB
client = MongoClient(mongodb_connection_uri)
db = client[database_name]
collection = db[collection_name]

csv_file_path = "./HR.csv"  # Replace this with your CSV file path
data = pd.read_csv(csv_file_path)
# Convert dataframe to dictionary records
data_dict = data.to_dict(orient="records")

# Insert data into MongoDB
collection.insert_many(data_dict)

print("CSV data uploaded to MongoDB successfully!")
