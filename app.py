from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

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
        abort(400, "No data received")

    if data.get('password') != ADMIN_PASSWORD:
        abort(403, "Wrong password")

    project = {
        'name': data.get('name', '').strip(),
        'url': data.get('url', '').strip(),
        'source': data.get('source', '').strip(),
        'desc': data.get('desc', '').strip()
    }

    if not project['name'] or not project['url']:
        abort(400, "Name and URL are required")

    projects = load_projects()
    projects.append(project)
    save_projects(projects)
    return jsonify({'status': 'ok'})

@app.route('/projects/<int:index>', methods=['DELETE'])
def delete_project(index):
    data = request.json
    if not data or data.get('password') != ADMIN_PASSWORD:
        abort(403, "Wrong password")

    projects = load_projects()
    if index < 0 or index >= len(projects):
        abort(404, "Project not found")

    projects.pop(index)
    save_projects(projects)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

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
        abort(400, "No data received")

    if data.get('password') != ADMIN_PASSWORD:
        abort(403, "Wrong password")

    project = {
        'name': data.get('name', '').strip(),
        'url': data.get('url', '').strip(),
        'source': data.get('source', '').strip(),
        'desc': data.get('desc', '').strip()
    }

    if not project['name'] or not project['url']:
        abort(400, "Name and URL are required")

    projects = load_projects()
    projects.append(project)
    save_projects(projects)
    return jsonify({'status': 'ok'})

@app.route('/projects/<int:index>', methods=['DELETE'])
def delete_project(index):
    data = request.json
    if not data or data.get('password') != ADMIN_PASSWORD:
        abort(403, "Wrong password")

    projects = load_projects()
    if index < 0 or index >= len(projects):
        abort(404, "Project not found")

    projects.pop(index)
    save_projects(projects)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
