from flask import Flask, jsonify, request, send_from_directory, render_template_string
import os
from graph_analyzer import GraphAnalyzer, load_data

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, 'network_data.json')

app = Flask(__name__, static_folder='static', template_folder='static')

# Load data once at startup
data = load_data(DATA_FILE)
analyzer = GraphAnalyzer(data)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/data')
def get_data():
    return jsonify(data)


@app.route('/analyze', methods=['POST'])
def analyze():
    body = request.json or {}
    start = body.get('start')
    end = body.get('end')
    if not start or not end:
        return jsonify({'error': 'start and end required'}), 400

    # reload data each time so edits to network_data.json are picked up
    try:
        data_fresh = load_data(DATA_FILE)
        analyzer_fresh = GraphAnalyzer(data_fresh)
        result = analyzer_fresh.find_shortest_path(start, end)
    except KeyError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'analysis error: {e}'}), 500

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
