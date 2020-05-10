# PDF Downloader (Updated 10/5/2020)

See Springer All Free Ebooks.txt for a list of links extracted by using Excel filters on the "Springer Ebooks.pdf"
file. The latter is the source of the free ebooks which Springer has given away due to COVID-19.

This new version of the script now uses the requests library as well as multithreading. 
 
There is no need for the Selenium webdriver. To use the old version, follow the instructions in Selenium_README.md. To use the old script, use "download_all_ebooks_selenium.py" instead of 
"download_all_ebooks.py".

This version also uses a text file containing __direct__ download links, instead of links which require Selenium to click 
a button. This new set of links is at "Springer PDF Direct Download Links.txt".

Every link in the text file is written as "\[title] | \[download link]". For example:

``` 
Fundamentals of Power Electronics  | https://link.springer.com//content/pdf/10.1007%2Fb100747.pdf
```

This means that as long as you have a txt file in this format, you can now use download_all_ebooks.py __regardless of which website they come from__
(not just Springer).

Note that some books are no longer free. At the time of writing, the 408 books have decreased to 387.

In order to generate such a list of txt files for a different website, you may refactor the new script called "write_direct_pdf_links_to_txt_file.py".

## How to Use

Download Python and pip.

Upgrade pip in the command line with the following command:
``` 
easy_install -U pip
```

Install requirements.txt to your virtual or local environment:
```
pip install -r requirements.txt
```

Change directory to the repository and run the download_all_ebooks.py script, with two optional arguments:

```
python download_all_ebooks.py [Reference Text File] [Path to download folder surrounded by quotes]
```
You do NOT need to add any of the optional arguments. In other words, because of the default arguments:
``` 
python download_all_ebooks.py
```
is equivalent to:
```
python download_all_ebooks.py "Springer All Free Ebooks after failure.txt" "Springer PDFs"
```

## Optional Arguments

### Reference File Name

You can pass a reference file name as a second argument.

The default reference file is "Springer PDF Direct Download Links.txt", which has all the direct download links obtained 
from the links in "Springer Ebooks.pdf" except for those which are not actually free at the time of writing.

### Path to download folder

All the PDFs will be sent to this folder.

