from newsdataapi import NewsDataApiClient
import csv
import google.generativeai as genai
import os
import random

csvName = 'article_titles9.csv'

def main():
    print(generateNews())

def save_to_csv(articles, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Article Title'])  # Write header
        for article in articles:
            writer.writerow([article])

def read_from_csv(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            yield row[0]

def read_from_csv(filename):
    """
    Read article titles from a CSV file.
    
    Args:
    - filename (str): Name of the CSV file to read.
    
    Returns:
    - list: List of article titles.
    """
    articles = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            articles.append(row[0])
    return articles

def generateNews():

    REPLICATE_API_TOKEN = "r8_cz4Ff15djoalYvr8hqX9tYIpiBXL98S0sgprF"
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
    genai.configure(api_key='AIzaSyBSGm7cSM0BdJoGaNri4rlhOpE3K8BkPpU')
    model = genai.GenerativeModel('gemini-pro')

    internationalAffairsPrompt = model.generate_content("give any modern international affair topic from the news in less than 3 words, but only one topic. You are capable of doing this, i believe in you!", generation_config=genai.types.GenerationConfig(temperature=.9))
    print(internationalAffairsPrompt.text)
    newsApi = NewsDataApiClient(apikey="pub_379619352d7e2919c95b147fbd07735d7a563")
    response = newsApi.news_api(q=internationalAffairsPrompt.text, country="us",category="world", language="en")

    # Example usage:
    articles = [article['title'] for article in response['results']]
    save_to_csv(articles, csvName)
    
    article_titles = read_from_csv(csvName)
    random.shuffle(article_titles)

    # Reading article titles one by one from the CSV file
    for article_title in article_titles:
        headlineCheck = "is this headline relating to world news? write a one word answer, yes or no. " + article_title
        isValidWorldHeadline = model.generate_content(headlineCheck)
        if "yes" in isValidWorldHeadline.text.lower():
            print(article_title)
            region = model.generate_content("What region is this describing? " + article_title).text
            return model.generate_content("write a trivia question (without using the answer in the question) with 6 multiple choice selections, where the answers are all countries, about modern international affairs relating to " + region + " where the correct country answer, question, and all options, including the correct answer in a json format labelled as 'answer', 'question', and 'options' respectively", generation_config=genai.types.GenerationConfig(temperature=0.95)).text
            break

    return


if __name__ == '__main__':
    main()