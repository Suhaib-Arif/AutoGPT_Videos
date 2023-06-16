import os

GPTKEY = os.environ["GPTKEY"]
GIPHYAPIKEY = os.environ["GIPHYAPIKEY"]
ELEVENLABSAPIKEY = os.environ["ELEVENLABSKEY"]

ELEVENLABS_VOICE_ID = os.environ["ELEVENLABSVOICEID"]

from scriptmanager import Script
from snippetmanager import SnippetScraper
from gifmanager import GIPHY
from audiomanager import Voiceover
from assetsmanager import AssetHandler

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s ==> at line %(lineno)d --> %(message)s", datefmt="%m-%d %H:%M:%S")

# importing movie py to handle Image, Audio and Video clips
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip

# Creating the absolute File path for all directories
handler = AssetHandler()

logging.info("Checking if the folders are empty")
handler.check_directory()


# calling ChatGPT to generate Script for video
video_title= "Java"
aiscript = Script(GPTKEY,video_title)

logging.info("Configuring Download options")
snippet = SnippetScraper()

logging.info("Setting up VoiceOver")
audio_obj = Voiceover(ELEVENLABS_VOICE_ID, ELEVENLABSAPIKEY)

logging.info("Creating a session with Giphy")
gif_obj = GIPHY(GIPHYAPIKEY)
# Generate a script using CHATGPT
script = aiscript.create_script()

# Retriving an already generated script
# script = aiscript.retrive_script()

# a Variable used for halting the program until a file is added
image_count = 0
clips = list()

# loop through the script stepwise to generate visual content and images for the video
for i, item in enumerate(script.split("**Step")):

    assets = {}

    item = "Step" + item.replace("**","")

    # If the step contains a code snippet
    if "```" in item:

        logging.info(f"Producing Code Snippet layout: {i}")

        item_list = item.split("```")

        # separating the code snippets from the regular text and the text header
        code_snippet = item_list[1]
        text = item_list[0]
        head = text.split('"')[0]

        # Creating Code Snippets
        image_directory = snippet.obtainsnippet(head, code_snippet, image_count, i)

        # Creating an image Clip object from the filepath
        image_asset = ImageClip(image_directory)

        logging.info("Image added to assets list")
        assets["image_asset"] = image_asset

        image_count += 1

    # if the step does not contain a code snippet
    else:
        text_list = item.split('"')

        # obtain the heading and the text region
        head = text_list[0]
        text = text_list[-1]

    logging.info("Requesting Gifs from giphy")
    gif_directory = gif_obj.obtain_gif(head, i)


    if gif_directory is not None:
        gif_asset = VideoFileClip(gif_directory)
        assets["gif_asset"]=gif_asset
        logging.info("Gif Added to assets list")


    # Using ELeven labs API to obtain the audio files
    audio_file_dir = audio_obj.obtain_audio(text,i)
    audio_asset = AudioFileClip(audio_file_dir)


    clip = handler.combine_assets(assets,audio_asset, i)
    clips.append(clip)

handler.generate_video(clips)
