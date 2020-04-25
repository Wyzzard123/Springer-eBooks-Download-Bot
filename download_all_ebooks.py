import time
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

# USELESS
def stay_on_correct_tab(driver, link, text_pattern="/book/"):
    """
    Note: This is borrowed from some other code of mine. It does not fully function. It ensures that we are on the
    right tab by checking for /book/ in the current url. Though it works in getting rid of wrong windows, it does NOT
    get rid of the stray dialog boxes that sometimes appear, making this function useless for this code. Nonetheless,
    keeping it in here in case it can be improved.

    :param driver:          Selenium webdriver
    :type driver:           Driver
    :param link:            Link we are supposed to be on but are not
    :type link:             str
    :param text_pattern:    A pattern which should appear in the url. Sometimes, the code accidentally opens up a link
                            with /content/ instead of /book/.
    :type text_pattern:     str
    :return:                Returns True if we are on the right tab. Otherwise, return False.
    :rtype:                 bool
    """
    print("Checking if on correct tab")
    if text_pattern not in driver.current_url:
        print("On wrong tab")
        current_window = driver.current_window_handle

        other_window_handles = [window_handle for window_handle in driver.window_handles if
                                window_handle != current_window]

        if other_window_handles:
            # Close window and switch
            driver.close()
            if len(other_window_handles) == 1:
                driver.switch_to.window(other_window_handles[0])
            else:
                last_window_handle = other_window_handles[-1]
                for window_handle in other_window_handles:
                    driver.switch_to.window(window_handle)
                    if text_pattern not in driver.current_url and window_handle != last_window_handle:
                        driver.close()
                        continue
                    elif text_pattern not in driver.current_url and window_handle == last_window_handle:
                        driver.get(text_pattern)
                        driver.switch_to.window(window_handle)
                    elif text_pattern in driver.current_url and window_handle == last_window_handle:
                        break
        elif not other_window_handles:
            # If no other windows, renavigate to the faucet link and switch to the right windoow
            driver.get(link)
            driver.switch_to.window(current_window)
        # Return False if we were on the wrong tab
        return False
    else:
        # Return True if we are on the right tab
        print("On correct tab")
        # driver.switch_to.window(driver.current_window_handle)
        current_window = driver.current_window_handle

        other_window_handles = [window_handle for window_handle in driver.window_handles if
                                window_handle != current_window]

        print("Other windows:", other_window_handles)

        if other_window_handles:
            for window_handle in other_window_handles:
                driver.switch_to.window(window_handle)
                driver.close()
            driver.switch_to.window(current_window)
            return False

        driver.switch_to.window(current_window)
        return True


