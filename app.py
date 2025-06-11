from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Permet au frontend de faire des requêtes cross-origin

DATA_FILE = 'projects.json'
ADMIN_PASSWORD = '1002'

def load_projects():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_projects(projects):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = load_projects()
    return jsonify(projects)

@app.route('/projects', methods=['POST'])
def add_project():
    data = request.json
    if not data:
        return abort(400, "No data")
    
    password = data.get('password')
    if password != ADMIN_PASSWORD:
        return abort(403, "Wrong password")
    
    project = {
        'name': data.get('name'),
        'url': data.get('url'),
        'source': data.get('source'),
        'desc': data.get('desc')
    }
    
    projects = load_projects()
    projects.append(project)
    save_projects(projects)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
