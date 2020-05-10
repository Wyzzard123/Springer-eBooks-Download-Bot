"""
Download each ebook from the direct downloads page directly and with multi-threading.
"""
import concurrent.futures
import os
from tqdm import tqdm
import requests
import re
import sys


def get_direct_link_strings(txt_file):
    with open(txt_file, "r") as txt:
        return txt.readlines()


def get_title_and_direct_links(txt_file):
    direct_link_strings = get_direct_link_strings(txt_file)

    titles_and_direct_links = []
    with open(txt_file, "r") as txt:
        # Filter out all non-alphanumeric characters from title
        re_pattern = r"[A-Za-z0-9 ]"

        for index, direct_link_string in enumerate(direct_link_strings):
            title, direct_link = (title_and_direct_link.strip() for title_and_direct_link in
                                  direct_link_string.split("|"))
            print(index + 1, title, "-", direct_link)
            title = "".join(re.findall(re_pattern, title))
            titles_and_direct_links.append((title, direct_link))

    return titles_and_direct_links


def download_pdf_from_link(title, link, folder_name=None):
    BASE_DIR = os.getcwd()
    try:
        response = requests.get(link)
        pdf_content = response.content
        filename = f"{title}.pdf"
        if folder_name:
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
                print(f"Created directory {folder_name}")
            file_path = os.path.join(BASE_DIR, folder_name, filename)
        else:
            file_path = os.path.join(BASE_DIR, filename)

        # Ignore if file already exists.
        if os.path.isfile(file_path):
            result_str = f"{str(file_path)} - {link} already exists. Moving on."
            print(result_str)
            return result_str

        with open(file_path, 'wb') as pdf_file:
            pdf_file.write(pdf_content)
            result_str = f"Done at {str(file_path)} - {title}: {link}"
            print(result_str)
            return result_str
    except Exception as e:
        print(e.args)
        result_str = f"Failed for {title}: {link}"
        print(result_str)
        return result_str


def download_pdf_from_link_tuples(title_link_folder_name_tuple):
    """
    Creating a helper function to easily use the ThreadPoolExecutor().map() method.
    Pass in a list of tuples with the title, link and folder_name.

    E.g.:
    links = get_title_and_direct_links("Springer PDF Direct Download Links.txt")
    # print(links)
    folder_name = "New PDFs"
    with concurrent.futures.ThreadPoolExecutor() as executor:
        args = [(title, link, folder_name) for title, link in links]
        executor.map(download_pdf_from_link_tuples, args)

    :param title_link_folder_name_tuple:    List of tuples of (title, link, folder_name)
    :type title_link_folder_name_tuple:     tuple
    :return:                                None
    :rtype:                                 None
    """
    return download_pdf_from_link(*title_link_folder_name_tuple)


def download_pdfs_in_link_to_folder(txt_file, folder_name, use_progress_bar=False):
    links = get_title_and_direct_links(txt_file)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if use_progress_bar:
            with tqdm(total=len(links)) as progress_bar:
                futures = []
                for title, link in links:
                    # TODO - None of the prints are printing. I have to put everything in return values? What about errors?
                    # TODO - One suggested solution has been to use tqdm.write instead of print in order to keep the progress bar at the bottom
                    future = executor.submit(download_pdf_from_link, title, link, folder_name)
                    future.add_done_callback(lambda p: progress_bar.update())
                    futures.append(future)
                results = []
                for future in futures:
                    result = future.result()
                    results.append(result)
        elif not use_progress_bar:
            # Version without progress bar.
            title_link_folder_name_tuples = [(title, link, folder_name) for title, link in links]
            executor.map(download_pdf_from_link_tuples, title_link_folder_name_tuples)

    print("Done")


if __name__ == "__main__":

    # Parsing command line arguments.
    if len(sys.argv) > 1:
        txt_file = sys.argv[1]
        if not os.path.isfile(txt_file):
            raise Exception("Usage: python download_all_ebooks.py [txt_file] [download folder]\n"
                            "The first argument should be the txt_file to reference. The provided file does not exist. "
                            "By default this is 'Springer PDF Direct Download Links.txt'."
                            )
    else:
        txt_file = "Springer PDF Direct Download Links.txt"
        if not os.path.isfile(txt_file):
            raise Exception("Did you delete/rename/move the file 'Springer PDF Direct Download Links.txt'?")

    print("Reference Text File:", txt_file)

    if len(sys.argv) > 2:
        folder_name = sys.argv[2]
    else:
        folder_name = "Springer PDFs"

    print("Download Folder:", folder_name)

    download_pdfs_in_link_to_folder(txt_file, folder_name)
