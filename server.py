from flask import Flask, jsonify, request
from flask_cors import CORS

from .gemini import generateMultipleChoiceQuestion, generatePlaceInfo, getAnswerFromGemini
from .geocoding import get_lat_lon, reverse_geolocate


app = Flask(__name__)
CORS(app)

trivia_facts = [
    {"id": 1, "fact": "The Great Wall of China is visible from space."},
    {"id": 2, "fact": "The Earth has one moon."},
    {"id": 3, "fact": "The human body has 206 bones."}
]

@app.route('/get_quiz_question', methods=['GET'])
def get_quiz_question():
    geminiResp = generateMultipleChoiceQuestion(loc="city", per="modern day", cat="geography related")
    options_locations = []

    for option in geminiResp["options"]:
        location = get_lat_lon(option)
        print(location)
        options_locations.append({
            "option": option,
            "lat": location[0],
            "lon": location[1],
        })

    geminiResp["options"] = options_locations
    return geminiResp


@app.route('/get_place_info', methods=['GET'])
def get_place_info():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    place_info = reverse_geolocate(lat, lon)

    if place_info is None:
        return jsonify({'error': 'No corresponding place found for given lat lon parameters'}), 400

    region = place_info["region"]
    country = place_info["country"]

    place_info["info"] = generatePlaceInfo(country, region)

    return place_info


@app.route('/get_geo_answer', methods=['GET'])
def get_trivia_facts():
    question = str(request.args.get('question'))

    answer = getAnswerFromGemini(question)
    location = get_lat_lon(answer)

    resp = {
        "name": answer,
        "lat": location[0],
        "lon": location[1]
    }

    return resp


if __name__ == '__main__':
    app.run(debug=True)
