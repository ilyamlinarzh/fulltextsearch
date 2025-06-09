from document import Document
import math
from stemmer import stem
from sort import timsort


class Index:
    def __init__(self):
        self.index: dict[str, set] = {}
        self.documents: dict[int, Document] = {}

    def add_document(self, doc: Document):
        if doc.id not in self.documents:
            self.documents[doc.id] = doc

        for term, _ in doc.term_frequencies.items():
            if term not in self.index:
                self.index[term] = set()
            self.index[term].add(doc.id)

    def document_frequency(self, term: str):
        return len(self.index.get(term, set()))

    def inv_document_frequency(self, term: str):
        return math.log(len(self.documents) / self.document_frequency(term))

    @staticmethod
    def query_to_terms(q: str):
        terms = []
        for word in q.split():
            term = stem(word)
            if term is not None:
                terms.append(term)
        return terms

    def _get_terms_sets(self, terms: list[str]):
        return [self.index.get(term, set()) for term in terms]

    def search(self, q: str):
        terms = self.query_to_terms(q)
        if len(terms) == 0:
            return []

        result = self._get_terms_sets(terms)
        documents = [self.documents[d_id] for d_id in set.intersection(*result)]

        return self.rank(documents, terms)

    def search_by_terms(self, terms: list[str]):
        if len(terms) == 0:
            return []

        result = self._get_terms_sets(terms)
        documents = [self.documents[d_id] for d_id in set.intersection(*result)]

        return self.rank(documents, terms)

    def rank(self, documents: list[Document], query_terms: list[str]):
        results = []
        if not documents:
            return results

        for document in documents:
            score = 0.0
            for term in query_terms:
                tf = document.term_frequency(term)
                idf = self.inv_document_frequency(term)
                score += tf * idf
            results.append((document, score))

        timsort(results, selector=lambda x: x[1], reverse=True)
        return results
