from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.log_core import LogCore
    from ..models.time import Time


T = TypeVar("T", bound="LogInit")


@attr.s(auto_attribs=True)
class LogInit:
    """A full model that is returned from a query call

    Attributes:
        info (LogCore): Model for the core log info saved to DB
        time_created (Time): A simple model that has a time string field
        time_modified (Time): A simple model that has a time string field
        message (str):
    """

    info: "LogCore"
    time_created: "Time"
    time_modified: "Time"
    message: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        info = self.info.to_dict()

        time_created = self.time_created.to_dict()

        time_modified = self.time_modified.to_dict()

        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "info": info,
                "time_created": time_created,
                "time_modified": time_modified,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_core import LogCore
        from ..models.time import Time

        d = src_dict.copy()
        info = LogCore.from_dict(d.pop("info"))

        time_created = Time.from_dict(d.pop("time_created"))

        time_modified = Time.from_dict(d.pop("time_modified"))

        message = d.pop("message")

        log_init = cls(
            info=info,
            time_created=time_created,
            time_modified=time_modified,
            message=message,
        )

        log_init.additional_properties = d
        return log_init

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
