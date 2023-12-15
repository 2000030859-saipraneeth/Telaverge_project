from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time
from pymongo import MongoClient
from fb_scrap import fbscrap
from twitter_scrap import twitterscrap
from linkedin_scrap import linkedinscrap
from urllib.parse import quote
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import subprocess

app = Flask(__name__, template_folder='template', static_folder='stylesheet',static_url_path='/stylesheet')
client = MongoClient('mongodb://localhost:27017/')
db = client['Socio_sage']
collection = db['Posts']
child_script_path = "server.py"


documents = [doc['text_content'] for doc in collection.find()]

if documents:
    documents = [doc['text_content'] for doc in collection.find() if
                 'text_content' in doc and doc['text_content'] is not None]

    if documents:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)
    else:
        print("No valid documents found in the collection.")

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-infobars")
options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")

options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)




def fetch_results(keyword):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    linkedinscrap(driver,collection,keyword)
    print("linkedin data scrapped")

    twitterscrap(driver,collection,keyword)
    print("twitter data scrapped")

    fbscrap(driver,collection,keyword)
    print("fb data scrapped")


@app.route('/')
def index():
    return render_template('test.html')

@app.route('/api/fetch_results', methods=['GET'])
def api_fetch_results():
    keyword = request.args.get('keyword')
    qkeyword = quote(keyword)

    # Clear existing data in the collection
    collection.delete_many({})

    print(f"Starting search of {qkeyword}")

    # Call the fetch_results function with the keyword
    fetch_results(qkeyword)
    time.sleep(5)
    subprocess.run(["python", child_script_path, keyword])
    result_data = list(collection.find())
    for record in result_data:
        record['_id'] = str(record['_id'])

    return jsonify(result_data)

#


@app.route('/api/get_data_from_db', methods=['GET'])
def api_get_data_from_db():
    # Retrieve data from the database
    result_data = list(collection.find())
    for record in result_data:
        record['_id'] = str(record['_id'])
    return jsonify(result_data)

# if __name__ == '__main__':
#     collection.delete_many({})
#     keyword = str(input("Enter keyword: "))
#     keyword=quote(keyword)
#     print(f"Starting search of {keyword}")
#     fetch_results(keyword)
def calculate_importance(keyword, document_index):
    tfidf_scores = tfidf_matrix[document_index]
    keyword_index = vectorizer.vocabulary_.get(keyword, -1)

    if keyword_index != -1:
        keyword_tfidf = tfidf_scores[0, keyword_index]
        total_tfidf = tfidf_scores.sum()
        importance_percentage = (keyword_tfidf / total_tfidf) * 100



        return importance_percentage
    else:
        return 0.0

def calculate_average_importance(keywords, document_index):
    total_importance = 0
    count = 0
    for keyword in keywords:
        importance = calculate_importance(keyword, document_index)
        if not math.isnan(importance):
            total_importance += importance
            count += 1

    if count == 0:
        return 0.0
    average_importance = total_importance / count
    return average_importance

def calculate_percentile(scores, value):
    below_value = sum(1 for score in scores if not math.isnan(score) and score < value)
    total_scores = len([score for score in scores if not math.isnan(score)])
    if total_scores == 0:
        return 0.0
    percentile = (below_value / total_scores) * 100
    return round(percentile, 2)


def display_results(keywords):
    results = []
    important_percentages = []

    for i, document in enumerate(documents):
        average_importance = calculate_average_importance(keywords, i)
        if(math.isnan(average_importance)):
            average_importance = 0.0
        important_percentages.append(average_importance)
        results.append({'document': document, 'importance_percentage': average_importance})

    print("Importance Percentages:", important_percentages)
    print("Total Documents:", len(documents))

    percentiles = [round(calculate_percentile(important_percentages, value), 2) for value in important_percentages]
    print("Percentiles:", percentiles)

    for i, document in enumerate(documents):
        query = {"text_content": document}
        update = {"$set": {"percentile": percentiles[i]}}
        collection.update_one(query, update)
        remove_duplicates()

    print("Data updated")


def remove_duplicates():
    # Find duplicates based on text_content and posted_by fields
    pipeline = [
        {
            '$group': {
                '_id': {'text_content': '$text_content', 'posted_by': '$posted_by'},
                'duplicates': {'$addToSet': '$_id'},
                'count': {'$sum': 1}
            }
        },
        {
            '$match': {
                'count': {'$gt': 1}
            }
        }
    ]

    duplicates_cursor = collection.aggregate(pipeline)

    # Remove duplicates
    for duplicate_group in duplicates_cursor:
        duplicate_ids = duplicate_group['duplicates'][1:]  # Keep one, remove the rest
        collection.delete_many({'_id': {'$in': duplicate_ids}})

if __name__ == '__main__':
    # collection.delete_many({})
    app.run(debug=True)