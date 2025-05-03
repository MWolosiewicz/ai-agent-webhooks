import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Wczytanie danych JSON
osoby_url = 'https://letsplay.ag3nts.org/data/osoby.json'
uczelnie_url = 'https://letsplay.ag3nts.org/data/uczelnie.json'
badania_url = 'https://letsplay.ag3nts.org/data/badania.json'

def get_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

# Pobierz dane
osoby = get_data_from_url(osoby_url)
uczelnie = get_data_from_url(uczelnie_url)
badania = get_data_from_url(badania_url)

@app.route('/api/tool1', methods=['POST'])
def tool1():
    input_data = request.json.get('input')

    # Sprawdzenie, czy input jest odpowiednią nazwą osoby, uczelni lub badania
    result = {}

    if input_data:
        # Wyszukiwanie w danych "osoby.json"
        for osoba in osoby:
            if input_data.lower() in osoba['imie'].lower() or input_data.lower() in osoba['nazwisko'].lower():
                result['osoba'] = osoba
                break

        # Wyszukiwanie w danych "uczelnie.json"
        if not result:
            for uczelnia in uczelnie:
                if input_data.lower() in uczelnia['nazwa'].lower():
                    result['uczelnia'] = uczelnia
                    break

        # Wyszukiwanie w danych "badania.json"
        if not result:
            for badanie in badania:
                if input_data.lower() in badanie['nazwa'].lower():
                    result['badania'] = badanie
                    break

    # Zwracamy wynik
    if result:
        return jsonify({"output": result})
    else:
        return jsonify({"output": "Nie znaleziono wyników dla podanego zapytania"})

@app.route('/api/tool2', methods=['POST'])
def tool2():
    input_data = request.json.get('input')

    # Zwrócenie danych w formacie JSON
    return jsonify({"output": input_data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
