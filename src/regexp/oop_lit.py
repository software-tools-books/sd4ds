from oop_base import RegexBase

class RegexLit(RegexBase):
    def __init__(self, chars):
        super().__init__()
        self.chars = chars

    def _match(self, text, start):
        nextIndex = start + len(self.chars)
        if nextIndex > len(text):
            return None
        if text[start:nextIndex] != self.chars:
            return None
        return nextIndex
