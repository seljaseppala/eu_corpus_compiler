#!/usr/bin/python
# coding=<utf-8>


""" Functions to extract the text from XML documents into a new text file. """

import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup, NavigableString, Tag
from utils.html2txt import html2txt_path_eu


def xml2txt_etree(file_path):
    """
    Get the text from the given XML file and return a text string.
    The text within XML tags is separated by spaces.
    In some cases, this generates double spaces,
    which are then replaced by a single space.

    :param file: str of XML file name
    :return: text str
    """

    tree = ET.parse(file_path)
    root = tree.getroot()

    text = ' '.join(root.itertext()).replace('  ', ' ').replace('\n ', '\n').replace(' \n', '\n')

    double_returns = re.compile('\n\n')
    text = re.sub(double_returns, '\n', text).strip()

    return text


def xml2txt_bs4(file_path: str):
    # Get XML root from file and text from XML
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_str = BeautifulSoup(file.read(), "lxml-xml")
        # print('XML_STR:', xml_str)

        # Get text
        raw_str = xml_str.get_text(" ", strip=True)

        # Clean-up text
        clean_str = clean_up_str(raw_str)

        return clean_str


def xml2txt_bs4_eu(file_path: str):
    # Get XML root from file and text from XML
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_str = BeautifulSoup(file.read(), "lxml-xml")
        # print('XML_STR:', xml_str.prettify())
        # print('XML_NEXT_SIBLING:', xml_str.contents[0].next_sibling)
        # print('XML_CONTENTS:', xml_str.contents[0].name)
        # print('XML_CHILDREN:', len(list(xml_str.contents[0].children)), list(xml_str.contents[0].children))
        # print('XML_TAGS:', [tag.name for tag in xml_str.find_all()])
        # print('XML_NESTED:', len(xml_str.ACT.findChildren(recursive=False)))

        # If XML file with Doctype declaration, process with html2txt
        if 'html' in xml_str.contents[0]:
            return html2txt_path_eu(file_path)
        # Else, process XML
        else:
            # Remove footnotes
            footnotes = xml_str.find_all(TYPE="FOOTNOTE")
            for note in footnotes:
                # print('NOTE:', note)
                note.clear()

            # Get text
            raw_str_list = []
            for child in xml_str.contents[0].children:
                if isinstance(child, NavigableString):
                    # print('NavigableString:', child.name)
                    continue
                if isinstance(child, Tag):
                    # print('CHILD:', child.name)
                    raw_str_list.append(child.get_text(" ", strip=True))

        raw_str = '\n\n'.join(raw_str_list)
        # print('RAW_STR:', raw_str)

        # Clean-up text
        clean_str = clean_up_str(raw_str)

        return clean_str


def clean_up_str(raw_str):
    """
    Clean up given raw text string (raw_str) and return a clean string.
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
    clean_up_open_par = re.compile(r'\(\s')
    stripped_str = re.sub(clean_up_open_par, '(', stripped_str).strip()

    # Remove space before closing parenthesis
    clean_up_close_par = re.compile(r'\s\)')
    clean_str = re.sub(clean_up_close_par, ')', stripped_str).strip()

    # # Add returns before subdivisions -> Produces too much noise
    # subdivisions = re.compile(r'\. ((chapter|subsection|section|article) [A-Z]+)', flags=re.IGNORECASE)
    # clean_str = re.sub(subdivisions, '.\n\n\g<1>', stripped_str).strip()

    # print('TEXT:', raw_str, '\n')
    # print('STRIPPED:', stripped_str)
    # print('CLEAN:', clean_str)

    return clean_str

