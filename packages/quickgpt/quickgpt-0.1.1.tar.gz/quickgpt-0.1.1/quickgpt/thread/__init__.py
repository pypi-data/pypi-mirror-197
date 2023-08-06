import openai

from quickgpt.thread.messagetypes import *
from quickgpt.thread.response import Response

class Thread:
    def __init__(self, quickgpt):
        self.quickgpt = quickgpt

        openai.api_key = quickgpt.api_key

        self.thread = []

    def feed(self, *messages):

        try:
            # Check if the first argument is a list, and then make it the parent
            iter(messages[0])
            messages = messages[0]
        except TypeError:
            pass

        for msg in messages:
            assert type(msg) in (System, Assistant, User, Response, dict), \
                "Must be of type System, Assistant, User, Response, or dict"

            if type(msg) == Response:
                msg = Assistant(msg.message)

            # Convert a boring old dict message to a pretty object message
            if type(msg) == dict:
                role = msg["role"]
                content = msg["content"]

                if role == "system":
                    msg = System(content)
                elif role == "assistant":
                    msg = Assistant(content)
                elif role == "user":
                    msg = User(content)
                else:
                    raise TypeError("Unknown role '%s'" % role)

            self.thread.append(msg)

    @property
    def messages(self):
        return [ msg.obj for msg in self.thread ]

    def run(self, feed=True):
        """ Executes the current thread and get a response. If `feed` is
        True, it will automatically save the response to the thread. """
        messages = self.messages

        response_obj = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        response = Response(response_obj)

        if feed:
            self.feed(response)

        return response
