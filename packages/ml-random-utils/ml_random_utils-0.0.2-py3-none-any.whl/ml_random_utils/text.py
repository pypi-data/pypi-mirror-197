import itertools
from typing import Generator


def replace_char(text: str, char: str, replacement: str) -> str:
    """
    Replaces the first occurrence of char in text with replacement.

    Args:
        text (str): the text where char will be replaced.
        char (str): the char to be replaced

    Returns:
        a string where the occurrence of char has been replaced with replacement.
    """

    idx = text.index(char)
    return text[:idx] + replacement + text[idx + 1 :]


def ngrams(text: str, n: int) -> list[str]:
    """
    Splits text into overlapping n-grams.

    Args:
        text (str): the text to split.
        n (int): the size of the gram

    Returns:
        a list of n-grams
    """
    return [text[i : i + n] for i in range(0, len(text) + 1 - n)]


def ngrams_vocabulary(
    alphabet: str | list[str],
    n: int,
) -> Generator:
    """
    Generates a vocabulary of ngrams on the fly with consistent ordering.

    Arguments:
        alphabet: base characters (as a string or list)
        n: word size

    Returns:
        a generator that produces each word in the vocabulary.
    """
    if isinstance(alphabet, str):
        alphabet = list(alphabet)

    alphabet = list(set(alphabet))

    for char_list in itertools.product(alphabet, repeat=n):
        yield "".join(char_list)
