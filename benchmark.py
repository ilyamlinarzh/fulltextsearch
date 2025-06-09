from main import build_index
from collections import Counter
from index import Index
import time
import numpy as np
from sys import getsizeof


def time_measure(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, end - start

class Benchmark:
    def __init__(self, index: Index, query_sizes: list[int], tests_count: int = 100):
        counter = Counter()
        for term, d_ids in index.index.items():
            counter[term] += len(d_ids)

        self.top_keys: list[str] = [item[0] for item in counter.most_common(max(query_sizes))]
        self.index = index
        self.q_sizes = query_sizes
        self.tests_count = tests_count

    @staticmethod
    def calculate_stats(numbers: list[float | int]):
        np_numbers = np.array(numbers)

        stats = {
            'mean': float(np.mean(np_numbers)),
            'median': float(np.median(np_numbers)),
            'p95': float(np.percentile(np_numbers, 95))
        }

        return stats

    def index_stats(self):
        terms = len(self.index.index)
        includes = 0
        for term, d_ids in self.index.index.items():
            includes += len(d_ids)

        avg_ids_in_term = includes / terms

        print(f"Ключевых слов загружено: {terms}")
        print(f"Среднее количество записей в ключевом слове: {avg_ids_in_term:.1f}")
        print(f"Размер индекса: {(getsizeof(self.index.index) + getsizeof(self.index.documents))/1024/1024:.6f} Мб.")

    def __call__(self):
        results = {}
        for q_size in self.q_sizes:
            terms = self.top_keys[:q_size]
            print(terms)

            time_results = []
            for _ in range(self.tests_count):
                res, time_res = time_measure(self.index.search_by_terms, terms)
                time_results.append(time_res)

            results[q_size] = self.calculate_stats(time_results)

        for q_size, stats_res in results.items():
            print(f"Длина запроса {q_size}:")
            print(f"Среднее: {stats_res['mean']:.6f} s.")
            print(f"Медиана: {stats_res['median']:.6f} s.")
            print(f"95-ый перцентиль: {stats_res['p95']:.6f} s.")
            print("\n")


def main():
    index, time_res = time_measure(build_index)
    print(f"Индекс построен за: {time_res:.6f} сек.")
    benchmark = Benchmark(index=index, query_sizes=[2, 3, 5, 7, 9], tests_count=1000)
    benchmark.index_stats()
    benchmark()


if __name__ == "__main__":
    main()
