# importing requests to make API calls to GIPHY API and ElevenLabs
import requests

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s ==> at line %(lineno)d --> %(message)s",
                    datefmt="%m-%d %H:%M:%S")

from assetsmanager import AssetHandler
import sys


class GIPHY:

    def __init__(self, GIPHYAPIKEY):
        self.handler = AssetHandler()
        self.gif_dir = self.handler.gif_dir
        self.session = requests.session()
        self.gif_endpoint = "https://api.giphy.com/v1/gifs/search"
        self.GIPHYAPIKEY = GIPHYAPIKEY

    def obtain_gif(self, head, index):

        giphy_response = self.session.get(url=self.gif_endpoint,
                                          params={"api_key": self.GIPHYAPIKEY, "q": head.split(":")[-1]})

        logging.info(f"Giphy Status code {giphy_response.status_code}")

        # if the response is successful
        if giphy_response.status_code == 200:
            logging.info(f"Gif No {index} acquired")

            # Acquiring the URL
            try:
                gif_url = giphy_response.json()['data'][-1]['images']['original']['url']

            except IndexError:
                logging.info("No gif found")
                return None

            else:
                # Downloading the url as gif
                logging.info("Downloading gif locally")
                giphy_content = requests.get(gif_url)
                gif_directory = self.handler.combine_directory(self.gif_dir, f"{index}gif.gif")
                with open(gif_directory, "wb") as gif_file:
                    gif_file.write(giphy_content.content)
                    added_gif = self.handler.get_latest_file(self.gif_dir)
                    logging.info(f"Gif: {added_gif} saved locally")

                return gif_directory
        else:
            giphy_error_msg = giphy_response.json()['meta']['msg']
            logging.error(f"Giphy error: {giphy_error_msg}")
            sys.exit()
