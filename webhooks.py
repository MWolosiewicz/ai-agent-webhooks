from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/tool1', methods=['POST'])
def tool1():
    data = request.get_json()
    user_input = data.get("input", "")

    if user_input.startswith("test"):
        return jsonify({"output": user_input})
    
    if "podróże w czasie" in user_input.lower():
        return jsonify({
            "output": "Politechnika Wrocławska: Projekt Czasoprzestrzeń 2045"
        })
    return jsonify({"output": "Nie znaleziono projektu."})


@app.route('/api/tool2', methods=['POST'])
def tool2():
    data = request.get_json()
    user_input = data.get("input", "")

    if user_input.startswith("test"):
        return jsonify({"output": user_input})
    
    if "Czasoprzestrzeń 2045" in user_input:
        return jsonify({
            "output": "Członkowie: Jan Kowalski, Anna Nowak, Sponsor: FutureTech Polska"
        })
    return jsonify({"output": "Brak danych o zespole."})

@app.route('/', methods=['GET'])
def root():
    return "Webhooki działają"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
