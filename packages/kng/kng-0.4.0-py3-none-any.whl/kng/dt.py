"""datetime utils"""


def decimal_yr(
    yr: int, mo: int, day: int, hr: int = 0, mi: int = 0, sec: int = 0
) -> float:
    """return decimal year from year, month, day

    Examples:
        >>> decimal_yr(2000,1,1)
        2000.0

        >>> round(decimal_yr(2000,6,15), 1)
        2000.5
    """
    from datetime import datetime as dt

    yr_start = dt(yr, 1, 1)
    days_of_yr = dt(yr + 1, 1, 1) - yr_start
    current = dt(yr, mo, day, hr, mi, sec)
    fraction = (current - yr_start) / days_of_yr
    return yr + fraction
