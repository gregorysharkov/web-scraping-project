'''how we store articles'''
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

        file_name = output_path / f'{self.site} - {self.title}.txt'
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(self.text)
