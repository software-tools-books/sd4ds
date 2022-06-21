from oop_base import RegexBase

class RegexLit(RegexBase):
    def __init__(self, chars):
        super().__init__()
        self.chars = chars

    def _match(self, text, start):
        return None
