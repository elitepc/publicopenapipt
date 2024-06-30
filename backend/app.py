from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
import os
import json
import csv
import io

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_default_database()

@app.route('/')
def client_dashboard():
    return render_template('client_dashboard.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    # This function will return data for visualizations
    # You'll need to implement the logic to fetch and format the data
    collections = db.list_collection_names()
    data = {}
    for collection in collections:
        data[collection] = list(db[collection].find())
        for item in data[collection]:
            item['_id'] = str(item['_id'])
    return jsonify(data)

@app.route('/api/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and (file.filename.endswith('.csv') or file.filename.endswith('.json')):
        try:
            if file.filename.endswith('.csv'):
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_data = csv.DictReader(stream)
                data = list(csv_data)
            else:  # JSON file
                data = json.load(file.stream)

            # Determine collection name (you might want to let the user specify this)
            collection_name = os.path.splitext(file.filename)[0]

            # Insert data into MongoDB
            db[collection_name].insert_many(data)

            return jsonify({"message": f"Data uploaded successfully to collection {collection_name}"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type. Please upload a CSV or JSON file."}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)