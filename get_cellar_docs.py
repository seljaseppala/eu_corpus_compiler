#!/usr/bin/python
# coding=<utf-8>


""" Program to send GET requests to download zip files for the given documents under a CELLAR URI."""


import requests
import zipfile
import io
from collections import defaultdict
from datetime import datetime
from file_utils import get_file_list_from_path, text_to_str
from SPARQLWrapper import SPARQLWrapper, XML, POST, GET, URLENCODED, POSTDIRECTLY, JSON
import os
import threading
from threading import Thread
import time
from tqdm import tqdm


def get_cellar_ids_from_file(file_path):
    """
    Get the list of cellar IDs from the file in the given file_path.
    Check whether the id is already present in the directory
    containing previously downloaded files.

    Return a list of cellar_ids absent from the directory.

    :param file_path: file path str
    :return: set
    """

    # Get CELLAR ids of the files already downloaded
    downloaded_files_dict = defaultdict()
    downloaded_files_list = get_file_list_from_path("texts/", name='', extension='')
    downloads = 0
    for file in downloaded_files_list:
        downloads += 1
        cellar_id = file.split('/')[1]
        downloaded_files_dict[cellar_id] = 0

    # Get all the CELLAR ids retrieved with SPARQL query
    # in the given file_path

    # Set counter to zero
    count = 0

    # Create set (to avoid duplicates) of CELLAR ids to process
    cellar_ids = set()

    with open(file_path, 'r') as file:
        file_contents = file.readlines()

        # If the files with that id have not
        # already been downloaded
        # and the id was not added to the list
        # of ids to process (cellar_ids),
        # add the id to the latter dict.
        for line in file_contents[1:]:
            id = line.split(',')[0].split('/')[-1].strip()
            if id not in downloaded_files_dict.keys() and id not in cellar_ids:
                count += 1
                cellar_ids.add(id)

    return cellar_ids


def rest_get_call(id):
    """Send a GET request to download a zip file for the given id under the CELLAR URI."""

    url = 'http://publications.europa.eu/resource/cellar/' + id

    headers = {
        'Accept': "application/zip;mtype=fmx4, application/xml;mtype=fmx4, application/xhtml+xml, text/html, text/html;type=simplified, application/msword, text/plain, application/xml;notice=object",
        'Accept-Language': "eng",
        'Content-Type': "application/x-www-form-urlencoded",
        'Host': "publications.europa.eu"#,
    }

    response = requests.request("GET", url, headers=headers)

    return response


def download_zip(response, folder_path):
    """
    Downloads the zip file returned by the restful get request.
    Source: https://stackoverflow.com/questions/9419162/download-returned-zip-file-from-url?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    """
    z = zipfile.ZipFile(io.BytesIO(response.content))
    z.extractall(folder_path)


def process_range(sub_list, i):
    """
    Process a list of ids to download the corresponding zip files.

    :param sub_list: list of str
    :param i: int
    :return: write to files
    """
    # Specify folder_path to send results of request
    # Commented the creation of numbered subfolders
    folder_path = "texts/" #+ str(i + 1) + "/"

    # Keep track of downloads
    zip_files = []
    single_files = []
    other_downloads = []

    # Count downloads
    count_cellar_ids = 0
    count_zip = 0
    count_single= 0
    count_other = 0

    for id in sub_list:
        count_cellar_ids += 1

        # Specify sub_folder_path to send results of request
        sub_folder_path = folder_path + id

        # Send Restful GET request
        response = rest_get_call(id.strip())

        # If the response's header contains the string 'Content-Type'
        if 'Content-Type' in response.headers:

            # If the string 'zip' appears as a value of 'Content-Type'
            if 'zip' in response.headers['Content-Type']:

                count_zip += 1
                zip_files.append(id)

                # Download the contents of the zip file in the given folder
                download_zip(response, sub_folder_path)

            # If the value of 'Content-Type' is not 'zip'
            else:
                count_single += 1
                single_files.append(id)

                # Create a directory with the cellar_id name
                # and write the returned content in a file
                # with the same name
                out_file = sub_folder_path + '/' + id + '.xml'
                os.makedirs(os.path.dirname(out_file), exist_ok=True)
                with open(out_file, 'w') as f:
                    f.write(response.text)

        # If the response's header does not contain the string 'Content-Type'
        else:
            count_other += 1
            other_downloads.append(id)
            print(response.content)

            #  Write the returned content in a file
            # out_file = sub_folder_path + '/' + id + '.xml'
            # with open(out_file, 'wb') as f:
            #     f.write(response.text)

    # log_text = ("\nQuery file: " + __file__ +
    #             "\nDownload date: " + str(datetime.today()) +
    #             "\n\nNumber of zip files downloaded: " + str(count_zip) +
    #             "\nNumber of non-zip files downloaded: " + str(count_single) +
    #             "\nNumber of other downloads: " + str(count_other) +
    #             "\nTotal number of cellar ids processed: " + str(count_zip + count_single + count_other) +
    #             "\n\nTotal number of downloaded files: " + str(count_zip + count_single) +
    #             "\nTotal number of cellar ids: " + str(len(id_list)) +
    #             "\n\n========================================\n"
    #             )
    #
    # print(log_text)

    # Write the list of other (failed) downloads in a file
    with open('failed.txt', 'a') as f:
        f.write(str(other_downloads))


if __name__ == '__main__':

    # Specify file (path) containing the cellar IDs
    cellar_ids_file = 'cellar_ids/cellar_ids_2019-06-11.txt'

    # Create a list of ids from the ids file
    id_list = list(get_cellar_ids_from_file(cellar_ids_file))
    print('ID LIST:', len(id_list), id_list)

    # Run multiple threads in parallel to download the files
    # Adapted from: https://stackoverflow.com/questions/16982569/making-multiple-api-calls-in-parallel-using-python-ipython
    nthreads = 11
    threads = []
    for i in range(nthreads):  # Four times...
        print(id_list[i::nthreads])
        sub_list = id_list[i::nthreads]
        t = Thread(target=process_range, args=(sub_list, i))
        threads.append(t)

    # start the threads
    [t.start() for t in threads]
    # wait for the threads to finish
    [t.join() for t in threads]
