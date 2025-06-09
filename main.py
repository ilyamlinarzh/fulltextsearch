from index import Index
from document import Document
from pathlib import Path
import time

articles_path = "./articles"


def iter_documents_names():
    folder_path = Path(articles_path)
    i = 0
    for file in folder_path.glob('*.txt'):  # Только .txt файлы
        yield i, file.name
        i += 1


def iter_documents():
    for id, name in iter_documents_names():
        doc = Document(filename=f"./articles/{name}", id=id)
        yield doc


def build_index():
    index = Index()
    for document in iter_documents():
        index.add_document(document)

    return index


def main():
    index = build_index()

    while True:
        q = input("Запрос: ")
        start = time.time()
        res = index.search(q)
        end = time.time()
        print(f"<{end-start:.6f} s.> Результат поиска: \n")
        for doc in res:
            print(f'[{doc[1]:.2f}]', str(doc[0]))
        print("\n")


if __name__ == "__main__":
    main()
