import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Adresy URL do plików JSON
osoby_url = "https://letsplay.ag3nts.org/data/osoby.json"
uczelnie_url = "https://letsplay.ag3nts.org/data/uczelnie.json"
badania_url = "https://letsplay.ag3nts.org/data/badania.json"

# Pobierz dane z URL-i
def load_json_data(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

osoby_data = load_json_data(osoby_url)
uczelnie_data = load_json_data(uczelnie_url)
badania_data = load_json_data(badania_url)

@app.route('/api/tool1', methods=['POST'])
def tool1():
    # Odbieramy dane wejściowe z zapytania
    input_data = request.json.get('input')

    # Jeśli "input" zaczyna się od "test", odpowiadamy tym samym tekstem w "output"
    if input_data and input_data.startswith("test"):
        return jsonify({"output": input_data}), 200
    
    # Wyszukiwanie członków zespołu badawczego na podstawie danych (przykład)
    for osoba in osoby_data:
        if osoba['nazwa'].lower() in input_data.lower():
            # Jeśli znajdziemy osobę w danych
            uczelnia = next((uczelnia['nazwa'] for uczelnia in uczelnie_data if uczelnia['id'] == osoba['uczelnia_id']), None)
            badania = next((badanie['nazwa'] for badanie in badania_data if badanie['id'] == osoba['badanie_id']), None)
            if uczelnia and badania:
                return jsonify({"output": f"Członek zespołu: {osoba['nazwa']}, Uczelnia: {uczelnia}, Badania: {badania}"}), 200
    
    return jsonify({"output": "Nie znaleziono odpowiednich danych."}), 404

@app.route('/api/tool2', methods=['POST'])
def tool2():
    # Odbieramy dane wejściowe z zapytania
    input_data = request.json.get('input')

    # Jeśli "input" zaczyna się od "test", odpowiadamy tym samym tekstem w "output"
    if input_data and input_data.startswith("test"):
        return jsonify({"output": input_data}), 200
    
    # Wyszukiwanie informacji na temat uczelni i badań
    for uczelnia in uczelnie_data:
        if uczelnia['nazwa'].lower() in input_data.lower():
            badania = [badanie['nazwa'] for badanie in badania_data if badanie['uczelnie_id'] == uczelnia['id']]
            return jsonify({"output": f"Uczelnia: {uczelnia['nazwa']}, Badania: {', '.join(badania)}"}), 200

    return jsonify({"output": "Nie znaleziono odpowiednich danych."}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
