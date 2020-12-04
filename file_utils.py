#!/usr/bin/python
# coding=<utf-8>

import json
import os
import random
import shutil
from collections import defaultdict
import spacy


def get_file_list_from_path(path, name='', extension='.txt'):
    """
    Get all the files (i.e., file paths) recursively from the given path str.
    Search for a specific name str and/or extension str, if any.
    Return a list of file paths.

    :param path: str
    :param name: str
    :param extension: str
    :return: list of path str
    """

    # Loop over files in folders
    file_list = []
    for dirpath, dirs, files in os.walk(path):
        # print(files)
        for file in files:
            if file.startswith(name) and file.endswith(extension):
                filename = os.path.join(dirpath, file)
                file_list.append(filename)
    # print(file_list)
    return file_list


def get_subdir_list_from_path(dirpath):
    """
    Get the names of the immediate subdirectories in the given path.
    Return a list of subdirectory names.
    Source: https://stackoverflow.com/a/40347279

    :param path: str
    :return: list
    """
    subdir_list = [f.path.split('/')[-1] for f in os.scandir(dirpath) if f.is_dir()]
    # print('SUBDIR_LIST:', len(subdir_list), subdir_list[:10])
    return subdir_list


def file_lines_to_list(file_path):
    """
    Get text of file in the given file_path,
    add each line to a list and return the list.
    Source: https://qiita.com/visualskyrim/items/1922429a07ca5f974467

    :param path: file path str
    :return: list of str
    """
    return [line.rstrip('\n') for line in open(file_path)]


def sentence_to_list(path):
    """
    Get text of file in the given path str,
    process with SpaCy to get each sentence separately
    (in case the input is a single string without newlines).
    Return list of sentences.

    :param path: file path str
    :return: list of sentence str
    """

    # Get the text
    text_as_str = text_to_str(path)

    # Load NLP for English and process text
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text_as_str)

    text_lines_list = []

    for sent in doc.sents:
        text_lines_list.append(sent.text)

    return text_lines_list


def text_to_str(file_path):
    """
    Read lines of file in given path
    and return string of the text.

    :param file_path: file path str
    :return: text str
    """
    with open(file_path, 'r') as file:
        return file.read()


def get_random_sample_dict(text_lines_list, k):
    """
    From the given list of text lines,
    select a random sample of k lines
    and return a dictionary
    where key=line number, value=selected line text.

    :param text_lines_list: list of text str
    :param k: int
    :return: dict of { int : [ list of str ] }
    """
    assert k < len(text_lines_list), "The input text is too short."
    rand_lines = random.sample(text_lines_list, k)

    random_sample = defaultdict()
    for line in rand_lines:
        line_index = text_lines_list.index(line)
        # print(line_index, ':', line.strip())
        random_sample[line_index] = line.strip()

    return random_sample


def get_random_sample_list(text_lines_list, k):
    """
    From the given list of text lines text_lines_list,
    select a random sample of k lines
    and return a list of file names.

    :param text_lines_list: list of text str
    :param k: int
    :return: list of str
    """
    assert k < len(text_lines_list), "The input text is too short."
    # print('RAND_SAMPL:', len(random_sample), random_sample[:10])
    return random.sample(text_lines_list, k)


def copy_files_from_list(file_list, destination_path):
    """
    Copy files from the given file_list of file names
    to the given destination folder (destination_path).

    :param file_list: list of file names
    :param destination_path: path str
    :return: None
    """
    # print('COPY_FUNCTION:', file_list[:10])
    # print('DEST_PATH:', destination_path)
    # print('OS_DIR_LIST:', os.listdir(os.getcwd()))

    # Check existence of destination_path
    # if no such directory, create it
    if destination_path not in os.listdir(os.getcwd()):
        os.makedirs(destination_path)

    counter = 0
    for file_name in file_list:
        if file_name != '':
            # print(file_name)
            counter += 1
            shutil.copy2(file_name, destination_path)

    print('Number of files copied:', counter)


def remove_existing_file_names(file_list, dir_path):
    """
    From the given file_list, remove all the file names
    that exist in the given dir_path.
    Return a new list of non-existing file names.

    :param file_list: list of str
    :return: list of str
    """
    # print('INPUT:', file_list[:10])
    
    # Get names with whole path of the already existing files
    existing_files_dict = defaultdict()
    existing_files_list = get_file_list_from_path(dir_path, name='', extension='')
    # print('EXISTING:', existing_files_list[:10])

    downloads = 0
    for file in existing_files_list:
        downloads += 1

        # Get the file name
        file_id = file.split('/')[-1]

        if file_id == '.DS_Store':
            pass
        else:
            existing_files_dict[file_id] = 0

    # Check whether each file name
    # in the given file_list
    # already exists in the folder.
    # If not, add it to a new list.
    non_existing_files_list = list()

    for file_name in file_list:

        # Get the file name from full path
        if file_name.split('/')[-1] in existing_files_dict:
            pass
        else:
            non_existing_files_list.append(file_name)

    # print('LEN file_list/non_existing_files_list/existing_files_dict:', len(file_list), '/', len(non_existing_files_list), '/', len(existing_files_dict), len(non_existing_files_list)+len(existing_files_dict))

    return non_existing_files_list


def json2dict(file_name):
    # print(file_name)
    with open(file_name, 'r') as f:
        # pprint(json.load(f))
        return json.load(f)


def to_json_output_file(file_name, data):
    """
    Print the given data input to 
    a file in json format with the given file_name.

    :param file_name: str
    :param data: structured data
    :return: text file
    """
    with open(file_name, 'w') as outfile:
        # print('JSON_DUMPS:', json.dumps(data))
        json.dump(data, outfile, indent=4)


def print_list_to_file(outfile_name, list):
    """
    Create a file with the given outfile_name
    and print each element in the given list
    on a new line of the new file.
    Last line not followed by newline.

    :param outfile_name: str
    :param list: list
    :return: None
    """
    with open(outfile_name, 'w') as outfile:
        for elt in list[:-1]:
            outfile.write('{name}{newline}'.format(name=elt, newline='\n'))
            # outfile.write("%s\n" % file_name)

        # Last line not followed by newline
        for file_name in list[-1]:
            outfile.write(file_name)