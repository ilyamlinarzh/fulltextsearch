import snowballstemmer
import re
from nltk.corpus import stopwords

pattern = re.compile(r'[^а-яa-z0-9]', re.IGNORECASE)
en_stopwords = set(stopwords.words('english'))
ru_stopwords = set(stopwords.words('russian'))

stemmer_ru = snowballstemmer.stemmer('russian')
stemmer_en = snowballstemmer.stemmer('english')

CYRILLIC_RE = re.compile('[а-яА-ЯёЁ]')
LATIN_RE = re.compile('[a-zA-Z]')


def stem(word: str) -> str | None:
    if CYRILLIC_RE.search(word):
        if word in ru_stopwords:
            return None

        return stemmer_ru.stemWord(word)

    elif LATIN_RE.search(word):
        if word in en_stopwords:
            return None

        return stemmer_en.stemWord(word)
    else:
        return None
