from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.log_response_log import LogResponseLog


T = TypeVar("T", bound="LogResponse")


@attr.s(auto_attribs=True)
class LogResponse:
    """A model returned a log is POSTed

    Attributes:
        log (LogResponseLog):
        status (bool):
        timestamp (str):
        message (str):
    """

    log: "LogResponseLog"
    status: bool
    timestamp: str
    message: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        log = self.log.to_dict()

        status = self.status
        timestamp = self.timestamp
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "log": log,
                "status": status,
                "timestamp": timestamp,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_response_log import LogResponseLog

        d = src_dict.copy()
        log = LogResponseLog.from_dict(d.pop("log"))

        status = d.pop("status")

        timestamp = d.pop("timestamp")

        message = d.pop("message")

        log_response = cls(
            log=log,
            status=status,
            timestamp=timestamp,
            message=message,
        )

        log_response.additional_properties = d
        return log_response

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
