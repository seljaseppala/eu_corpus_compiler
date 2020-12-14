#!/usr/bin/python
# coding=<utf-8>

""" Functions to extract the text from HTML documents or strings. """

import re
from bs4 import BeautifulSoup
import sys
sys.path.append("..")


def html2txt_str(string):
    """
    Get text string from the given string with HTML tags.
    Clean up and return the text str.

    :param string: str
    :return: str
    """
    # Get text str from html str
    html_str = BeautifulSoup(string, features="lxml")
    raw_str = html_str.get_text(separator="\n")

    # Clean up the string
    clean_str = clean_up_str(raw_str)

    return clean_str


def html2txt_path(file_path):
    """
     Get text string from the HTML file in the given file_path.

    :param file_path: str
    :return: str
    """

    with open(file_path, 'r') as file:
        text = ' '.join(file.readlines())
        output_text = html2txt_str(text)

        return output_text


def html2txt_path_eu(file_path):
    """
    Get text string from the HTML file in the given file_path of EU file.

    :param file_path: str
    :return: str
    """

    with open(file_path, 'r') as file:
        text = ' '.join(file.readlines())
        output_text = html2txt_str_eu(text)

        return output_text


def html2txt_str_eu(string):
    """
    Get text string from the given string with HTML tags from EU docs.
    Clean up and return the text str of the document where each <p> tag
    is on a new line.

    :param string: str
    :return: str
    """
    # Get text str from html str
    html_str = BeautifulSoup(string, features="lxml")

    raw_str_list = []
    for tag in html_str.html.find_all():

        # Get text from tables
        if tag.name == 'table':
            # Get text for each row and append it to a list
            raw_str_list.append(table2txt(tag))

        # Get text from tags outside tables
        # If tag is p and p is not in a table and has no other p descendents
        elif tag.name == 'p' and 'table' not in [tab.name for tab in tag.parents] and tag.p == None:
            # print('TAG_P_is_None:', tag.p == None)
            raw_str_list.append(tag.get_text(separator=" "))
            # print('P_TXT:', tag.get_text(separator=" "))
    # print('RAW_STR_LIST:', raw_str_list)

    # Clean up strings in list
    clean_str_list = []
    for raw_str in raw_str_list:

        clean_str = clean_up_str(raw_str)

        # Add clean str to new list
        clean_str_list.append(clean_str)

    all_text = '\n\n'.join(clean_str_list)

    # Replace multiple returns with a single one
    clean_up_return = re.compile(r'\n{2,}')
    clean_text = re.sub(clean_up_return, r'\n', all_text)

    # print('CLEAN:', clean_text)
    return clean_text


def table2txt(table):
    """
    Get the text in the <p> tags of the rows of the given table.
    Join the extracted text with a space to reconstruct the row.
    Return the new row str.

    :param table: str
    :return: str
    """
    output_rows_list = []

    for table_row in table.find_all('tr'):
        columns = table_row.find_all('td', recursive=False)

        for column in columns:
            output_rows_list.append(column.find_next("p").text.strip())

    text_str = ' '.join(output_rows_list)
    # print('DATA:', text_str)

    return text_str


def clean_up_str(raw_str):
    """
    Clean up the given raw_str string and return a clean str.

    :param raw_str: str
    :return: str
    """
    # Replace insecable spaces with normal spaces
    stripped_str = raw_str.replace('\u00a0', ' ')

    # Replace insecable spaces with normal spaces
    stripped_str = stripped_str.replace('\xa0', ' ')

    # Remove space before period
    clean_up_dot = re.compile(r'\s\.')
    stripped_str = re.sub(clean_up_dot, '.', stripped_str).strip()

    # Remove space before comma
    clean_up_comma = re.compile(r'\s,')
    stripped_str = re.sub(clean_up_comma, ',', stripped_str).strip()

    # Remove space before colon
    clean_up_semi_colon = re.compile(r'\s;')
    stripped_str = re.sub(clean_up_semi_colon, ';', stripped_str).strip()

    # Remove space after opening parenthesis
    clean_up_open_par = re.compile(r'\(\s+')
    stripped_str = re.sub(clean_up_open_par, '(', stripped_str).strip()

    # Remove space before closing parenthesis
    clean_up_close_par = re.compile(r'\s+\)')
    stripped_str = re.sub(clean_up_close_par, ')', stripped_str).strip()

    # # Replace multiple returns with a single one
    # clean_up_return = re.compile(r'\n{2,}')
    # stripped_str = re.sub(clean_up_return, r'\n', stripped_str)

    # # Remove returns before and after a single character
    # clean_up_return = re.compile(r'\n[a-zA-Z0-9\(\)]{,2}\n')
    # text_str = re.sub(clean_up_return, '$1', text_str)

    # Restore lines in tables
    restore_lines = re.compile(r'^(\([^\)]+\))\n')
    restored_lines = re.sub(restore_lines, '\0 ', stripped_str)

    # Replace multiple spaces with a single space
    clean_up_spaces = re.compile(r'\s{2,}')
    clean_str = re.sub(clean_up_spaces, ' ', restored_lines)

    return clean_str


