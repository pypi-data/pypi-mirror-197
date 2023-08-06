from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AboutModel")


@attr.s(auto_attribs=True)
class AboutModel:
    """
    Attributes:
        name (Union[Unset, str]):  Default: 'pfdcm_hello'.
        about (Union[Unset, str]):  Default: '`pftel` is a simple fastAPI telemetry logger. Clients POST a text payload
            to an API endpoint, which `pftel` will simply log to a file, in a variety of possible formats.\n\nAPI
            documentation is available at :22223/docs\n'.
        version (Union[Unset, str]):  Default: '1.0.0'.
    """

    name: Union[Unset, str] = "pfdcm_hello"
    about: Union[
        Unset, str
    ] = "`pftel` is a simple fastAPI telemetry logger. Clients POST a text payload to an API endpoint, which `pftel` will simply log to a file, in a variety of possible formats.\n\nAPI documentation is available at :22223/docs\n"
    version: Union[Unset, str] = "1.0.0"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        about = self.about
        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if about is not UNSET:
            field_dict["about"] = about
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        about = d.pop("about", UNSET)

        version = d.pop("version", UNSET)

        about_model = cls(
            name=name,
            about=about,
            version=version,
        )

        about_model.additional_properties = d
        return about_model

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
