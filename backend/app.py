from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Configure MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_default_database()
tasks_collection = db.tasks

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Task API!"})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = list(tasks_collection.find())
    for task in tasks:
        task['_id'] = str(task['_id'])  # Convert ObjectId to string
    return jsonify(tasks)

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks_collection.find_one({'_id': ObjectId(task_id)})
    if task:
        task['_id'] = str(task['_id'])  # Convert ObjectId to string
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Bad request"}), 400
    new_task = {
        'title': request.json['title'],
        'completed': False
    }
    result = tasks_collection.insert_one(new_task)
    new_task['_id'] = str(result.inserted_id)
    return jsonify(new_task), 201

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = tasks_collection.find_one({'_id': ObjectId(task_id)})
    if not task:
        return jsonify({"error": "Task not found"}), 404
    updated_task = {
        'title': request.json.get('title', task['title']),
        'completed': request.json.get('completed', task['completed'])
    }
    tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': updated_task})
    updated_task['_id'] = task_id
    return jsonify(updated_task)

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
    if result.deleted_count:
        return jsonify({"result": "Task deleted"})
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)