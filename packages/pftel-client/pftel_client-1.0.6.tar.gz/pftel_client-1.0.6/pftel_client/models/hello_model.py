from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.echo_model import EchoModel
    from ..models.sys_info_model import SysInfoModel


T = TypeVar("T", bound="HelloModel")


@attr.s(auto_attribs=True)
class HelloModel:
    """The model describing the relevant "hello" data

    Attributes:
        name (Union[Unset, str]):  Default: 'pfdcm_hello'.
        version (Union[Unset, str]):  Default: '1.0.0'.
        sysinfo (Union[Unset, SysInfoModel]): For the most part, copied from
            https://github.com/FNNDSC/pfcon/blob/87f5da953be7c2cc80542bef0e67727dda1b4958/pfcon/pfcon.py#L601-611

            Provides information about the environment in which the service
            is currently running.
        echo_back (Union[Unset, EchoModel]): Simply echo back whatever is POSTed to this API endpoing
    """

    name: Union[Unset, str] = "pfdcm_hello"
    version: Union[Unset, str] = "1.0.0"
    sysinfo: Union[Unset, "SysInfoModel"] = UNSET
    echo_back: Union[Unset, "EchoModel"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        version = self.version
        sysinfo: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.sysinfo, Unset):
            sysinfo = self.sysinfo.to_dict()

        echo_back: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.echo_back, Unset):
            echo_back = self.echo_back.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if version is not UNSET:
            field_dict["version"] = version
        if sysinfo is not UNSET:
            field_dict["sysinfo"] = sysinfo
        if echo_back is not UNSET:
            field_dict["echoBack"] = echo_back

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.echo_model import EchoModel
        from ..models.sys_info_model import SysInfoModel

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        version = d.pop("version", UNSET)

        _sysinfo = d.pop("sysinfo", UNSET)
        sysinfo: Union[Unset, SysInfoModel]
        if isinstance(_sysinfo, Unset):
            sysinfo = UNSET
        else:
            sysinfo = SysInfoModel.from_dict(_sysinfo)

        _echo_back = d.pop("echoBack", UNSET)
        echo_back: Union[Unset, EchoModel]
        if isinstance(_echo_back, Unset):
            echo_back = UNSET
        else:
            echo_back = EchoModel.from_dict(_echo_back)

        hello_model = cls(
            name=name,
            version=version,
            sysinfo=sysinfo,
            echo_back=echo_back,
        )

        hello_model.additional_properties = d
        return hello_model

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
