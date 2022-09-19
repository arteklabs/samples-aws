class InvalidArgError(Exception):
    """
    Raised if the argument is not [0].
    """
    pass


def f(arg=[0]):
    """
    Returns 0 if ``arg == ['0']``

    :param arg: An argument of no use.
    :type arg: list[int]
    :raise mod.InvalidArgError: if arg is not [0].
    :return: 0
    :rtype: list[int]
    """
    if arg == [0]:
        return 0
    else:
        raise InvalidArgError
