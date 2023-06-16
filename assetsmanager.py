import warnings
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s ==> at line %(lineno)d --> %(message)s", datefmt="%m-%d "
                                                                                                             "%H:%M:%S")

from moviepy.editor import concatenate_videoclips

class AssetHandler:

    def __init__(self):
        self.base_dir = os.getcwd()
        self.images_dir = os.path.join(self.base_dir, "images")
        self.gif_dir = os.path.join(self.base_dir, "gifs")
        self.audio_dir = os.path.join(self.base_dir, "audio")

    def check_directory(self):
        if len(os.listdir(self.images_dir)) != 0 and len(os.listdir(self.gif_dir)) != 0 and len(os.listdir(self.audio_dir)) != 0:
            logging.error("Mask sure the images directory is empty")
            sys.exit()

    def combine_directory(self,full_path, filename):
        full_dir = os.path.join(full_path, filename)
        return full_dir

    def get_latest_file(self,directory):
        latest_file = os.listdir(directory)[-1]
        return latest_file

    def check_directory_length(self, directory):
        return len(os.listdir(directory))

    def combine_assets(self, assets, audio, index):

        if len(assets.values()) != 0:

            assetlist = []
            logging.info(f"Creating clip no {index + 1}")

            gif = assets.get("gif_asset")
            image = assets.get("image_asset")

            if gif is not None:
                gif = gif.set_duration(2)
                assetlist.append(gif)
            if image is not None:
                image = image.set_duration(audio.duration)
                assetlist.append(image)

            clip = concatenate_videoclips(assetlist, method="compose")
            clip = clip.set_audio(audio)

            return clip

    def generate_video(self,clips):
        logging.info("Creating the Video")

        clips = [clip for clip in clips if clip != None]

        warnings.filterwarnings("ignore")

        full_video = concatenate_videoclips(clips, method="compose")
        full_video.write_videofile("video/fullvideo3.mp4", fps=50)

