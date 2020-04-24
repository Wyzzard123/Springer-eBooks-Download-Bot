import time

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


def download_all_ebooks(txt_file="Springer All Free Ebooks.txt", delay=2):
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

    :param delay:       Passed in as a command line argument. Delay in seconds. If not passed in, defaults to 2.
                        Any lower than 2 and the program will likely break.

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
        driver = webdriver.Chrome("webdrivers/windows/chromedriver.exe")
        driver.implicitly_wait(10)

        for line_no, link in enumerate(f):
            driver.get(link)
            print(line_no, link)
            print("Current URL:", driver.current_url)

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
        time.sleep(60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if not sys.argv[1].isnumeric():
            raise ValueError("Usage: python download_all_ebooks.py [delay/s]")
        delay = int(sys.argv[1])
    else:
        delay = 2
    print("Delay:", delay)

    if len(sys.argv) > 2:
        txt_file = sys.argv[2]
    else:
        txt_file = "Springer All Free Ebooks.txt"
    print("Reference Text File:", txt_file)
    download_all_ebooks(txt_file=txt_file, delay=delay)
