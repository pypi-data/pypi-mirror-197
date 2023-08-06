from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogStructured")


@attr.s(auto_attribs=True)
class LogStructured:
    """A simple structured log model

    Attributes:
        log_object (Union[Unset, str]):  Default: 'default'.
        log_collection (Union[Unset, str]):  Default: ''.
        log_event (Union[Unset, str]):  Default: ''.
        app_name (Union[Unset, str]):  Default: ''.
        exec_time (Union[Unset, float]):
        request_host (Union[Unset, str]):  Default: ''.
        request_port (Union[Unset, str]):  Default: ''.
        request_user_agent (Union[Unset, str]):  Default: ''.
        payload (Union[Unset, str]):  Default: ''.
    """

    log_object: Union[Unset, str] = "default"
    log_collection: Union[Unset, str] = ""
    log_event: Union[Unset, str] = ""
    app_name: Union[Unset, str] = ""
    exec_time: Union[Unset, float] = 0.0
    request_host: Union[Unset, str] = ""
    request_port: Union[Unset, str] = ""
    request_user_agent: Union[Unset, str] = ""
    payload: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        log_object = self.log_object
        log_collection = self.log_collection
        log_event = self.log_event
        app_name = self.app_name
        exec_time = self.exec_time
        request_host = self.request_host
        request_port = self.request_port
        request_user_agent = self.request_user_agent
        payload = self.payload

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if log_object is not UNSET:
            field_dict["logObject"] = log_object
        if log_collection is not UNSET:
            field_dict["logCollection"] = log_collection
        if log_event is not UNSET:
            field_dict["logEvent"] = log_event
        if app_name is not UNSET:
            field_dict["appName"] = app_name
        if exec_time is not UNSET:
            field_dict["execTime"] = exec_time
        if request_host is not UNSET:
            field_dict["requestHost"] = request_host
        if request_port is not UNSET:
            field_dict["requestPort"] = request_port
        if request_user_agent is not UNSET:
            field_dict["requestUserAgent"] = request_user_agent
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        log_object = d.pop("logObject", UNSET)

        log_collection = d.pop("logCollection", UNSET)

        log_event = d.pop("logEvent", UNSET)

        app_name = d.pop("appName", UNSET)

        exec_time = d.pop("execTime", UNSET)

        request_host = d.pop("requestHost", UNSET)

        request_port = d.pop("requestPort", UNSET)

        request_user_agent = d.pop("requestUserAgent", UNSET)

        payload = d.pop("payload", UNSET)

        log_structured = cls(
            log_object=log_object,
            log_collection=log_collection,
            log_event=log_event,
            app_name=app_name,
            exec_time=exec_time,
            request_host=request_host,
            request_port=request_port,
            request_user_agent=request_user_agent,
            payload=payload,
        )

        log_structured.additional_properties = d
        return log_structured

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
