# importing OpenAI module
import openai
from pprint import pprint

import logging
import time


logging.basicConfig(level=logging.INFO, format="%(asctime)s ==> at line %(lineno)d --> %(message)s", datefmt="%m-%d %H:%M:%S")


class Script:

    def __init__(self, key,video_title):
        openai.api_key = key
        self.video_title =video_title

    def create_script(self):

        logging.info("Generating Script")

        st = time.time()

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are an intelligent content writer"},
                {"role": "user", "content": f"Generate a script for a video called '{self.video_title} in 100 second' stepwise"},
                {"role": "user", "content": "Separate each step with '**' before each step"},
                {"role": "system", "content": "Generate some code snippets for each step enclosed in '```' "},
                {"role": "system", "content": 'Make sure that the theoretical explanation in each step is enclosed in '
                                              'double Quotations(") '},
                {"role": "system", "content": "When you are Quoting Something, use single quotations(')"}
            ],
            max_tokens=1000
        )

        script = response['choices'][0]['message']['content']
        et = time.time()

        logging.info(f"Script Created in {et - st} time")

        # saving the script locally inside a txt file
        with open("script1", "w") as file:
            file.write(script)
            logging.info(f"script saved in {file.name} file")

        return script


    def retrive_script(self):

        with open("script4") as file:
            script = file.read()

        return script



