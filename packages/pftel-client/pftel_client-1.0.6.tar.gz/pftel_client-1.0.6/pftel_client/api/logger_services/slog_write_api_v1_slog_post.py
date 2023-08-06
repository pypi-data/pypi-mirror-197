from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.log_response import LogResponse
from ...models.log_simple import LogSimple
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    json_body: LogSimple,
    log_object: Union[Unset, None, str] = "default",
    log_collection: Union[Unset, None, str] = "slog",
    log_event: Union[Unset, None, str] = "log",
) -> Dict[str, Any]:
    url = "{}/api/v1/slog/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["logObject"] = log_object

    params["logCollection"] = log_collection

    params["logEvent"] = log_event

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[HTTPValidationError, LogResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LogResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[HTTPValidationError, LogResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: LogSimple,
    log_object: Union[Unset, None, str] = "default",
    log_collection: Union[Unset, None, str] = "slog",
    log_event: Union[Unset, None, str] = "log",
) -> Response[Union[HTTPValidationError, LogResponse]]:
    """
        Use this API route to POST a simple log payload to the
        logger.


     Description
    -----------

    Use this API entry point to simply record some log string.
    `slog` entries are by default logged to `default/slog/<count>-log`
    but this can be overriden with appropriate query parameters.

    ```
    {
        log  : str   = \"\"
    }
    ```

    Internally, they are mapped to a complete *telemetry* model for
    consistent processing.

    Args:
        log_object (Union[Unset, None, str]):  Default: 'default'.
        log_collection (Union[Unset, None, str]):  Default: 'slog'.
        log_event (Union[Unset, None, str]):  Default: 'log'.
        json_body (LogSimple): The simplest log model POST

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        log_object=log_object,
        log_collection=log_collection,
        log_event=log_event,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: LogSimple,
    log_object: Union[Unset, None, str] = "default",
    log_collection: Union[Unset, None, str] = "slog",
    log_event: Union[Unset, None, str] = "log",
) -> Optional[Union[HTTPValidationError, LogResponse]]:
    """
        Use this API route to POST a simple log payload to the
        logger.


     Description
    -----------

    Use this API entry point to simply record some log string.
    `slog` entries are by default logged to `default/slog/<count>-log`
    but this can be overriden with appropriate query parameters.

    ```
    {
        log  : str   = \"\"
    }
    ```

    Internally, they are mapped to a complete *telemetry* model for
    consistent processing.

    Args:
        log_object (Union[Unset, None, str]):  Default: 'default'.
        log_collection (Union[Unset, None, str]):  Default: 'slog'.
        log_event (Union[Unset, None, str]):  Default: 'log'.
        json_body (LogSimple): The simplest log model POST

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogResponse]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        log_object=log_object,
        log_collection=log_collection,
        log_event=log_event,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: LogSimple,
    log_object: Union[Unset, None, str] = "default",
    log_collection: Union[Unset, None, str] = "slog",
    log_event: Union[Unset, None, str] = "log",
) -> Response[Union[HTTPValidationError, LogResponse]]:
    """
        Use this API route to POST a simple log payload to the
        logger.


     Description
    -----------

    Use this API entry point to simply record some log string.
    `slog` entries are by default logged to `default/slog/<count>-log`
    but this can be overriden with appropriate query parameters.

    ```
    {
        log  : str   = \"\"
    }
    ```

    Internally, they are mapped to a complete *telemetry* model for
    consistent processing.

    Args:
        log_object (Union[Unset, None, str]):  Default: 'default'.
        log_collection (Union[Unset, None, str]):  Default: 'slog'.
        log_event (Union[Unset, None, str]):  Default: 'log'.
        json_body (LogSimple): The simplest log model POST

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        log_object=log_object,
        log_collection=log_collection,
        log_event=log_event,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: LogSimple,
    log_object: Union[Unset, None, str] = "default",
    log_collection: Union[Unset, None, str] = "slog",
    log_event: Union[Unset, None, str] = "log",
) -> Optional[Union[HTTPValidationError, LogResponse]]:
    """
        Use this API route to POST a simple log payload to the
        logger.


     Description
    -----------

    Use this API entry point to simply record some log string.
    `slog` entries are by default logged to `default/slog/<count>-log`
    but this can be overriden with appropriate query parameters.

    ```
    {
        log  : str   = \"\"
    }
    ```

    Internally, they are mapped to a complete *telemetry* model for
    consistent processing.

    Args:
        log_object (Union[Unset, None, str]):  Default: 'default'.
        log_collection (Union[Unset, None, str]):  Default: 'slog'.
        log_event (Union[Unset, None, str]):  Default: 'log'.
        json_body (LogSimple): The simplest log model POST

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogResponse]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            log_object=log_object,
            log_collection=log_collection,
            log_event=log_event,
        )
    ).parsed
