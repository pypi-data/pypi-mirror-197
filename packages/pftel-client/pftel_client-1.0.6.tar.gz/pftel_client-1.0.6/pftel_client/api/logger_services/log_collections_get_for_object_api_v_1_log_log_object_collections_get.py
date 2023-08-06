from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    log_object: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/api/v1/log/{logObject}/collections/".format(client.base_url, logObject=log_object)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[HTTPValidationError, List[Any]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(List[Any], response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[HTTPValidationError, List[Any]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    log_object: str,
    *,
    client: Client,
) -> Response[Union[HTTPValidationError, List[Any]]]:
    """
        GET the collections that constitute this log object


     Description
    -----------
    GET the list of collections in `logObject`. A _collection_ gathers
    a set of events. For instance, a _collection_ called **02Feb2024** could
    collect all events from the 2nd Feb 2024.

    Args:
        log_object (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List[Any]]]
    """

    kwargs = _get_kwargs(
        log_object=log_object,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    log_object: str,
    *,
    client: Client,
) -> Optional[Union[HTTPValidationError, List[Any]]]:
    """
        GET the collections that constitute this log object


     Description
    -----------
    GET the list of collections in `logObject`. A _collection_ gathers
    a set of events. For instance, a _collection_ called **02Feb2024** could
    collect all events from the 2nd Feb 2024.

    Args:
        log_object (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List[Any]]]
    """

    return sync_detailed(
        log_object=log_object,
        client=client,
    ).parsed


async def asyncio_detailed(
    log_object: str,
    *,
    client: Client,
) -> Response[Union[HTTPValidationError, List[Any]]]:
    """
        GET the collections that constitute this log object


     Description
    -----------
    GET the list of collections in `logObject`. A _collection_ gathers
    a set of events. For instance, a _collection_ called **02Feb2024** could
    collect all events from the 2nd Feb 2024.

    Args:
        log_object (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List[Any]]]
    """

    kwargs = _get_kwargs(
        log_object=log_object,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    log_object: str,
    *,
    client: Client,
) -> Optional[Union[HTTPValidationError, List[Any]]]:
    """
        GET the collections that constitute this log object


     Description
    -----------
    GET the list of collections in `logObject`. A _collection_ gathers
    a set of events. For instance, a _collection_ called **02Feb2024** could
    collect all events from the 2nd Feb 2024.

    Args:
        log_object (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List[Any]]]
    """

    return (
        await asyncio_detailed(
            log_object=log_object,
            client=client,
        )
    ).parsed
