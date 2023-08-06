import functools
from gwdc_python.exceptions import GWDCAuthenticationError


class GWLabAuthenticationError(Exception):
    def __init__(self):
        super().__init__(
            """
Your API token does not exist, make sure it is correct!

Please read the API token documentation:
https://gwlab-viterbi-python.readthedocs.io/en/latest/gettingstarted.html#getting-access

Alternatively, head straight to https://gwlab.org.au/auth/api-token to create one.
            """
        )


def custom_error_handler(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except GWDCAuthenticationError:
            raise GWLabAuthenticationError
    return wrapper
