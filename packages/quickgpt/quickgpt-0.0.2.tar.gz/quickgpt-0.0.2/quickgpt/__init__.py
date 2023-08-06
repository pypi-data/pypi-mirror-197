from quickgpt.thread import Thread

import os

class QuickGPT:
    def __init__(self, api_key=None):
        if not api_key:
            api_key = os.environ.get("OPENAI_API_KEY")

        self.api_key = api_key

    def new_thread(self):
        thread = Thread(self)

        return thread
