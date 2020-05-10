# Selenium Bot to Download All Free Ebooks

See Springer All Free Ebooks.txt for a list of links extracted by using Excel filters on the "Springer Ebooks.pdf"
file. The latter is the source of the free ebooks which Springer has given away due to COVID-19.

This bot helps to download all 408 of them.

UPDATE on 25/4/2020: The bot now runs completely in the background and is at least 4 times faster. 

UPDATE on 10/5/2020: This bot is now deprecated and this README renamed to Selenium_README.md. 

You must, however, close the new Chrome window manually.

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

Change directory to the repository and run the download_all_ebooks_selenium.py script, with four optional arguments:

```
python download_all_ebooks_selenium.py [Path to download folder surrounded by quotes] [Reference Text File] [Delay/s] [Run in Background ('True' or 'False']
```
You do NOT need to add any of the optional arguments.

Unless you use background mode (an older implementation of the code which you can activate using the fourth positional argument),
you can continue to use your computer during this time.

The code will open a chrome window which will download everything in the background.

Note that you must close the Chrome window manually. This is to prevent the Chrome window from closing prematurely (before your downloads are complete).
## Driver

If your Google Chrome is not Chrome 81 (Check by going to "Help > About Chrome), download the appropriate driver from here:
https://chromedriver.chromium.org/downloads

Then replace the driver for your OS. The code automatically checks for your OS and uses the correct driver accordingly.

## Stopping the Program prematurely

To stop the program prematurely, go to the console and press "Ctrl + C".

To continue where you left off, pass in a reference text file with the remaining links as an argument (second positional argument).

## Example Usage
Example (using default arguments):
```
python download_all_ebooks_selenium.py "C:\Downloads\Ebooks"
```

Example (continuing where we left off if code fails prematurely):
```
python download_all_ebooks_selenium.py "C:\Downloads\Ebooks" "Springer All Free Ebooks after failure.txt"
```

Example (using foreground mode with a longer delay):
```
python download_all_ebooks_selenium.py "C:\Downloads\Ebooks" "Springer All Free Ebooks after failure.txt" 5 false
```


## Optional Arguments

### Path to download folder

All the PDFs will be sent to this folder.

### Reference File Name

You can pass a reference file name as a second argument (in which case you should set the delay as well - default being 2).

The default reference file is "Springer All Free Ebooks.txt", which has all the links from "Springer Ebooks.pdf.pdf" except for 
two which are not actually free:

- https://link.springer.com/book/10.1007%2F978-3-030-19128-3 (Literature and Medicine)
- https://link.springer.com/book/10.1007%2F978-3-319-32185-1 (Business Statistics for Competitive Advantage with
      Excel 2016)

### Delay

Set an optional argument for delay between actions (default 2 seconds). 

This does not matter as much if you are running in the default Background mode. See below for notes on delay when not
running in background mode.

If running in background mode, the bot should take approximately 15 minutes. If not, the bot should take about 66 minutes to download every file.


### Background

If you set this to "False" or "F", this will run in the old mode which requires the window to be in focus. This is much 
slower and not recommended.

By default, this is set to "True" or "T".

If you are using background mode, do *not* touch your computer during this time. You can leave the bot on during lunch or dinner. If you interfere with 
your computer during this time, the bot may break. 

This is because the bot in background mode does not only rely on Selenium, but also PyAutoGUI (Which relies on GUI elements appearing and being in focus).

#### Delay while in Background Mode

If background is set to "true", take note of the following for the delay argument:

* At minimum, the delay should be set to 2 seconds. Set it slower if your internet or computer is slower.

* Otherwise, the code will break frequently as it relies on various UI elements appearing on the screen before it can move on.

* If no argument is passed, this will default to the maximum recommended speed of 2 seconds (approximately 66 minutes to
download all files). 

* Note that this delay is activated 4 times per file download (Updated 24/4/2020 7 PM UTC+8) (only 1 time when running in background mode).