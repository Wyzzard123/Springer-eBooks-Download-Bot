"""
Used to write the direct download links from the Springer website based on Springer All Free Ebooks.txt to another
txt file.

You may refactor this for use on any other website.
"""

import concurrent.futures
import requests
from bs4 import BeautifulSoup

def get_direct_pdf_links(link, base_link='https://link.springer.com'):
    """
    Get all the direct pdf download links from the links in the txt_file (containing Springer Links) and output them to a text file.

    :param txt_file:    File with links to download page. We will try to get the direct-download link from each.
    :return:            None
    """
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    # CHANGE THIS: This line of code is used because Springer page titles take the form of
    # "Intuitive Probability and Random Processes Using MATLAB® | SpringerLink", where we are only interested in the
    # portion before the '|'
    title = soup.find("title").text.split("|")[0]
    try:
        # CHANGE THIS: This is a particular CSS selector used to grab direct PDF download links from the Springer
        # website. Your website will likely be different if you are refactoring this code.
        direct_pdf_link = soup.select_one("a[title='Download this book in PDF format']").get('href')

    except AttributeError as e:
        print(e)
        print(f"Book might not be downloadable for free: {link}")
        print("Moving on")
        return None
    else:
        # CHANGE base_link: This is the main link. Most of the direct_pdf_link's will be obtained as "/xxx", with the
        # base_link omitted. Thus, you need to add it back in. If your website does not do this, then you may safely
        # remove the "base_link" variable from this code.
        direct_link_string = f"{title} | {base_link}{direct_pdf_link}\n"
        print(direct_link_string)
        return direct_link_string

def write_to_txt_file(txt_file, output_file, base_link='https://link.springer.com'):
    with open(txt_file, 'r') as txt:
        current_links = txt.readlines()
        print(current_links)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            list_of_futures = [executor.submit(get_direct_pdf_links, current_link, base_link) for current_link in current_links]
            list_of_links = filter(lambda x: x is not None, map(lambda future: future.result(), list_of_futures))
    with open(output_file, 'w') as output:
        output.writelines(list_of_links)
        print(f"Done writing to {output_file}")

if __name__ == "__main__":
    # CHANGE THESE VARIABLES:
    txt_file = "Springer All Free Ebooks.txt"
    output_file = "Springer PDF Direct Download Links.txt"
    base_link = 'https://link.springer.com'
    write_to_txt_file(txt_file, output_file, base_link)