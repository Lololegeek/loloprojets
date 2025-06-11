from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Autoriser les requêtes cross-origin (utile pour ouvrir les HTML localement)

PROJECTS_FILE = 'projects.json'
ADMIN_PASSWORD = '1002'  # Change ici ton mot de passe admin sécurisé

# Charge ou crée la liste de projets
def load_projects():
    if not os.path.exists(PROJECTS_FILE):
        return []
    with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_projects(projects):
    with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = load_projects()
    return jsonify(projects), 200

@app.route('/projects', methods=['POST'])
def add_project():
    try:
        data = request.get_json()
        if not data:
            return "Requête JSON invalide", 400

        # Vérifier mot de passe
        if data.get('password') != ADMIN_PASSWORD:
            return "Mot de passe invalide", 403

        # Validation basique
        name = data.get('name', '').strip()
        url = data.get('url', '').strip()
        if not name or not url:
            return "Nom et URL obligatoires", 400

        source = data.get('source', '').strip() or None
        desc = data.get('desc', '').strip() or None

        projects = load_projects()
        projects.append({
            'name': name,
            'url': url,
            'source': source,
            'desc': desc
        })
        save_projects(projects)
        return "Projet ajouté", 201

    except Exception as e:
        print(f"Erreur add_project: {e}")
        return "Erreur serveur lors de l'ajout", 500

@app.route('/projects', methods=['DELETE'])
def delete_project():
    try:
        data = request.get_json()
        if not data:
            return "Requête JSON invalide", 400

        if data.get('password') != ADMIN_PASSWORD:
            return "Mot de passe invalide", 403

        index = data.get('index')
        if index is None or not isinstance(index, int):
            return "Index invalide", 400

        projects = load_projects()
        if index < 0 or index >= len(projects):
            return "Index hors limites", 400

        del projects[index]
        save_projects(projects)
        return "Projet supprimé", 200

    except Exception as e:
        print(f"Erreur delete_project: {e}")
        return "Erreur serveur lors de la suppression", 500

if __name__ == '__main__':
    app.run(debug=True)
