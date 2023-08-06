class InvalidDeadLockNumber(ValueError):
    """
    Raises a exception if a negative number was passed as a deadlock number
    """

    def __init__(
        self,
        message: str = 'A dead lock number must be a natural number!',
        number: int = 0,
    ):
        self.message = f"{message} The number received was: '{number}'"
        self.number = number

    def __str__(self):
        return str(self.message)


class EmptyDataFrame(ValueError):
    """
    Raises a exception if a Empty DataFrame is given to find a times series
    """

    def __init__(
        self,
        message: str = 'A Empty DataFrame there is no time series!',
    ):
        self.message = message

    def __str__(self):
        return str(self.message)
