from pathlib import Path


def listdir(path: str | Path, pattern: str = "*") -> list[Path]:
    """
    Returns a list of Paths in the path directory in alphabetical order.

    Arguments:
        path: the path of the directory.
        pattern: a glob pattern to filter paths of interest.

    Returns:
        the list of paths in the directory sorted in alphabetical order.
    """
    return sorted(Path(path).glob(pattern))


def dir_is_empty(path: str | Path, pattern: str = "*") -> bool:
    """
    Checks whether a directory is empty (or if contains files with a certain pattern).

    Arguments:
        path: the path of the directory.
        pattern: a glob pattern to filter paths of interest.

    Returns:
        True if there are files (that respect the pattern) in the directory, False otherwise.

    """
    return not any(Path(path).glob(pattern))
