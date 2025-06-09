from collections import Counter
from stemmer import stem
import re

pattern = re.compile(r'[^а-яa-z0-9]', re.IGNORECASE)


class Document:
    def __init__(self, filename: str, id: int):
        self.filename: str = filename
        self.id = id
        self.title = ""
        self.term_frequencies = Counter()
        self.update_title()
        self.analyze()

    def update_title(self, chunk_size=2**7):
        with open(self.filename, 'r', encoding='utf-8') as file:
            chunk = file.read(chunk_size)
            self.title = f"{chunk}..."

    def read(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                for word in line.split():
                    cleaned_word = pattern.sub('', word.lower().strip())
                    if cleaned_word:
                        yield cleaned_word

    def analyze(self):
        for word in self.read():
            stemmed_word = stem(word)
            if stemmed_word is None:
                continue

            self.term_frequencies[stemmed_word] += 1

    def term_frequency(self, term: str):
        return self.term_frequencies.get(term, 0)

    def __str__(self):
        return f"[{self.id} | {self.filename}] {self.title}"

    def __repr__(self):
        return f"Document(id={self.id}, title='{self.title}', filename='{self.filename}')"
