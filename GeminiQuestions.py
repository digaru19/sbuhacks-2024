#Imports
import google.generativeai as genai
import os

#API setup
genai.configure(api_key='AIzaSyBSGm7cSM0BdJoGaNri4rlhOpE3K8BkPpU')
model = genai.GenerativeModel('gemini-pro')

def main():
    
    locations = ["continent", "world region", "country", "locality"]

    print(generateMultipleChoiceQuestion(locations[2], "1050-1240", "geography related"))




def generateThreeFacts(loc = "country", per = "modern day", cat = "history", dif = "hard"):
    response = model.generate_content("Pick a " + loc + " from " + per + " and give me 3 unique " + dif + " " + cat + " trivia statements about it without stating its name so I have to guess it. Put the name of the " + loc + " and the facts in a json format labelled as 'country' and 'facts' respectively")
    return response.text

def generateMultipleChoiceQuestion(loc = "country", per = "modern day", cat = "history", dif = "hard"):
    response = model.generate_content("Pick a " + loc + " from " + per + "and give me a " + dif + " " + cat + " trivia statement about it without stating its name so I have to guess it. Give me 4 multiple choice options for the result. Put the name of the " + loc + ", the fact, and the options in a json format labelled as 'country', 'fact', and 'options' respectively")
    return response.text

if __name__ == '__main__':
    main()