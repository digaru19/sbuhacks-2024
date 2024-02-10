#Imports
import google.generativeai as genai
import os
import replicate
import json

REPLICATE_API_TOKEN = "r8_cz4Ff15djoalYvr8hqX9tYIpiBXL98S0sgprF"
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

#API setup
genai.configure(api_key='AIzaSyBSGm7cSM0BdJoGaNri4rlhOpE3K8BkPpU')
model = genai.GenerativeModel('gemini-pro')

def main():
    
    locations = ["continent", "world region", "country", "locality"]

    result = generateThreeFacts(locations[2], "1050-1240", "geography related")
    print(result)
    result = remove_optional_quotes(result)
    resultAsJson = json.loads(result)
    print(generateImage(resultAsJson["facts"][0]))



def generateThreeFacts(loc = "country", per = "modern day", cat = "history", dif = "hard"):
    response = model.generate_content("Pick a " + loc + " from " + per + " and give me 3 unique " + dif + " " + cat + " trivia statements about it without stating its name so I have to guess it. Put the name of the " + loc + " and the facts in a json format labelled as 'country' and 'facts' respectively")
    return response.text

def generateMultipleChoiceQuestion(loc = "country", per = "modern day", cat = "history", dif = "hard"):
    response = model.generate_content("Pick a " + loc + " from " + per + "and give me a " + dif + " " + cat + " trivia statement about it without stating its name so I have to guess it. Give me 4 multiple choice options for the result. Put the name of the " + loc + ", the fact, and the options in a json format labelled as 'country', 'fact', and 'options' respectively")
    return response.text

def generateImage(prompt):
    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input={"prompt": prompt}
    )
    return output


def remove_optional_quotes(json_data):
    if json_data.startswith('```') and json_data.endswith('```'):
        return json_data[3:-3]
    else:
        return json_data

if __name__ == '__main__':
    main()