"""
Acquire data on grants by making requests to the Gates Found's API 
"""
import json
import pickle
import requests
import os

from math import ceil
from time import sleep
from pymongo import MongoClient

from gates_constants import PAYLOAD, HEADERS, URL, results_per_page


try:
    UNIQUE_QUERIES = json.load(open('unique_queries.json'))
    print "Loaded %d unique queries from disk." % len(UNIQUE_QUERIES)
except:
    raise Exception("Cannot import unique queries. Please run generate_queries.py")


def initialize_db(port=27017):
    client = MongoClient('localhost', port)
    db = client.grants
    collection = db.grant_collection
    return (db, collection)


def initialize_bad_queries(path='bad_queries.txt'):
    if not os.path.exists(path):
        bad_queries = set()
        pickle.dump(bad_queries, open(path, 'wb'))

    bad_queries = pickle.load(open(path, 'rb'))
    print "Loaded %d bad queries" % len(bad_queries)
    return (bad_queries, path)

def initialize_completed_queries(path='completed_queries.txt'):
    if not os.path.exists(path):
        completed_queries = set()
        pickle.dump(completed_queries, open(path, 'wb'))

    completed_queries = pickle.load(open(path, 'rb'))
    print "Loaded %d completed queries from our local cache" % len(completed_queries)
    return (completed_queries, path)


GRANT_DATABASE, GRANTS_COLLECTION = initialize_db()
BAD_QUERIES, BAD_QUERIES_PATH = initialize_bad_queries()
COMPLETED_QUERIES, COMPLETED_QUERIES_PATH = initialize_completed_queries()


def get_grant_data():
    """Get grant data based on each query string"""
    # Obtain the set of unique query strings
    for query in UNIQUE_QUERIES:
        # Create initial query 
        field_query = "(@gfomediatype==\"Grant\") and %s" % query

        # Make the request if it's a good query
        if field_query in BAD_QUERIES or field_query in COMPLETED_QUERIES:
            continue
        else:
            initial_json_response = make_page_request(field_query, 1)
            COMPLETED_QUERIES.add(field_query)
            pickle.dump(COMPLETED_QUERIES, open(COMPLETED_QUERIES_PATH, 'wb'))
        
        # store the intial data for each grant we get back, if it's unique
        stored_successfully = submit_data_to_db(initial_json_response)
        print "On page 1, we found and stored %d unique grants." % stored_successfully

        # Extract total count by this query and divide by number of results per page 
        total_count = initial_json_response["totalCount"]
        num_pages = int(ceil(total_count / results_per_page))
        print "Query: %s" % field_query
        print "Total count: %d; Total pages: %d" %(total_count, num_pages)


        # Create a list of broken queries to improve running time later on 
        if total_count == 0:
            BAD_QUERIES.add(field_query)
            pickle.dump(BAD_QUERIES, open(BAD_QUERIES_PATH, 'wb'))


        # for each successive page, store the unique data
        for i in range(2, num_pages):
            page_json_response = make_page_request(field_query, i)
            stored_successfully = submit_data_to_db(page_json_response)
            print "On page %d, we found and stored %d unique grants." %(i, stored_successfully)


def make_page_request(field_query, page_number):
    """Return JSON response for specified page"""
    PAYLOAD["page"] = page_number
    PAYLOAD["fieldQueries"] = field_query
    r = requests.post(URL, data=json.dumps(PAYLOAD), headers=HEADERS)
    r.raise_for_status()
    try:
        response_json = r.json()
    except:
        raise Exception("Json response empty for page %d of query: %s" %(page_number, field_query))
    else:
        sleep(2)
        return response_json


def submit_data_to_db(data):
    """Submit each result to database. Return a count of total stored."""
    stored_successfully = 0
    for r in data["results"]:
        if store_if_unique(r):
            stored_successfully += 1
    return stored_successfully


def store_if_unique(grant_result):
    """
    Store the grant in our DB if it does not already exist there.
    """
    # Fields we care about:
    ## title, grantee, description, amount, [topics], [regions], year, [categories]
    if not GRANTS_COLLECTION.find_one({"url": grant_result["url"]}):
        grant = {
            "title": grant_result["title"],
            "grantee": grant_result["grantee"],
            "description": grant_result["description"],
            "amount": grant_result["amount"],
            "topics": grant_result["topics"],
            "regions": grant_result["regions"],
            "year": grant_result["year"],
            "date": grant_result["date"],
            "url": grant_result["url"],
        }
        GRANTS_COLLECTION.insert(grant)
        return True
    else:
        return False

if __name__ == "__main__":
    get_grant_data()
