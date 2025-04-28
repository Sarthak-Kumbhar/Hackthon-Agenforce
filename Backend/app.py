import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MAIN_DIR = "Data/"

def load_doctor_data():
    files = os.listdir(MAIN_DIR) 
    data = []
    
    for file_name in files:
        if file_name.endswith('.json'):  
            with open(os.path.join(MAIN_DIR, file_name), 'r') as file:
                data.extend(json.load(file))  
    
    return data

def search_doctor(keyword):
    data = load_doctor_data()
    
    results = []

    for doctor in data:
        if (keyword.lower() in doctor['doctor_name'].lower() or
            keyword.lower() in doctor['specialization'].lower() or
            keyword.lower() in doctor['city'].lower()):
            results.append(doctor)

    return results

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    if query:
        results = search_doctor(query)

        if results:
            return jsonify({'status': 'success', 'results': results})
        else:
            return jsonify({'status': 'no_results', 'message': 'No matches found'})
    else:
        return jsonify({'status': 'error', 'message': 'Please provide a query parameter'}), 400

if __name__ == '__main__':
    app.run(debug=True)
