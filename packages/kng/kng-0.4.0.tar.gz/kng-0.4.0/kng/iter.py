"""utils for iterables"""


def list_2d(arr: list, row_size: int, fill_end=None) -> list[list]:
    """convert 1D list to 2D list, aka. rows

    Examples:
        >>> list_2d([1,2,3,4,5], row_size=2)
        [[1, 2], [3, 4], [5]]

        >>> list_2d([1,2,3,4,5], row_size=2, fill_end=0)
        [[1, 2], [3, 4], [5, 0]]


    Args:
        arr (list): 1D list
        row_size (int): len of the rows
        fill_end (Any, optional): obj to fill the last chuck. None means don't fill.
    """
    op = []
    for i in range(0, len(arr), row_size):
        row = arr[i : i + row_size]
        if fill_end is not None and len(row) < row_size:
            shortage = row_size - len(row)
            row = row + [fill_end] * shortage
        op.append(row)
    return op
