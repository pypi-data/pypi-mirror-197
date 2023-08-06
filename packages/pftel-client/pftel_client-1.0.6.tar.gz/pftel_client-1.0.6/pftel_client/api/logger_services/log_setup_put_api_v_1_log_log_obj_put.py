from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.log_core import LogCore
from ...models.log_init import LogInit
from ...types import Response


def _get_kwargs(
    log_obj: str,
    *,
    client: Client,
    json_body: LogCore,
) -> Dict[str, Any]:
    url = "{}/api/v1/log/{logObj}/".format(client.base_url, logObj=log_obj)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[HTTPValidationError, LogInit]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LogInit.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[HTTPValidationError, LogInit]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    log_obj: str,
    *,
    client: Client,
    json_body: LogCore,
) -> Response[Union[HTTPValidationError, LogInit]]:
    """PUT information to a (possibly new) pftel object

     Description
    -----------
    PUT an entire object. If the object already exists, overwrite.
    If it does not exist, append to the space of available objects.

    Args:
        log_obj (str):
        json_body (LogCore): Model for the core log info saved to DB

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogInit]]
    """

    kwargs = _get_kwargs(
        log_obj=log_obj,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    log_obj: str,
    *,
    client: Client,
    json_body: LogCore,
) -> Optional[Union[HTTPValidationError, LogInit]]:
    """PUT information to a (possibly new) pftel object

     Description
    -----------
    PUT an entire object. If the object already exists, overwrite.
    If it does not exist, append to the space of available objects.

    Args:
        log_obj (str):
        json_body (LogCore): Model for the core log info saved to DB

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogInit]]
    """

    return sync_detailed(
        log_obj=log_obj,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    log_obj: str,
    *,
    client: Client,
    json_body: LogCore,
) -> Response[Union[HTTPValidationError, LogInit]]:
    """PUT information to a (possibly new) pftel object

     Description
    -----------
    PUT an entire object. If the object already exists, overwrite.
    If it does not exist, append to the space of available objects.

    Args:
        log_obj (str):
        json_body (LogCore): Model for the core log info saved to DB

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogInit]]
    """

    kwargs = _get_kwargs(
        log_obj=log_obj,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    log_obj: str,
    *,
    client: Client,
    json_body: LogCore,
) -> Optional[Union[HTTPValidationError, LogInit]]:
    """PUT information to a (possibly new) pftel object

     Description
    -----------
    PUT an entire object. If the object already exists, overwrite.
    If it does not exist, append to the space of available objects.

    Args:
        log_obj (str):
        json_body (LogCore): Model for the core log info saved to DB

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogInit]]
    """

    return (
        await asyncio_detailed(
            log_obj=log_obj,
            client=client,
            json_body=json_body,
        )
    ).parsed
