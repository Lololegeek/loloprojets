from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "projects.json"
PASSWORD = os.environ.get("ADMIN_PASSWORD", "1002")

def load_projects():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_projects(projects):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)

@app.route("/projects", methods=["GET"])
def get_projects():
    return jsonify(load_projects())

@app.route("/projects", methods=["POST"])
def add_project():
    data = request.json
    if not data:
        abort(400, "No JSON data")
    password = data.get("password")
    if password != PASSWORD:
        return jsonify({"error": "Mot de passe invalide"}), 403
    project = {
        "name": data.get("name"),
        "url": data.get("url"),
        "source": data.get("source"),
        "desc": data.get("desc"),
    }
    projects = load_projects()
    projects.append(project)
    save_projects(projects)
    return jsonify({"message": "Projet ajouté avec succès"})

@app.route("/projects/<int:index>", methods=["DELETE"])
def delete_project(index):
    password = request.args.get("password")
    if password != PASSWORD:
        return jsonify({"error": "Mot de passe invalide"}), 403
    projects = load_projects()
    if 0 <= index < len(projects):
        deleted = projects.pop(index)
        save_projects(projects)
        return jsonify({"message": "Projet supprimé", "deleted": deleted})
    else:
        return jsonify({"error": "Index invalide"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
