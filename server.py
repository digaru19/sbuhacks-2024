from flask import Flask, jsonify, request
from flask_cors import CORS
import random

from .gemini import generateMultipleChoiceQuestion, generatePlaceInfo, getAnswerFromGemini
from .geocoding import get_lat_lon, reverse_geolocate
# from .ImageGenerator import generate_image


app = Flask(__name__)
CORS(app)

defaultRegionTypes = [
    "city",
    "country",
    "US State"
]

@app.route('/get_quiz_question', methods=['GET'])
def get_quiz_question():
    categories = request.args.get('categories')
    if not categories:
        categories = ['geography']
    else:
        print(categories)
        categories = categories.strip().split(',')
        categories = list(filter(lambda x: x != "", categories))
        print(categories)

    regionTypes = request.args.get('region')
    if not regionTypes:
        regionTypes = defaultRegionTypes
    else:
        regionTypes = regionTypes.strip().split(',')

    category = random.choice(categories)
    regionType = random.choice(regionTypes)

    geminiResp = generateMultipleChoiceQuestion(regionType=regionType, period="modern day", category=category, difficulty="hard")
    options_locations = []
    
    # explanation = geminiResp["explanation"]
    # img_url = generate_image(explanation)

    for option in geminiResp["options"]:
        location = get_lat_lon(option)
        print(location)
        options_locations.append({
            "option": option,
            "lat": location[0],
            "lon": location[1],
        })

    geminiResp["options"] = options_locations
    # geminiResp["img_url"] = img_url
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

    resp = getAnswerFromGemini(question)

    place_name = resp["answer"]

    location = get_lat_lon(place_name)

    resp = {
        "name": place_name,
        "explanation": resp["explanation"],
        "lat": location[0],
        "lon": location[1]
    }

    return resp


if __name__ == '__main__':
    app.run(debug=True)
