import os
from abc import ABC, abstractmethod
import pandas as pd
from io import StringIO

class BaseParser():

    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
        self.file_ext = os.path.splitext(filename)[1].lower()
    
    def parsable(self):
        return self.file_ext == '.rtf'
    
    @abstractmethod
    def parse(self):
        pass


class FM24Parser(BaseParser):
    ATTRIBUTE_MAPS = {
        'name': 'name',
        'cro': 'crossing',
        'dri': 'dribbling',
        'fin': 'finishing',
        'fir': 'first_touch',
        'fre': 'free_kick_taking',
        'hea': 'heading',
        'lon': 'long_shots',
        'l th': 'long_throws',
        'mar': 'marking',
        'pas': 'passing',
        'pen': 'penalty_taking',
        'tck': 'tackling',
        'tec': 'technique',
        'cor': 'corners',
        'agg': 'aggression',
        'ant': 'anticipation',
        'bra': 'bravery',
        'cmp': 'composure',
        'cnt': 'concentration',
        'dec': 'decisions',
        'det': 'determination',
        'fla': 'flair',
        'ldr': 'leadership',
        'otb': 'off_the_ball',
        'pos': 'positioning',
        'tea': 'teamwork',
        'vis': 'vision',
        'wor': 'work_rate',
        'acc': 'acceleration',
        'agi': 'agility',
        'bal': 'balance',
        'jum': 'jumping_reach',
        'nat': 'natural_fitness',
        'pac': 'pace',
        'sta': 'stamina',
        'str': 'strength',
        'aer': 'aerial_reach',
        'cmd': 'command_of_area',
        'com': 'communication',
        'ecc': 'eccentricity',
        'han': 'handling',
        'kic': 'kicking',
        '1v1': 'one_on_ones',
        'pun': 'punching_tendency',
        'ref': 'reflexes',
        'tro': 'rushing_out_tendency',
        'thr': 'throwing',
    }

    def __init__(self, path, filename, delimiter="|"):
        super().__init__(path, filename)
        self.delimiter = delimiter

    def parse(self):
        with open(self.path, 'rb') as file:
            content = file.read()

        try:
            content_str = content.decode('utf-8')
        except UnicodeDecodeError:
            content_str = content.decode('latin-1')

        lines = []
        for line in content_str.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if set(stripped) <= set("|- "):
                continue
            lines.append(line)

        clean_content = "\n".join(lines)
        df = pd.read_csv(StringIO(clean_content), delimiter=self.delimiter, skipinitialspace=True)

        cols_to_drop = [col for col in df.columns if str(col).strip() == "" or str(col).startswith('Unnamed')]
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop, errors='ignore')

        df.columns = df.columns.str.strip().str.lower()
        df = df.rename(columns={k: v for k, v in self.ATTRIBUTE_MAPS.items() if k in df.columns})
        for column in df.columns:
            if pd.api.types.is_string_dtype(df[column].dtype):
                df[column] = df[column].map(lambda x: x.strip() if isinstance(x, str) else x)
        return df
