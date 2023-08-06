import requests
import aiohttp
import typing
from .data.resources import API_ENDPOINT
from ..errors import VisepointInvalidCredentialsError

class Models:
    """
    `Models`: The Models class provides functions for retrieving completion data from visepoint API endpoints.

    Usage:
    To use `visepoint.Models`, simply import this `Models` class and call the `completion_create()` function.

    Example:
    ```
    from visepoint import Models

    # Synchronous call
    data = Models.completion_create(<model>, <authentication_token>, <query>)

    # Asynchronous call
    async_data = await Models.completion_create_async(<model>, <authentication_token>, <query>)
    ```

    See https://developers.visepoint.net/documentation/api/python/completion_create for additional information.
    """

    @staticmethod
    def completion_create(
        model: str,
        authentication: str,
        query: str,
    ) -> typing.Dict[str, typing.Any]:
        """
        Send a text-completion request to a `visepoint` model.

        Args:
            - model (str): Define a Model to query from.
            - authentication (str): Define your api key to authenticate this request.
            - query (str): Send a query to this completion model.

        Returns:
            `Dict[str, Any]`
        """
        completion_url = f'{API_ENDPOINT}/api/{authentication}/{model}?q=\'"{query}"\''
        response = requests.get(completion_url)
        if response: return response.json()['data']
        else: raise VisepointInvalidCredentialsError()

    @staticmethod
    async def completion_create_async(
        model: str,
        authentication: str,
        query: str,
    ) -> typing.Dict[str, typing.Any]:
        """
        Send an async text-completion request to a `visepoint` model.

        Args:
            - model (str): Define a Model to query from.
            - authentication (str): Define your api key to authenticate this request.
            - query (str): Send a query to this completion model.

        Returns:
            `Dict[str, Any]`
        """
        completion_url = f'{API_ENDPOINT}/api/{authentication}/{model}?q="{query}"'
        async with aiohttp.ClientSession() as session:
            async with session.get(completion_url) as response:
                try:
                    data = await response.json()
                    return data['data']
                except:
                    raise VisepointInvalidCredentialsError()