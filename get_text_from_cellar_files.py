#!/usr/bin/python
# coding=<utf-8>

"""
    Program to get the text from the XML and HTML files
    downloaded from the EU CELLAR server, clean it up,
    and print it to a new text file.

    If replace_existing=False (default setting),
    the program checks the output_dir
    for existing text files and only processes files
    from which the text has not yet been extracted.

    Usage: get_text(input_path, output_dir, replace_existing=False)

    The input_path can be a dir name ending with "/"
    or a text file containing a list of file names.
    The output_dir name must also end with "/".

    XML files with ".doc." and ".toc." in their names are excluded
    as they only contain metadata.

     Note that:
     - Footnotes in XML files are currently deleted to avoid them being inserted in the middle of a sentence.
     - The text from nested tables in HTML files is repeated.
 """
import os
import sys
from tqdm import tqdm
from utils.file_utils import get_file_list_from_path
from utils.html2txt import html2txt_path_eu
from utils.xml2txt import xml2txt_bs4_eu

sys.path.append("..")

def get_text(input_path, output_dir, replace_existing=False):
    """
    Get the text from the XML and HTML files
    downloaded from the EU CELLAR server, clean it up,
    and print it to a new text file.
    The input_path can be a dir name ending with "/"
    or a text file containing a list of file names.
    The output_dir name must also end with "/".
    Exclude XML files with ".doc." and ".toc." in their names.

     Note that:
     - Footnotes in XML files are currently removed to avoid them being inserted in the middle of a sentence.
     - The text from nested tables in HTML files is repeated.

    :param input_path: dir path str ending with "/"
    :param output_dir: dir path str ending with "/"
    :return:
    """
    # Get list of files to process
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
        # print('FILE_LIST:', file_list)

    # Get list of existing text files
    existing_txt_files_list = [f.split('/')[-1].replace('.txt','') for f in get_file_list_from_path(output_dir, name='', extension='.txt')]
    # print('EXISTING_TXT_FILES:', existing_txt_files_list)

    # Display processed file and progress bar
    pbar = tqdm(total=len(file_list), desc='{desc}')

    # Process XML and HTML files in file_list
    for file_path in file_list:

        # Display processed file
        pbar.update(1)

        # Remove unwanted return character in folder names.
        file_path = file_path.replace('\n', '')

        # Get full file name with extension
        file = file_path.split('/')[-1]

        # Get CELLAR id
        cellar_id = file_path.split('/')[-2]

        # Get extension
        extension = file_path.split('.')[-1]

        # Get file name without extension
        file_name = file.replace('.' + extension, '').strip()

        # print('FILE_PATH:', file_path)
        # print('EXTENSION:', extension)
        # print('FILE:', file)
        # print('FILE_NAME:', file_name)
        # print('OUT_FILE:', out_file)

        # Check whether text file already exists in output_dir
        if replace_existing == False and file_name in existing_txt_files_list:
            # print('FILE_EXISTS:', file_name, file_path)
            pass

        else:
            # Write text outputs of each XML and HTML file in a separate file
            # named with the same file name as the original
            # but with a .txt extension
            # and located under the path specified by out_file.
            # Exclude XML files with ".doc." and ".toc." in their names.
            text = ''

            # Get text from XML file
            if extension == 'xml' and '.doc.' not in file_path and '.toc.' not in file_path:
                pbar.set_description_str(f'Processing file: <XML> {cellar_id}/{file}', refresh=True)
                text = xml2txt_bs4_eu(file_path)

            # Get text from HTML file
            elif extension == 'html':
                pbar.set_description_str(f'Processing file: <HTML> {cellar_id}/{file}', refresh=True)
                text = html2txt_path_eu(file_path)

            # print(text[:200])

            # Output to file only if text was extracted from file
            if len(text) > 0:
                # Specify path for output text file
                out_file_path = output_dir + file_name + '.txt'

                # Create output directory if it doesn't exist
                os.makedirs(os.path.dirname(output_dir), exist_ok=True)

                # Open output file for writing
                with open(out_file_path, 'w+') as outfile:
                    # Write the text to the output file
                    outfile.write(text)

if __name__ == '__main__':

    # Specify input dir name
    input_path = "/Users/seljaseppala/Dropbox/Documents/Programmes/regdef_corpus/corpus_compiler_testing/cellar_files_testing/"
    # input_path = "/Users/seljaseppala/Git/eu_corpus_compiler/data/cellar_files_20201216-124636/"

    # Specify path for output text files
    output_dir = '/Users/seljaseppala/Dropbox/Documents/Programmes/regdef_corpus/corpus_compiler_testing/text_files_testing_new/'
    # output_dir = '/Users/seljaseppala/Git/eu_corpus_compiler/data/text_files_20201216-124636/'

    # Get the text
    get_text(input_path, output_dir, replace_existing=True)