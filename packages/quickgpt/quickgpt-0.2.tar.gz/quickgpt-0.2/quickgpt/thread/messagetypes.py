class Message:
    def __init__(self, content):
        self.content = content

    @property
    def role(self):
        return self.__class__.__name__.lower()

    @property
    def obj(self):
        return {
            "role": self.role,
            "content": self.content
        }

    def __str__(self):
        return "<%s> %s" % (self.role, self.content)

class System(Message): pass
class User(Message): pass
class Assistant(Message): pass
