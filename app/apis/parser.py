import os
from abc import ABC, abstractmethod
import pandas as pd
from io import StringIO

class BaseParser():

    def __init__(self, path, filename):

        self.file = open(path,'rb')
        self.filename = filename
        self.file_ext = os.path.splitext(filename)[1].lower()
    
    @classmethod
    def parsable(self):
        return self.file_ext == '.rtf'
    
    @abstractmethod
    def parse(self):
        pass


class FM24Parser(BaseParser):
    ATTRIBUTE_MAPS = {

    }
    def __init__(self,path,filename,delimiter="|"):
        super().__init__(path,filename)
        self.delimiter=delimiter

    def parse(self):
        content = self.file.read()

        try:
            content_str = content.decode('utf-8')
        except UnicodeDecodeError:
            content_str = content.decode('latin-1')

        df = pd.read_csv(StringIO(content_str), delimiter=self.delimiter)

        return df
