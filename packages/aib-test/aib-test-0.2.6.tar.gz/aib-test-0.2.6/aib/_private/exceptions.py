class InitError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return "Aibeem init fail:" + self.msg


class NotInitiated(Exception):
    def __str__(self):
        return "Aibeem client isn't initiated yet"

