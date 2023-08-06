import typing
import requests
from .data.resources import API_ENDPOINT
from ..errors import VisepointCreateError

class UserCreate:
    """
    `UserCreate`: Create a visepoint user.

    Usage: 
    If you don't already have a visepoint account, create one by initializing our `create` function (or just by calling this class). This will return a checkout session for you to proceed with the creation of your account.
    """
    def generate_checkout(model: str = '') -> str:
        completion_url = f'{API_ENDPOINT}/new/{model}'
        response = requests.get(completion_url).json()
        if response:
            return response
        else:
            raise VisepointCreateError()