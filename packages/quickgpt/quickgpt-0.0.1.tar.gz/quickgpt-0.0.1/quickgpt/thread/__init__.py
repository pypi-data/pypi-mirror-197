import openai

from quickgpt.thread.messagetypes import *
from quickgpt.thread.response import Response

class Thread:
    def __init__(self, quickgpt):
        self.quickgpt = quickgpt

        openai.api_key = quickgpt.api_key

        self.thread = []

    def feed(self, *messages):

        for msg in messages:
            assert type(msg) in (System, Assistant, User), \
                "Must be of type System, Assistant, User"

            self.thread.append(msg)

    def run(self):
        messages = [ msg.obj for msg in self.thread ]

        response_obj = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        response = Response(response_obj)

        return response
