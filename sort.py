MIN_MERGE = 32

def calc_min_run(n):
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


def insertion_sort(arr, left, right, selector=None, reverse=False):
    if selector is None:
        cmp = lambda x, y: x > y if reverse else x < y
    else:
        cmp = lambda x, y: selector(x) > selector(y) if reverse else selector(x) < selector(y)

    for i in range(left + 1, right + 1):
        j = i
        while j > left and cmp(arr[j], arr[j - 1]):
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1


def merge(arr, l, m, r, selector=None, reverse=False):
    len1, len2 = m - l + 1, r - m
    left = arr[l:m + 1]
    right = arr[m + 1:r + 1]

    if selector is None:
        cmp = lambda x, y: x > y if reverse else x <= y
    else:
        cmp = lambda x, y: selector(x) > selector(y) if reverse else selector(x) <= selector(y)

    i = j = 0
    k = l

    while i < len1 and j < len2:
        if cmp(left[i], right[j]):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len2:
        arr[k] = right[j]
        j += 1
        k += 1


def timsort(arr, selector=None, reverse=False):
    n = len(arr)
    if n < 2:
        return

    min_run = calc_min_run(n)

    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(arr, start, end, selector, reverse)

    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:
                merge(arr, left, mid, right, selector, reverse)
        size *= 2
