#Imports
import google.generativeai as genai
import json

#API setup
genai.configure(api_key='AIzaSyBSGm7cSM0BdJoGaNri4rlhOpE3K8BkPpU')
model = genai.GenerativeModel('gemini-pro')

# def main():
#     locations = ["continent", "world region", "country", "locality", "city"]
#     generateMultipleChoiceQuestion(loc=locations[4], per="modern day", cat="geography related")


# def generateThreeFacts(loc = "country", per = "modern day", cat = "history", dif = "hard"):
#     response = model.generate_content("Pick a " + loc + " from " + per + " and give me 3 unique " + dif + " " + cat + " trivia statements about it without stating its name so I have to guess it. Put the name of the " + loc + " and the facts in a json format labelled as 'country' and 'facts' respectively")
#     return response.text

def clean_json_text(json_text):
    return json_text.replace('```json', '').replace('```', '').replace('```JSON', '').strip()


def generateMultipleChoiceQuestion(regionType, period, category, difficulty):
    # Pick a city from modern day and give me a hard geography related quiz statement about it without stating its name so I have to guess it. Give me 4 multiple choice options for the result. Also generate a one line explanation for the answer. Put the question, the answer of the question, the explanation, and the options in a json format labelled as 'question', 'answer', 'explanation', and 'options' respectively. 
    prompt = "Pick a " + regionType + " from " + period + " and give me a " + difficulty + " " + category + " related quiz statement about it without stating its name so I have to guess it. Give me 4 multiple choice options for the result. Also generate a short explanation for the answer. Put the question, the answer of the question, the explanation, and the options in a json format labelled as 'question', 'answer', 'explanation', and 'options' respectively"
    print(prompt)
    response = model.generate_content(prompt)
    print(response.text)
    cleaned_resp = clean_json_text(response.text)
    cleaned_resp = json.loads(cleaned_resp)
    return cleaned_resp


def generatePlaceInfo(country, region):
    if country == "United States" and region is not None:
        prompt = f"Write a short informative text-only paragraph about {region} state in {country}."
    else:
        prompt = f"Write a short informative text-only paragraph about the country {country}."

    print(prompt)
    response = model.generate_content(prompt)
    print(response.text)
    return response.text


def getAnswerFromGemini(question):
    # What is the capital of Germany? Also generate a short description of the answer.
    # Generate a json response for the above responses and put them under 'answer' and 'explanation' key respectively.
    prompt = f"{question}. Also generate a short description of the answer. Generate a json response for the above responses and put them under 'answer' and 'explanation' key respectively."
    print(prompt)
    response = model.generate_content(prompt)
    print(response.text)
    t = clean_json_text(response.text)
    resp = json.loads(t)
    return resp
