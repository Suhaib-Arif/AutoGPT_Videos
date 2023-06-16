# importing selenium to create visuals
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import sys
import time
import os
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s ==> at line %(lineno)d --> %(message)s", datefmt="%m-%d "
                                                                                                             "%H:%M:%S")
from assetsmanager import AssetHandler

class SnippetScraper:

    def __init__(self):
        # Configuring download options such that the Downloaded files will be stored in an images folder locally
        self.handler = AssetHandler()
        self.images_dir = self.handler.images_dir

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_experimental_option(
            "prefs", {
                "download.default_directory": self.images_dir,
                "download.prompt_for_download": False,
            }
        )

        # creating driver object and a wait variable to create visuals for snippets
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)


    def obtainsnippet(self, head, code_snippet, image_count, index):

        # opening the webpage to create visuals
        self.driver.get("https://ray.so/")

        # waiting until the web page loads
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ControlContainer_control__GLDPu']/button")))

        # Accessing the text area and header
        header = self.driver.find_element(By.TAG_NAME, "input")
        textarea = self.driver.find_element(By.TAG_NAME, "textarea")

        # typing the step name into header
        header.send_keys(head)

        # removing the placeholder code and writing our desired code snippets
        textarea.clear()
        textarea.send_keys(code_snippet)
        textarea.send_keys(Keys.BACKSPACE)

        time.sleep(2)
        # Finding the export button to download the image and waiting for the file to complete download
        self.driver.find_element(By.XPATH, "//div[@class='ExportButton_container__KRFXe']/button").click()


        # Waiting until the file is added to the directory
        while self.handler.check_directory_length(self.images_dir) == image_count:
            logging.info("Waiting for file to download")
            time.sleep(2)


        # Creating a custom filename based on the index
        filename = self.handler.combine_directory(self.images_dir, f"{index}snippet.png")

        # accessing the latest file created and Creating its absolute file path
        unnamed_added_file = os.listdir("images")[-1]
        unnamed_added_file = os.path.join(self.images_dir, unnamed_added_file)

        # Renaming the accessed file to the custom file name
        os.rename(unnamed_added_file, filename)

        # Displaying the filename into the console
        added_file = os.listdir("images")[-1]
        logging.info(f"file added --> {added_file}")

        return filename