def download_all_ebooks(driver, txt_file="Springer All Free Ebooks.txt", delay=2, background=True, folder=None):
    """
    Example Usage:            python download_all_ebooks.py [delay] [reference file name with quotes]

    Downloads all ebooks from Springer from the passed in txt file. This must be run slowly. Otherwise, the pyautogui
    components are activated too quickly and do not sync with the Selenium Webdriver actions. If you wish to increase
    the delay from the current 2 seconds, add an argument when using the python script.

    Example:            python download_all_ebooks.py 10

    The above example adds a delay of 10 seconds between action.

    Note that there are 400 books. At the maximum recommended speed of delay=2, this means that the bot will take around
    66 minutes to complete. Leave the bot on during lunch.

    You can also optionally add a second argument if you are going to use a separate file.

    Example:            python download_all_ebooks.py 2 "Springer All Free Ebooks after failure.txt"

    There are some books in the E-books PDF which are not actually free which I have removed. These are:

    - https://link.springer.com/book/10.1007%2F978-3-030-19128-3 (Literature and Medicine)
    - https://link.springer.com/book/10.1007%2F978-3-319-32185-1 (Business Statistics for Competitive Advantage with
      Excel 2016)

    :param driver:      A Selenium webdriver. This is passed from outside the function to prevent the webdriver from
                        closing before all files have finished downloading. This means that the browser window must be
                        closed manually.
    :type driver:       webdriver
    :param folder:      The path to the download folder. If none, this is not set and the system default is used.
    :type folder:       str
    :param background:  If False, this uses PyAutoGUI and operates in the foreground. In other words, one cannot use
                        his computer while operating the bot.

                        If True, this only uses Selenium and operates in the background.
    :type background:   bool
    :param delay:       Passed in as a command line argument. Delay in seconds. If not passed in, defaults to 2.
                        Any lower than 2 and the program will likely break when not running in background mode.

                        Usage: python download_all_ebooks.py [delay/s]
                        If delay is not numeric, the code will raise an error.

    :type delay:        int or float
    :param txt_file:    A txt file containing links to all the ebooks line by line. This can be passed in as a second
                        argument in the command line if not using the default file. For example, if you have downloaded
                        up to a certain point and wish to continue, you can delete the links which have already been
                        downloaded and replace the file name.

                        Be sure to use quotes to surround the txt_file name when calling this from the command line.
    :type txt_file:     str
    :return:            None
    :rtype:             None
    """

    with open(txt_file, 'r') as f:
        # See https://stackoverflow.com/questions/43149534/selenium-webdriver-how-to-download-a-pdf-file-with-python
        if background:
            print("Running in background mode")
        # DEPRECATED
        else:
            print("Running in foreground mode (DEPRECATED)")
        driver.implicitly_wait(10)

        for line_no, link in enumerate(f):
            driver.get(link)
            print(line_no, link)
            print("Title:", driver.title)
            print("Current URL:", driver.current_url)
            if background:
                try:
                    download_button = driver.find_element_by_css_selector("a[title='Download this book in PDF format']")
                    # Move/Scroll to download button first to avoid click intercept errors
                    ActionChains(driver).move_to_element(download_button).perform()
                    download_button.click()
                    time.sleep(delay)

                except NoSuchElementException as e:
                    print("NoSuchElementException:", e)
                    print("Book might not be downloadable for free:", driver.title)
                    print("Moving on")
                    continue

            # DEPRECATED
            elif not background:
                # Switch to correct tab
                # TODO - This works but the file dialog doesn't go away or get handled. Handle this.
                stay_on_correct_tab(driver, link)
                # if "/book/" not in driver.current_url:
                #     print("Driver in wrong tab. Switching back.")
                #     # Switch back to active tab in case we accidentally opened a new tab
                #     driver.switch_to.window(driver.current_window_handle)

                try:
                    download_button = driver.find_element_by_css_selector("a[title='Download this book in PDF format']")
                    # Sleep to make sure all the context_click options appear
                    time.sleep(delay)
                    # Move/Scroll to download button first to avoid click intercept errors
                    ActionChains(driver).move_to_element(download_button).perform()
                    # Right click the "Download book PDF" button
                    ActionChains(driver).context_click(download_button).perform()

                    # Give time for context menu to appear before pressing down
                    time.sleep(delay)

                    for _ in range(4):
                        # Press down until we're at "Save Link As"
                        pyautogui.press('down')

                    # Sleep to ensure the next press for "enter" registers for the context menu, not the Download Button
                    # Clicking the Download Button instead will cause us to open a new window
                    time.sleep(delay)

                    # Press Enter in the context menu to save link as
                    pyautogui.press('enter')
                    time.sleep(delay)

                    # Press enter again to save to the default folder
                    pyautogui.press('enter')
                except NoSuchElementException as e:
                    print("NoSuchElementException:", e)
                    print("Book might not be downloadable for free:", driver.title)
                    print("Moving on")
                    continue

        # Allow time to leave webdriver open to download the last file
        time.sleep(120)


