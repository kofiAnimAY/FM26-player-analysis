import tempfile
from app.apis.parser import FM24Parser


def test_fm24_parser_strips_separator_rows_and_normalizes_headers():
    sample = """
| Name | Cro | Dri |
| --- | --- | --- |
|  Kylian Mbappé  | 12 | 18 |
| Ousmane Dembélé | 16 | 18 |
"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.rtf', delete=False, encoding='utf-8') as tmp:
        tmp.write(sample)
        tmp.flush()
        parser = FM24Parser(tmp.name, tmp.name, delimiter='|')
        df = parser.parse()

    assert 'name' in df.columns
    assert 'crossing' in df.columns
    assert 'dribbling' in df.columns
    assert df.shape[0] == 2
    assert df.loc[0, 'name'] == 'Kylian Mbappé'
    assert int(df.loc[1, 'crossing']) == 16
    assert int(df.loc[1, 'dribbling']) == 18
