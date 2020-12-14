#!/usr/bin/python
# coding=<utf-8>


"""
Program to send a SPARQL query to the EU SPARQL endpoint and
return a list of CELLAR IDs and other information related to each document.
It includes a function create a list of CELLAR ids to be used for downloading the corresponding files.
The program also has a function to return a list of CELLAR ids
from a CSV file that contains a set of information about each document.
"""
import os

import pandas as pd
from datetime import datetime
from utils.file_utils import text_to_str, to_json_output_file, print_list_to_file
from SPARQLWrapper import SPARQLWrapper, JSON, POST


def get_cellar_info_from_endpoint(sparql_query):
    """
    Send the given sparql_query to the EU Sparql endpoint
    and retrieve and return the results in JSON format.

    :param sparql_query: str
    :return: json dict
    """
    # sparql_query = "r'" + sparql_query + "'"
    # print('QUERY:', sparql_query)

    endpoint = "http://publications.europa.eu/webapi/rdf/sparql" # 2020-06-12 THIS

    ## USING SPARQLWrapper
    sparql = SPARQLWrapper(endpoint)

    sparql.setQuery(sparql_query)

    sparql.setMethod(POST)

    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()
    # print('RESULTS:', results)

    return results


def get_cellar_ids_from_csv_file(file_path):
    """
    Get the list of CELLAR ids from the CSV file in the given file_path.
    Return a list of CELLAR ids.

    Input file format:
    cellarURIs,lang,mtypes,workTypes,subjects,subject_ids

    :param file_path: file path str
    :return: list
    """
    # Read the CSV into a pandas data frame (df)
    df = pd.read_csv(file_path, delimiter=',')

    # Get CELLAR ids
    url_list = df.loc[ : , 'cellarURIs' ]
    csv_id_list = [url.split('/')[-1] for url in url_list]
    # print('CSV_ID_LIST:', csv_id_list, len(csv_id_list))

    return csv_id_list


def get_cellar_ids_from_json_results(cellar_results):
    """
    Create a list of CELLAR ids from the given cellar_results JSON dictionary and return the list.

    :param cellar_results: dict
    :return: list of cellar ids
    """
    results_list = cellar_results["results"]["bindings"]
    cellar_ids_list = [results_list[i]["cellarURIs"]["value"].split('/')[-1] for i in range(len(results_list))]

    return cellar_ids_list


def query_results_to_json(query_results):
    """
    Output query results to json file.
    :param query_results: dict
    :return: None
    """
    # Usage: to_json_output_file(file_name, data)
    to_json_output_file('sparql_query_results/query_results_'+timestamp+'.json', query_results)


def cellar_ids_to_file(id_list, timestamp):
    """
    Output the list of CELLAR ids to txt file.
    :param id_list: list
    :return: None
    """
    dir_name = "cellar_ids/"
    os.makedirs(os.path.dirname(dir_name), exist_ok=True)
    # Usage: print_list_to_file(file_name, data)
    print_list_to_file(dir_name + 'cellar_ids_' + timestamp + '.txt', id_list)


if __name__ == '__main__':
    timestamp = str(datetime.now().strftime("%Y%m%d-%H%M%S"))

    # Get SPARQL query from given file
    sparql_query = text_to_str('sparql_queries/financial_domain_sparql_2019-01-07.rq')

    # Get CELLAR information records from EU Sparql endpoint
    sparql_query_results = get_cellar_info_from_endpoint(sparql_query)
    # print('RETURNED:', sparql_query_results)

    # Output SPARQL query results to json file
    # Usage: query_results_to_json(data)
    query_results_to_json(sparql_query_results)

    # Create a list of ids from the SPARQL query results (in JSON format)
    id_list = get_cellar_ids_from_json_results(sparql_query_results)
    # print('ID LIST:', len(id_list), id_list)


    # # ALTERNATIVELY
    # # If you already have a CSV file with cellar ids,
    # # e.g., copy-pasted from browser results,
    # # specify file (path) containing the CELLAR ids.
    # # Input format: cellarURIs,lang,mtypes,workTypes,subjects,subject_ids
    # cellar_ids_file = 'sparql_query_results/query_results_2019-01-07.csv'
    #
    # # Create a list of CELLAR ids from the given CSV file.
    # id_list_from_file = get_cellar_ids_from_csv_file(cellar_ids_file)


    # Output CELLAR ids list to txt file.
    # with each ID on a new line
    cellar_ids_to_file(id_list, timestamp)