if __name__ == "__main__":
    import sys
    import stat
    import os
    from sys import platform

    # Parsing command line arguments.
    if len(sys.argv) > 1:
        folder = sys.argv[1]
        if not os.path.isdir(folder):
            raise Exception("Usage: python download_all_ebooks.py [download folder] [txt_file] [delay/s] [background]\n"
                            "The first argument should a directory for your downloaded files.")
    else:
        folder = None
    print("Download Folder:", folder)

    if len(sys.argv) > 2:
        txt_file = sys.argv[2]
        if not os.path.isfile(txt_file):
            raise Exception("Usage: python download_all_ebooks.py [download folder] [txt_file] [delay/s] [background]\n"
                            "The second argument should be the txt_file to reference. The provided file does not exist. "
                            "By default this is 'Springer All Free Ebooks.txt'."
                            )
    else:
        txt_file = "Springer All Free Ebooks.txt"
        if not os.path.isfile(txt_file):
            raise Exception("Did you delete/rename/move the file 'Springer All Free Ebooks.txt'?")
    print("Reference Text File:", txt_file)

    if len(sys.argv) > 3:
        if not sys.argv[3].isnumeric():
            raise ValueError("Usage: python download_all_ebooks.py [download folder] [txt_file] [delay/s] [background]\n"
                             "The third argument should be a numeric value with the delay in seconds. "
                             "By default this is 2.")
        delay = int(sys.argv[3])
    else:
        delay = 2
    print("Delay:", delay)

    if len(sys.argv) > 4:
        true_values = ["true", "t"]
        false_values = ["false", "f"]
        if sys.argv[4].lower() in true_values:
            background = True
        elif sys.argv[4].lower() in false_values:
            background = False
        else:
            raise ValueError("Usage: python download_all_ebooks.py [download folder] [txt_file] [delay/s] [background]\n"
                             "The fourth argument should be true/t or false/f, and indicates whether the program runs"
                             "in the background or not. By default this is True.")
    else:
        background = True
    print("Running in Background:", background)

    # Setting Driver options

    # Opening driver outside main function to allow it to stay open after downloading, in case not every file is
    # done downloading after clicking the last download button.
    if platform == "win32" or platform == "cygwin":
        driver_location = "webdrivers/windows/chromedriver.exe"
        system_os = "Windows"
    elif platform == "darwin":
        driver_location = "webdrivers/mac/chromedriver"
        # Set to executable by owner (This already works)
        os.chmod(driver_location, stat.S_IEXEC)

        # Set to read write executable by all (If the above permissions do not work, uncomment the line below this one)
        # os.chmod(driver_location, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        system_os = "Mac OS X"
    elif platform == "linux" or platform == "linux2":
        driver_location = "webdrivers/linux/chromedriver"
        # Set to executable by owner
        os.chmod(driver_location, stat.S_IEXEC)

        # Set to read write executable by all (If the above permissions do not work, uncomment the line below this one)
        # os.chmod(driver_location, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        system_os = "Linux"
    print("OS:", system_os)
    print("Driver Location:", driver_location)
    options = webdriver.ChromeOptions()

    profile = {
        "plugins.plugins_list":
        # Disable Chrome's PDF Viewer
            [{"enabled": False, "name": "Chrome PDF Viewer"}],
        "download.extensions_to_open": "applications/pdf",
        # To auto download the file
        "download.prompt_for_download": False,
        # "download.directory_upgrade": True,
        # It will not show PDF directly in chrome
        "plugins.always_open_pdf_externally": True,
    }
    if folder:
        if os.path.isdir(folder):
            profile.update({
                "download.default_directory": folder
            })
        else:
            raise Exception("Download folder provided does not exist.")

    options.add_experimental_option('prefs', profile)
    driver = webdriver.Chrome(driver_location, chrome_options=options)

    # Maximize window to prevent click intercepted errors (because the button is not visible)
    driver.maximize_window()

    # Activating function

    download_all_ebooks(driver=driver, folder=folder, txt_file=txt_file, delay=delay, background=background)
