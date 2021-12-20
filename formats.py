from abc import ABC, abstractmethod
import json

from dicttoxml import dicttoxml


class UploadFormat(ABC):
    def dump(self, obj, fp):
        with open(fp, "w") as fp:
            fp.write(self.dumps(obj))

    @abstractmethod
    def dumps(self, obj):
        pass


class LoadFormat(ABC):
    def load(self, fp):
        with open(fp, "r") as fp:
            return self.loads(fp.read())

    @abstractmethod
    def loads(self, obj):
        pass


class JsonSerializer(UploadFormat, LoadFormat):
    def dumps(self, obj):
        return json.dumps(obj)

    def loads(self, obj):
        return json.loads(obj)


class XmlSerializer(UploadFormat):
    def dumps(self, obj):
        xml = dicttoxml(obj, custom_root='rooms', attr_type=False, item_func=lambda x: x[:-1])
        xml_decode = xml.decode()
        return xml_decode
