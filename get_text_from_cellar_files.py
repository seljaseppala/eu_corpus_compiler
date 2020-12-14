#!/usr/bin/python
# coding=<utf-8>

"""
    Program to get the text from the XML and HTML files
    downloaded from the EU CELLAR server, clean it up,
    and print it to a new text file.

    Usage: get_text(input_path, output_dir)

    The input_path can be a dir name ending with "/"
    or a text file containing a list of file names.
    The output_dir name must also end with "/".

    XML files with ".doc." and ".toc." in their names are excluded
    as they only contain metadata.

     Note that:
     - Footnotes in HTML files are currently deleted to avoid them being inserted in the middle of a sentence.
     - The text from nested tables in HTML files is repeated.
 """
import os
import sys
from tqdm import tqdm
from utils.file_utils import get_file_list_from_path
from html2txt import html2txt_path_eu
from xml2txt import xml2txt_bs4_eu

sys.path.append("..")

def get_text(input_path, output_dir):
    """
    Get the text from the XML and HTML files
    downloaded from the EU CELLAR server, clean it up,
    and print it to a new text file.
    The input_path can be a dir name ending with "/"
    or a text file containing a list of file names.
    The output_dir name must also end with "/".
    Exclude XML files with ".doc." and ".toc." in their names.

     Note that:
     - Footnotes in HTML files are currently deleted to avoid them being inserted in the middle of a sentence.
     - The text from nested tables in HTML files is repeated.

    :param input_path: dir path str ending with "/"
    :param output_dir: dir path str ending with "/"
    :return:
    """
    # print('INPUT_PATH:', input_path, input_path[-1])
    if input_path[-1] == '/':
        # Get all XML and HTML files in a CELLAR folder
        # under the given path
        xml_file_list = get_file_list_from_path(input_path, name='', extension='.xml')
        html_file_list = get_file_list_from_path(input_path, name='', extension='.html')
        file_list = xml_file_list + html_file_list

    else:
        # Get list of documents listed in the given file
        file_list = [line.rstrip('\n') for line in open(input_path)]
        # print('FILE LIST:', file_list)

    for file_path in tqdm(file_list):
        # Remove unwanted return character in folder names.
        file_path = file_path.replace('\n', '')

        # Get full file name with extension
        file = file_path.split('/')[-1]

        # Get extension
        extension = file_path.split('.')[-1]

        # Get file name without extension
        file_name = file.replace('.' + extension, '').strip()

        # print('FILE_PATH:', file_path)
        # print('EXTENSION:', extension)
        # print('FILE:', file)
        # print('FILE_NAME:', file_name)
        # print('OUT_FILE:', out_file)

        # Write text outputs of each XML and HTML file in a separate file
        # named with the same file name as the original
        # but with a .txt extension
        # and located under the path specified by out_file.
        # Exclude XML files with ".doc." and ".toc." in their names.

        text = ''

        # Get text from XML file
        if extension == 'xml' and '.doc.' not in file_path and '.toc.' not in file_path:
            print('PROCESSING_XML_FILE:', file_path)
            text = xml2txt_bs4_eu(file_path)

        # Get text from HTML file
        elif extension == 'html':
            print('PROCESSING_HTML_FILE:', file_path)
            text = html2txt_path_eu(file_path)

        # print(text[:200])

        # Output to file only if text was extracted from file
        if len(text) > 0:
            # Specify path for output text file
            out_file_path = output_dir + file_name + '.txt'

            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Open output file for writing
            with open(out_file_path, 'w+') as outfile:
                # Write the text to the output file
                outfile.write(text)
