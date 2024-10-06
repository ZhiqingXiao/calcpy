from collections import defaultdict, deque
from copy import copy
import operator
from sys import maxsize


def min_repetend_len(args, allow_frac=True, matcher=None):
    """Get minimum length of repetends.

    Args:
        args (list): List of values as a sequence
        allow_frac (bool): Whether to allow partial repetend at the end of sequence
        matcher (:obj:`callable`, optional): A object to be used to determine whether two values are the same

    Returns:
        int: The minimum length of repetends.

    Examples:
        >>> min_repetend_len([1, 1, 1, 1])
        1
        >>> min_repetend_len([1, 2, 1, 2])
        2
        >>> min_repetend_len([1, 2, 1, 3])
        4
        >>> min_repetend_len([1, 2, 1, 3, 1, 2, 1, 3])
        4
        >>> min_repetend_len([1, 2, 1, 2, 1, 2, 1], allow_frac=False)
        7
    """
    length = len(args)
    matcher = matcher or operator.eq
    for l in range(1, length):  # noqa: E741
        if (not allow_frac) and (length % l > 0):
            continue
        for i in range(length-l):
            if not matcher(args[i], args[i+l]):
                break
        else:
            return l
    return length


def perm(values, cycle):
    """Permutates a list according to cycle notation.

    Args:
        values (list): Sequence to permutate.
        cycle (list): Permutation rule in cyclc notation.

    Returns:
        list: Permutated sequence.

    Examples:
        Permutate a list of strings.
        >>> perm(["a", "b", "c", "d", "e", "f", "g"], [1, 2, 4])
        ['a', 'c', 'e', 'd', 'b', 'f', 'g']

        Permutate a list of integers.
        >>> perm(list(range(6)), [0, 1, 2])
        [1, 2, 0, 3, 4, 5]
    """
    results = copy(values)
    for i, v in enumerate(cycle):
        results[v] = values[cycle[(i+1) % len(cycle)]]
    return results


def swap(values, i=0, j=1):
    """Swap two elements in a list.

    Args:
        values (list): Sequence to permutate.
        i (int): Index of the first element to swap.
        j (int): Index of the second element to swap.

    Returns:
        list: Swapped sequence.

    Examples:
        Swap two elements for a list of strings.
        >>> swap(["a", "b", "c", "d", "e", "f", "g"], 1, 2)
        ['a', 'c', 'b', 'd', 'e', 'f', 'g']

        Swap two elements for a list of integers.
        >>> swap(list(range(6)), 1, 2)
        [0, 2, 1, 3, 4, 5]
    """
    return perm(values, cycle=[i, j])


def A276128(n=maxsize):
    """Generate OEIS sequence A276128

    Args:
        n (int): Length of sequence

    Yields:
        int: Value of the sequence

    Reference:
        https://oeis.org/A276128

    Explanations:
        (Adapted from https://oeis.org/A276128)
        Definition of sequence:
            For a positive integer n, let the single-player game G[n] be as follows:
            x is a number in {0, 1, 2, ..., n}, but unknown to the player.
            The player can guess as many times as he wants to determine the value of x.
            For each guess, the player can propose a possible value c in {0, 1, 2, ..., n},
            but such guess will cost the player c dollars.
            After each guess, the player will get response to show whether c<x, c=x, or c>x.
            A guess strategy will consist a series of guesses to determine x.
            The cost of multiple guesses is defined to be the sum of the cost of each guess.
            The cost of guess strategy is defined to be the worse case of the cost of the guess series.
            The optimal guess strategy for the game G[n] is the guess strategy that has the minimum cost.
            a[n] is the cost of the optimal guess strategy.
            It is indifference whether the set {0, 1, ..., n} contains the element 0
            since identifing this element takes no costs.
        Algorithms: Dynamic programming

    Complexity:
        Generate a[n] when (a[0],...,a[n-1]) are available:
            Time complexity: O(n)
            Space complexity: O(n)
        Generate a[0],...,a[n-1] entries (n entries in total):
            Time complexity: O(n^2)
            Space complexity: O(n^2)

    Examples:
        >>> list(A276128(14))
        [0, 0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 21, 24]
    """
    a = defaultdict(int)  # tuple[int, int] -> int
    for end in range(n):
        h = end - 1
        fs = deque()  # deque[tuple[int, int]], store possible values of f
        for start in range(end - 1, 0, -1):
            # search h
            while a[(start, h - 1)] > a[(h + 1, end)]:
                if (len(fs) > 0) and (fs[0][1] == h):
                    fs.popleft()  # out of range, remove
                h -= 1
            v = start + a[(start + 1, end)]  # new entry into the range
            while (len(fs) > 0) and (v < fs[-1][0]):
                fs.pop()
            fs.append((v, start))

            # update a
            f = fs[0][0]
            g = a[(start, h)] + h + 1
            a[(start, end)] = min(f, g)
        yield a[(1, end)]
