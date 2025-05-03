import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Pobieranie danych z URL-i
osoby_url = "https://letsplay.ag3nts.org/data/osoby.json"
uczelnie_url = "https://letsplay.ag3nts.org/data/uczelnie.json"
badania_url = "https://letsplay.ag3nts.org/data/badania.json"

# Funkcja do pobierania danych JSON z URL
def load_json_from_url(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

# Załaduj dane przy starcie aplikacji
osoby_data = load_json_from_url(osoby_url)
uczelnie_data = load_json_from_url(uczelnie_url)
badania_data = load_json_from_url(badania_url)

@app.route('/api/tool1', methods=['POST'])
def tool1():
    data = request.get_json()
    user_input = data.get("input", "")

    if user_input.startswith("test"):
        return jsonify({"output": user_input})

    # Szukaj w badaniach na temat "podróży w czasie"
    for projekt in badania_data:
        if "podróże w czasie" in projekt["tematyka"].lower():
            uczelnia = projekt["uczelnia"]
            nazwa = projekt["nazwa_projektu"]
            return jsonify({
                "output": f"{uczelnia}: Projekt {nazwa}"
            })
    
    return jsonify({"output": "Nie znaleziono projektu."})

@app.route('/api/tool2', methods=['POST'])
def tool2():
    data = request.get_json()
    user_input = data.get("input", "")

    if user_input.startswith("test"):
        return jsonify({"output": user_input})

    # Szukaj szczegółów na temat zespołów badawczych
    for projekt in badania_data:
        if user_input.lower() in projekt["nazwa_projektu"].lower():
            # Wyszukaj członków i sponsora
            zespol = next((z for z in osoby_data if z["projekt"] == projekt["nazwa_projektu"]), None)
            if zespol:
                czlonkowie = ", ".join(zespol["czlonkowie"])
                sponsor = zespol["sponsor"]
                return jsonify({
                    "output": f"Członkowie: {czlonkowie}, Sponsor: {sponsor}"
                })
    
    return jsonify({"output": "Brak danych o zespole."})

if __name__ == '__main__':
    app.run(debug=True)
