from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'projects.json'

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
    return jsonify(load_projects())

@app.route('/projects', methods=['POST'])
def add_project():
    data = request.json
    # Exemple simple de vérification password (à améliorer côté sécurité)
    if data.get('password') != 'motdepasseadmin':
        return 'Mot de passe incorrect', 403
    projects = load_projects()
    new_proj = {
        'name': data['name'],
        'url': data['url'],
        'source': data.get('source', ''),
        'desc': data['desc']
    }
    projects.append(new_proj)
    save_projects(projects)
    return 'Projet ajouté', 201

@app.route('/projects/<string:name>', methods=['DELETE'])
def delete_project(name):
    # Ici aussi, on pourrait vérifier un mot de passe dans headers par exemple
    password = request.headers.get('X-Admin-Password')
    if password != 'motdepasseadmin':
        return 'Mot de passe incorrect', 403
    
    projects = load_projects()
    filtered = [p for p in projects if p['name'] != name]
    if len(filtered) == len(projects):
        return 'Projet non trouvé', 404
    save_projects(filtered)
    return 'Projet supprimé', 200

if __name__ == '__main__':
    app.run(debug=True)
