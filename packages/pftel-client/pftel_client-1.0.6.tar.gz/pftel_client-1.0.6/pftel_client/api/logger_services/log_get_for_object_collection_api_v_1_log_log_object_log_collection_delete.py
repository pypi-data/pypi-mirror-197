from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.log_delete import LogDelete
from ...types import Response


def _get_kwargs(
    log_object: str,
    log_collection: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/api/v1/log/{logObject}/{logCollection}/".format(
        client.base_url, logObject=log_object, logCollection=log_collection
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[HTTPValidationError, LogDelete]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LogDelete.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[HTTPValidationError, LogDelete]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    log_object: str,
    log_collection: str,
    *,
    client: Client,
) -> Response[Union[HTTPValidationError, LogDelete]]:
    """
        DELETE all the events comprising this log object.


     Description
    -----------
    DELETE all the events in the collection `logCollection` of the object
    `logObject`. Use with care!

    Args:
        log_object (str):
        log_collection (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogDelete]]
    """

    kwargs = _get_kwargs(
        log_object=log_object,
        log_collection=log_collection,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    log_object: str,
    log_collection: str,
    *,
    client: Client,
) -> Optional[Union[HTTPValidationError, LogDelete]]:
    """
        DELETE all the events comprising this log object.


     Description
    -----------
    DELETE all the events in the collection `logCollection` of the object
    `logObject`. Use with care!

    Args:
        log_object (str):
        log_collection (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogDelete]]
    """

    return sync_detailed(
        log_object=log_object,
        log_collection=log_collection,
        client=client,
    ).parsed


async def asyncio_detailed(
    log_object: str,
    log_collection: str,
    *,
    client: Client,
) -> Response[Union[HTTPValidationError, LogDelete]]:
    """
        DELETE all the events comprising this log object.


     Description
    -----------
    DELETE all the events in the collection `logCollection` of the object
    `logObject`. Use with care!

    Args:
        log_object (str):
        log_collection (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogDelete]]
    """

    kwargs = _get_kwargs(
        log_object=log_object,
        log_collection=log_collection,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    log_object: str,
    log_collection: str,
    *,
    client: Client,
) -> Optional[Union[HTTPValidationError, LogDelete]]:
    """
        DELETE all the events comprising this log object.


     Description
    -----------
    DELETE all the events in the collection `logCollection` of the object
    `logObject`. Use with care!

    Args:
        log_object (str):
        log_collection (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogDelete]]
    """

    return (
        await asyncio_detailed(
            log_object=log_object,
            log_collection=log_collection,
            client=client,
        )
    ).parsed
