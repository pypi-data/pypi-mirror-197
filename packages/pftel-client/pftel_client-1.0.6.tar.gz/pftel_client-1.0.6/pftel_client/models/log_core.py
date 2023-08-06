from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogCore")


@attr.s(auto_attribs=True)
class LogCore:
    """Model for the core log info saved to DB

    Attributes:
        url (Union[Unset, str]):  Default: 'http://localhost:2223'.
        username (Union[Unset, str]):  Default: 'any'.
        password (Union[Unset, str]):  Default: 'any'.
        db_dir (Union[Unset, str]):  Default: '/home/dicom'.
        telemetry_dir (Union[Unset, str]):  Default: 'telemetry'.
        description (Union[Unset, str]):  Default: 'Add a description!'.
    """

    url: Union[Unset, str] = "http://localhost:2223"
    username: Union[Unset, str] = "any"
    password: Union[Unset, str] = "any"
    db_dir: Union[Unset, str] = "/home/dicom"
    telemetry_dir: Union[Unset, str] = "telemetry"
    description: Union[Unset, str] = "Add a description!"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        username = self.username
        password = self.password
        db_dir = self.db_dir
        telemetry_dir = self.telemetry_dir
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password
        if db_dir is not UNSET:
            field_dict["dbDir"] = db_dir
        if telemetry_dir is not UNSET:
            field_dict["telemetryDir"] = telemetry_dir
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url", UNSET)

        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        db_dir = d.pop("dbDir", UNSET)

        telemetry_dir = d.pop("telemetryDir", UNSET)

        description = d.pop("description", UNSET)

        log_core = cls(
            url=url,
            username=username,
            password=password,
            db_dir=db_dir,
            telemetry_dir=telemetry_dir,
            description=description,
        )

        log_core.additional_properties = d
        return log_core

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
