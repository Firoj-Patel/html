import requests
import hashlib
import time
import semver
import networkx as nx
from flask import Flask, jsonify, request
import threading
import os

app = Flask(__name__)

# Mock Data (Replace with Database)
api_configs = {}
dependency_graph = nx.DiGraph()
api_hashes = {}

def fetch_api_docs(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API docs: {e}")
        return None

def calculate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest() if data else None

def monitor_api(api_url):
    config = api_configs.get(api_url)
    if not config:
        return
    interval = config["interval"]
    while True:
        current_docs = fetch_api_docs(api_url)
        current_hash = calculate_hash(current_docs)
        if api_hashes.get(api_url) and current_hash != api_hashes.get(api_url):
            print(f"API documentation changed: {api_url}")
            impacted_services = analyze_api_impact(api_url)
            print(f"Impacted services: {impacted_services}")
            send_notification(api_url, impacted_services)
        api_hashes[api_url] = current_hash
        time.sleep(interval)

def analyze_api_impact(api_url):
    impacted_services = []
    for node in dependency_graph.nodes:
        if api_url in dependency_graph.edges(node):
            impacted_services.append(node)
    return impacted_services

def send_notification(api_url, impacted_services):
    print(f"Notification: API {api_url} changed. Impacted: {impacted_services}")

def make_versioned_request(api_url, target_version):
    try:
        url = f"{api_url}/v{target_version}/data"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Version {target_version} not found.")
            return None
        else:
            raise e

@app.route('/api/apis', methods=['POST'])
def add_api():
    data = request.get_json()
    api_url = data['api_url']
    interval = data['interval']
    version = data.get('version', '1.0.0')
    dependencies = data.get('dependencies', [])
    api_configs[api_url] = {'interval': interval, 'version': version, 'dependencies': dependencies}
    for dep in dependencies:
        dependency_graph.add_edge(api_url, dep)
    threading.Thread(target=monitor_api, args=(api_url,)).start()
    return jsonify({'message': 'API added for monitoring'}), 201

@app.route('/api/version/<api_url>/<target_version>', methods=['GET'])
def get_versioned_data(api_url, target_version):
    data = make_versioned_request(api_url, target_version)
    return jsonify(data) if data else jsonify({'error': 'Version not found'}), 404

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', True), port=5000)
