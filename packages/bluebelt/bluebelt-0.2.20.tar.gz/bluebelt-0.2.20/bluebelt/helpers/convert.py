def str_to_list_of_int(x):
    """
    Build a list of integers from a string. Usefull for making lists of weeks, days, year, ...

    Parameters
    ----------
    x: the string
    
    Returns
    -------
    a list of integers

    Example
    -------
    str_to_list_of_int('3-7, 12-17')
    >> [3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17]

    """
    return [
        item
        for sublist in [
            list(range(int(group.split("-")[0]), int(group.split("-")[1]) + 1))
            for group in x.split(",")
        ]
        for item in sublist
    ]

