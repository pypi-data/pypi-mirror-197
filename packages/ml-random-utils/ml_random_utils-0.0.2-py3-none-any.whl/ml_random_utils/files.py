from pathlib import Path


def read_lines(
    path: str | Path, encoding: str | None = "utf-8",
    skip_blank: bool = True
) -> list[str]:
    """
    Reads file lines by stripping out breaklines and trailing empty lines.

    Arguments:
        path: the path to open as a file.
        encoding: the desired encoding

    Returns:
        lines: a list with one element for each file line.
    """
    with open(path, "r", encoding=encoding) as file:
        lines = [line.strip() for line in file.readlines()]

    if skip_blank:
        return [l for l in lines if l != ""]

    return lines
