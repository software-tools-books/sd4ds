class RegexBase:
    def match(self, text):
        for i in range(len(text)):
            if this._match(text, i):
                return True
        return False

    def _match(self, text, start):
        raise NotImplementedError("derived classes must override '_match'")
