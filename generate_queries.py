"""
Generate possible queries from Gates Found grant database. 

There are 4 filters and >11K possibilities, Bill returns a max of 1000 results per query combo. 
So the hope is that by using all potential queries, we will get everything. Otherwise, their 
system is broken too!
"""
import json
import requests
from itertools import product

from gates_constants import PAYLOAD, HEADERS, URL


def get_inital_parameters():
    """Request an unfiltered set of data from grant database to get a list of all filters"""
    # Request
    r = requests.post(URL, data=json.dumps(PAYLOAD), headers=HEADERS)
    r.raise_for_status()
    # Return raw JSON
    try:
        return r.json()
    except:
        raise Exception("Json response empty in intial request!!!")


def extract_facets(raw_json_response):
    """Extract facets dictionaries from response"""
    facets_dict = {}

    for f in raw_json_response["facets"]:
        facets_dict[f["field"]] = f["items"]

    return facets_dict


def create_field_dicts(facets_dict, minimum_count):
    """
    Return one dictionary with four entries; each key is a filter category
    with the corresponding list of all possible values.

    Exclude sets that would return below the minimum_count. 

    From quick testing:
    When minimum_count = 1, unique_queries = 19,403
    When minimum_count = 5, unique_queries = 18,521
    When minimum_count = 100, unique_queries = 6551
    When minimum_count = 150, unique_queries = 4031
    """
    master_dict = {}
    for key, value in facets_dict.items():
        category_set = {key: set()}
        for v in value:
            if v["count"] >= minimum_count:
                category_set[key].add(v["name"])
        master_dict.update(category_set)

    for k, v in master_dict.items():
        master_dict[k] = list(v)

    return master_dict


def generate_unique_queries(fields_dict):
    """
    Return list of strings, where each string is a unique
    possible query for the grant data set
    """
    # create sets of each category's options
    # Reference: "fieldQueries":
    # (@gfocategories==\"US Program\")
    # (@gfotopics==\"College-Ready\")
    # (@gfoyear==\"2009 and earlier\")
    # (@gforegions==\"North America\")
    master_query_set = set()
    template_query = "(@%s==\"%s\")"

    # Convert each plain string into it's query string equivalent
    query_string_dict = {}
    for category, fields in fields_dict.items():
        query_string_dict[category] = []
        for f in fields:
            query_string = template_query % (category, f)
            query_string_dict[category].append(query_string)
            # Add each query on it's own (without combining with other
            # possibilities)
            master_query_set.add(query_string)

        # Also, add an empty entry to each dictionary
        # (this is so the itertools.product function will return
        # possible combos including 0)
        query_string_dict[category].append("")

    # Generate the product of all possible queries as well
    # Why yes, what I did here does make me feel like a fool.
    list_of_tuples = product(
        query_string_dict.values()[0],
        query_string_dict.values()[1],
        query_string_dict.values()[2],
        query_string_dict.values()[3]
    )

    # Make tuple into strings
    query_strings = []
    # Remove empty strings
    strings_gone = [tuple(y for y in x if y != "") for x in list_of_tuples]
    for item in strings_gone:
        # remove empty tuples
        if len(item) > 0:
            # convert them to actual query strings
            query_strings.append(" and ".join(str(i) for i in item))

    master_query_set.update(query_strings)

    return list(master_query_set)


def save_unique_queries(minimum_count=150):
    """Save/update unique queries on disk"""
    print "Retrieving unique query strings, minimum filter count = %d" % minimum_count
    raw_json = get_inital_parameters()
    facets_dict = extract_facets(raw_json)
    fields_dict = create_field_dicts(facets_dict, minimum_count)
    unique_queries = generate_unique_queries(fields_dict)
    print "Returning a set of %d unique queries" % len(unique_queries)
    with open("unique_queries.json", 'w') as outfile:
        json.dump(unique_queries, outfile)

if __name__ == "__main__":
    queries = save_unique_queries()
