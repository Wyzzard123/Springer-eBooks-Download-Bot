# Selenium Bot to Download All Free Ebooks

See Springer All Free Ebooks.txt for a list of links extracted by using Excel filters on the "Springer Ebooks.pdf.pdf"
file. The latter is the source of the free ebooks which Springer has given away due to COVID-19.

This bot helps to download all 408 of them.

## How to Use

Install requirements.txt to your virtual or local environment:
```
pip install -r requirements.txt
```

Change directory to the repository and run the download_all_ebooks.py script, with two optional arguments:

```
python download_all_ebooks.py [optional delay in seconds] [optional reference file name surrounded by quotes]
```

Example:
```
python download_all_ebooks.py 5 "Continue Where we left off.txt"
```

Do *not* touch your computer during this time. You can leave the bot on during lunch or dinner. If you interfere with 
your computer during this time, the bot may break. 

This is because the bot does not only rely on Selenium, but also 
PyAutoGUI (Which relies on GUI elements appearing and being in focus).

## Optional Arguments

### Delay

Set an optional argument for delay between actions (default 2 seconds). 

At minimum, this should be set to 2 seconds. Set it slower if your internet or computer is slower.

Otherwise, the code will break frequently as it relies on various UI elements appearing on the screen before it can move on.

If no argument is passed, this will default to the maximum recommended speed of 2 seconds (approximately 66 minutes to
download all files). 

Note that this delay is activated 4 times per file download (Updated 24/4/2020 7 PM UTC+8).

### Reference File Name

You can pass a reference file name as a second argument (in which case you should set the delay as well - default being 2).

The default reference file is "Springer All Free Ebooks.txt", which has all the links from "Springer Ebooks.pdf.pdf" except for 
two which are not actually free:

- https://link.springer.com/book/10.1007%2F978-3-030-19128-3 (Literature and Medicine)
- https://link.springer.com/book/10.1007%2F978-3-319-32185-1 (Business Statistics for Competitive Advantage with
      Excel 2016)

