from formats import JsonSerializer, XmlSerializer


class FormatFactory:
    def __init__(self):
        self.formats = {
            'json': JsonSerializer(),
            'xml': XmlSerializer(),
        }

    def set_format(self, name, value):
        self.formats.setdefault(name, value)

    def get_format(self, name):
        format = self.formats.get(name)
        if not format:
            return NotImplemented
        else:
            return format
