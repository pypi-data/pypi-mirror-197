from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    log_object: str,
    log_collection: str,
    *,
    client: Client,
    style: Union[Unset, None, str] = "plain",
    padding: Union[Unset, None, bool] = False,
    fields: Union[Unset, None, str] = "",
) -> Dict[str, Any]:
    url = "{}/api/v1/log/{logObject}/{logCollection}/csv".format(
        client.base_url, logObject=log_object, logCollection=log_collection
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["style"] = style

    params["padding"] = padding

    params["fields"] = fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[HTTPValidationError, str]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(str, response.json())
        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[HTTPValidationError, str]]:
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
    style: Union[Unset, None, str] = "plain",
    padding: Union[Unset, None, bool] = False,
    fields: Union[Unset, None, str] = "",
) -> Response[Union[HTTPValidationError, str]]:
    """
        GET all the events comprising this log object collection as
        a CSV formatted string


     Description
    -----------
    GET all the events in the collection `logCollection` of the object
    `logObject` as a CSV formatted string.

    By passing a URL query as `style=fancy` a _fancy_ CSV payload is
    returned. Passing a comma-separated string of `fields=<strlist>`
    will only return the `strlist` tokens in the CSV.

    Args:
        log_object (str):
        log_collection (str):
        style (Union[Unset, None, str]):  Default: 'plain'.
        padding (Union[Unset, None, bool]):
        fields (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, str]]
    """

    kwargs = _get_kwargs(
        log_object=log_object,
        log_collection=log_collection,
        client=client,
        style=style,
        padding=padding,
        fields=fields,
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
    style: Union[Unset, None, str] = "plain",
    padding: Union[Unset, None, bool] = False,
    fields: Union[Unset, None, str] = "",
) -> Optional[Union[HTTPValidationError, str]]:
    """
        GET all the events comprising this log object collection as
        a CSV formatted string


     Description
    -----------
    GET all the events in the collection `logCollection` of the object
    `logObject` as a CSV formatted string.

    By passing a URL query as `style=fancy` a _fancy_ CSV payload is
    returned. Passing a comma-separated string of `fields=<strlist>`
    will only return the `strlist` tokens in the CSV.

    Args:
        log_object (str):
        log_collection (str):
        style (Union[Unset, None, str]):  Default: 'plain'.
        padding (Union[Unset, None, bool]):
        fields (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, str]]
    """

    return sync_detailed(
        log_object=log_object,
        log_collection=log_collection,
        client=client,
        style=style,
        padding=padding,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    log_object: str,
    log_collection: str,
    *,
    client: Client,
    style: Union[Unset, None, str] = "plain",
    padding: Union[Unset, None, bool] = False,
    fields: Union[Unset, None, str] = "",
) -> Response[Union[HTTPValidationError, str]]:
    """
        GET all the events comprising this log object collection as
        a CSV formatted string


     Description
    -----------
    GET all the events in the collection `logCollection` of the object
    `logObject` as a CSV formatted string.

    By passing a URL query as `style=fancy` a _fancy_ CSV payload is
    returned. Passing a comma-separated string of `fields=<strlist>`
    will only return the `strlist` tokens in the CSV.

    Args:
        log_object (str):
        log_collection (str):
        style (Union[Unset, None, str]):  Default: 'plain'.
        padding (Union[Unset, None, bool]):
        fields (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, str]]
    """

    kwargs = _get_kwargs(
        log_object=log_object,
        log_collection=log_collection,
        client=client,
        style=style,
        padding=padding,
        fields=fields,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    log_object: str,
    log_collection: str,
    *,
    client: Client,
    style: Union[Unset, None, str] = "plain",
    padding: Union[Unset, None, bool] = False,
    fields: Union[Unset, None, str] = "",
) -> Optional[Union[HTTPValidationError, str]]:
    """
        GET all the events comprising this log object collection as
        a CSV formatted string


     Description
    -----------
    GET all the events in the collection `logCollection` of the object
    `logObject` as a CSV formatted string.

    By passing a URL query as `style=fancy` a _fancy_ CSV payload is
    returned. Passing a comma-separated string of `fields=<strlist>`
    will only return the `strlist` tokens in the CSV.

    Args:
        log_object (str):
        log_collection (str):
        style (Union[Unset, None, str]):  Default: 'plain'.
        padding (Union[Unset, None, bool]):
        fields (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, str]]
    """

    return (
        await asyncio_detailed(
            log_object=log_object,
            log_collection=log_collection,
            client=client,
            style=style,
            padding=padding,
            fields=fields,
        )
    ).parsed
