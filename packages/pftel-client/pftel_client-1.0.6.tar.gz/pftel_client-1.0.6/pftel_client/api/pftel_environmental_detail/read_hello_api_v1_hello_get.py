from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.hello_model import HelloModel
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    echo_back: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/hello/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["echoBack"] = echo_back

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[HTTPValidationError, HelloModel]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = HelloModel.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[HTTPValidationError, HelloModel]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    echo_back: Union[Unset, None, str] = UNSET,
) -> Response[Union[HTTPValidationError, HelloModel]]:
    """Read Hello

     Produce some information like the OG pfcon

    Args:
        echo_back (Union[Unset, None, str]): something to print back verbatim

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, HelloModel]]
    """

    kwargs = _get_kwargs(
        client=client,
        echo_back=echo_back,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    echo_back: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HTTPValidationError, HelloModel]]:
    """Read Hello

     Produce some information like the OG pfcon

    Args:
        echo_back (Union[Unset, None, str]): something to print back verbatim

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, HelloModel]]
    """

    return sync_detailed(
        client=client,
        echo_back=echo_back,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    echo_back: Union[Unset, None, str] = UNSET,
) -> Response[Union[HTTPValidationError, HelloModel]]:
    """Read Hello

     Produce some information like the OG pfcon

    Args:
        echo_back (Union[Unset, None, str]): something to print back verbatim

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, HelloModel]]
    """

    kwargs = _get_kwargs(
        client=client,
        echo_back=echo_back,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    echo_back: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HTTPValidationError, HelloModel]]:
    """Read Hello

     Produce some information like the OG pfcon

    Args:
        echo_back (Union[Unset, None, str]): something to print back verbatim

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, HelloModel]]
    """

    return (
        await asyncio_detailed(
            client=client,
            echo_back=echo_back,
        )
    ).parsed
