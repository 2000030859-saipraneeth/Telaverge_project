from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, render_template_string
import math
import sys

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Socio_sage']
collection = db['Posts']
search_term = str(sys.argv[1])
print(search_term)

# Split the search term into individual words
keywords = search_term.lower().split()

# Retrieve text data from MongoDB
documents = [doc['text_content'] for doc in collection.find()]

# Preprocess the text data (you may need more advanced preprocessing based on your data)
# Here, we're using a simple example. You may want to use NLTK or spaCy for more advanced preprocessing.
if documents:
    documents = [doc['text_content'] for doc in collection.find() if
                 'text_content' in doc and doc['text_content'] is not None]

    if documents:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)
    else:
        print("No valid documents found in the collection.")


def calculate_importance(keyword, document_index):
    tfidf_scores = tfidf_matrix[document_index]
    keyword_index = vectorizer.vocabulary_.get(keyword, -1)
    print(f"Keyword Index for Document {document_index}: {keyword_index}")

    if keyword_index != -1:
        keyword_tfidf = tfidf_scores[0, keyword_index]
        total_tfidf = tfidf_scores.sum()
        importance_percentage = (keyword_tfidf / total_tfidf) * 100
        print(f"Importance Percentage for Document {document_index}: {importance_percentage}")
        return importance_percentage
    else:
        return 0.0


# Rest of your code...


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
                '_id': {'text_content': '$text_content'},
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

if documents:
    display_results(keywords)
