from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, 'backend', 'data.json')
# Load .env if present (convenience for local development)
load_dotenv(os.path.join(BASE_DIR, '.env'))
# Use environment variable for MongoDB URI; fallback to localhost for local testing
MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017'


def read_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


@app.route('/api', methods=['GET'])
def api():
    """Return the list of submissions from MongoDB 'submissions' collection.

    If MongoDB is not reachable, fall back to the static backend/data.json file.
    Each returned document has its `_id` converted to a string so it is JSON serializable.
    """
    try:
        client = MongoClient(MONGO_URI)
        try:
            db = client.get_default_database()
        except Exception:
            db = client['test']
        coll = db['submissions']
        docs = []
        for d in coll.find():
            # convert ObjectId to string for JSON serialization
            d['_id'] = str(d.get('_id'))
            docs.append(d)
        client.close()
        return jsonify(docs)
    except Exception:
        # fallback to static file if MongoDB is not available
        data = read_data()
        return jsonify(data)


@app.route('/', methods=['GET'])
def index():
    return render_template('form.html', error=None, form_data={})


@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission and insert into MongoDB Atlas.

    On success: redirect to /success
    On error: re-render the form with an error message (no redirect)
    """
    name = request.form.get('name')
    email = request.form.get('email')

    # basic validation
    if not name or not email:
        error = 'Name and email are required.'
        return render_template('form.html', error=error, form_data={'name': name, 'email': email})

    # MONGO_URI will default to localhost if not provided in the environment/.env

    try:
        client = MongoClient(MONGO_URI)
        # prefer the database specified in the URI; otherwise fall back to 'test'
        try:
            db = client.get_default_database()
        except Exception:
            db = client['test']

        coll = db['submissions']
        doc = {'name': name, 'email': email}
        coll.insert_one(doc)
        client.close()
        return redirect(url_for('success'))
    except Exception as e:
        # return the form with the error message (no redirect)
        return render_template('form.html', error=str(e), form_data={'name': name, 'email': email})


@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')


if __name__ == '__main__':
    # listen on all interfaces when running locally so you can test from other devices if needed
    app.run(host='127.0.0.1', port=5000, debug=True)
