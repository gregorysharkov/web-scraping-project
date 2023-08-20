'''how we store articles'''
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Article:
    '''class is responsible for storing and writing article information'''
    title: str
    text: str
    site: str

    def save(self, output_path: Path) -> None:
        '''saves given article in the given path'''
        # make sure that the path exists
        output_path.mkdir(parents=True, exist_ok=True)

        # clean article name
        clean_file_name = re.sub(r'[^a-zA-Z0-9]', '_', self.title)
        clean_file_name = re.sub('_{2,}', '_', clean_file_name)

        # save
        file_name = output_path / f'{self.site} - {clean_file_name}.txt'
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(self.text)
