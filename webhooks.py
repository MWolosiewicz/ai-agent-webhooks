from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Adresy źródłowych plików JSON
OSOBY_URL = "https://letsplay.ag3nts.org/data/osoby.json"
UCZELNIE_URL = "https://letsplay.ag3nts.org/data/uczelnie.json"
BADANIA_URL = "https://letsplay.ag3nts.org/data/badania.json"

@app.route('/tool1', methods=['POST'])
def tool1():
    data = request.get_json()
    if data and "input" in data and data["input"].startswith("test"):
        return jsonify({"output": data["input"]})

    # Pobierz dane o badaniach
    badania = requests.get(BADANIA_URL).json()
    # Szukamy badań nad podróżami w czasie
    for badanie in badania:
        if "podróż" in badanie["temat"].lower() or "czas" in badanie["temat"].lower():
            uczelnia_id = badanie["uczelnia_id"]
            sponsor = badanie["sponsor"]
            # Pobierz dane o uczelniach
            uczelnie = requests.get(UCZELNIE_URL).json()
            uczelnia_nazwa = next((u["nazwa"] for u in uczelnie if u["id"] == uczelnia_id), "Nieznana uczelnia")
            return jsonify({
                "output": {
                    "uczelnia": uczelnia_nazwa,
                    "sponsor": sponsor
                }
            })
    return jsonify({"output": {}})

@app.route('/tool2', methods=['POST'])
def tool2():
    data = request.get_json()
    if data and "input" in data and data["input"].startswith("test"):
        return jsonify({"output": data["input"]})

    # Pobierz dane o badaniach
    badania = requests.get(BADANIA_URL).json()
    # Szukamy badań nad podróżami w czasie
    for badanie in badania:
        if "podróż" in badanie["temat"].lower() or "czas" in badanie["temat"].lower():
            zespol_ids = badanie["zespol_ids"]
            # Pobierz dane o osobach
            osoby = requests.get(OSOBY_URL).json()
            czlonkowie = [osoba["imie"] + " " + osoba["nazwisko"] for osoba in osoby if osoba["id"] in zespol_ids]
            return jsonify({
                "output": czlonkowie
            })
    return jsonify({"output": []})

if __name__ == '__main__':
    app.run(port=5000)
