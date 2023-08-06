"""trading related uitls"""


def currency_split(a: float, b: float, percent: bool = False) -> str | float:
    """split of currency pair

    Examples:
        >>> currency_split(99,101)
        0.02

        >>> currency_split(99,101, percent=True)
        '2.00%'

    """
    avg = (a + b) / 2
    diff = abs(a - b)
    op = diff / avg
    return f"{op * 100:.2f}%" if percent else op
