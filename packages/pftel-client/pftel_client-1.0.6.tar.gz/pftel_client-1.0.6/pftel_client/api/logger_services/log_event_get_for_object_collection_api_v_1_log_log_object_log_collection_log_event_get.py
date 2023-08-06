from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.log_event_get_for_object_collection_api_v1_log_log_object_log_collection_log_event_get_response_logevent_getforobjectcollection_api_v1_log_logobject_logcollection_logevent_get import (
    LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet,
)
from ...types import Response


def _get_kwargs(
    log_object: str,
    log_collection: str,
    log_event: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/api/v1/log/{logObject}/{logCollection}/{logEvent}/".format(
        client.base_url, logObject=log_object, logCollection=log_collection, logEvent=log_event
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[
    Union[
        HTTPValidationError,
        LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet.from_dict(
            response.json()
        )

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        HTTPValidationError,
        LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    log_object: str,
    log_collection: str,
    log_event: str,
    *,
    client: Client,
) -> Response[
    Union[
        HTTPValidationError,
        LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet,
    ]
]:
    """
        GET a specific event that exists in this log object collection.


     Description
    -----------
    GET the specific details of event `logEvent` in the collection
    `logCollection` of the object `logObject`.

    Args:
        log_object (str):
        log_collection (str):
        log_event (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet]]
    """

    kwargs = _get_kwargs(
        log_object=log_object,
        log_collection=log_collection,
        log_event=log_event,
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
    log_event: str,
    *,
    client: Client,
) -> Optional[
    Union[
        HTTPValidationError,
        LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet,
    ]
]:
    """
        GET a specific event that exists in this log object collection.


     Description
    -----------
    GET the specific details of event `logEvent` in the collection
    `logCollection` of the object `logObject`.

    Args:
        log_object (str):
        log_collection (str):
        log_event (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet]]
    """

    return sync_detailed(
        log_object=log_object,
        log_collection=log_collection,
        log_event=log_event,
        client=client,
    ).parsed


async def asyncio_detailed(
    log_object: str,
    log_collection: str,
    log_event: str,
    *,
    client: Client,
) -> Response[
    Union[
        HTTPValidationError,
        LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet,
    ]
]:
    """
        GET a specific event that exists in this log object collection.


     Description
    -----------
    GET the specific details of event `logEvent` in the collection
    `logCollection` of the object `logObject`.

    Args:
        log_object (str):
        log_collection (str):
        log_event (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet]]
    """

    kwargs = _get_kwargs(
        log_object=log_object,
        log_collection=log_collection,
        log_event=log_event,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    log_object: str,
    log_collection: str,
    log_event: str,
    *,
    client: Client,
) -> Optional[
    Union[
        HTTPValidationError,
        LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet,
    ]
]:
    """
        GET a specific event that exists in this log object collection.


     Description
    -----------
    GET the specific details of event `logEvent` in the collection
    `logCollection` of the object `logObject`.

    Args:
        log_object (str):
        log_collection (str):
        log_event (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogEventGetForObjectCollectionApiV1LogLogObjectLogCollectionLogEventGetResponseLogeventGetforobjectcollectionApiV1LogLogobjectLogcollectionLogeventGet]]
    """

    return (
        await asyncio_detailed(
            log_object=log_object,
            log_collection=log_collection,
            log_event=log_event,
            client=client,
        )
    ).parsed
