from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SysInfoModel")


@attr.s(auto_attribs=True)
class SysInfoModel:
    """For the most part, copied from
    https://github.com/FNNDSC/pfcon/blob/87f5da953be7c2cc80542bef0e67727dda1b4958/pfcon/pfcon.py#L601-611

    Provides information about the environment in which the service
    is currently running.

        Attributes:
            version (str):
            memory (List[Any]): Actually a NamedTuple but I'm not typing it out
            loadavg (List[Any]): Average system load over last 1, 5, and 15 minutes
            cpu_percent (float):
            system (Union[Unset, str]):  Default: 'Linux'.
            machine (Union[Unset, str]):  Default: 'x86_64'.
            uname (Union[Unset, List[str]]): Uname output, converted from object to list
            platform (Union[Unset, str]):  Default: 'Linux-6.2.2-zen1-1-zen-x86_64-with-glibc2.2.5'.
            cpucount (Union[Unset, int]):  Default: 16.
            hostname (Union[Unset, str]):  Default: '004ba48a5ffc'.
            inet (Union[Unset, str]):  Default: '172.17.0.2'.
    """

    version: str
    memory: List[Any]
    loadavg: List[Any]
    cpu_percent: float
    system: Union[Unset, str] = "Linux"
    machine: Union[Unset, str] = "x86_64"
    uname: Union[Unset, List[str]] = UNSET
    platform: Union[Unset, str] = "Linux-6.2.2-zen1-1-zen-x86_64-with-glibc2.2.5"
    cpucount: Union[Unset, int] = 16
    hostname: Union[Unset, str] = "004ba48a5ffc"
    inet: Union[Unset, str] = "172.17.0.2"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        version = self.version
        memory = self.memory

        loadavg = self.loadavg

        cpu_percent = self.cpu_percent
        system = self.system
        machine = self.machine
        uname: Union[Unset, List[str]] = UNSET
        if not isinstance(self.uname, Unset):
            uname = self.uname

        platform = self.platform
        cpucount = self.cpucount
        hostname = self.hostname
        inet = self.inet

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "memory": memory,
                "loadavg": loadavg,
                "cpu_percent": cpu_percent,
            }
        )
        if system is not UNSET:
            field_dict["system"] = system
        if machine is not UNSET:
            field_dict["machine"] = machine
        if uname is not UNSET:
            field_dict["uname"] = uname
        if platform is not UNSET:
            field_dict["platform"] = platform
        if cpucount is not UNSET:
            field_dict["cpucount"] = cpucount
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if inet is not UNSET:
            field_dict["inet"] = inet

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        version = d.pop("version")

        memory = cast(List[Any], d.pop("memory"))

        loadavg = cast(List[Any], d.pop("loadavg"))

        cpu_percent = d.pop("cpu_percent")

        system = d.pop("system", UNSET)

        machine = d.pop("machine", UNSET)

        uname = cast(List[str], d.pop("uname", UNSET))

        platform = d.pop("platform", UNSET)

        cpucount = d.pop("cpucount", UNSET)

        hostname = d.pop("hostname", UNSET)

        inet = d.pop("inet", UNSET)

        sys_info_model = cls(
            version=version,
            memory=memory,
            loadavg=loadavg,
            cpu_percent=cpu_percent,
            system=system,
            machine=machine,
            uname=uname,
            platform=platform,
            cpucount=cpucount,
            hostname=hostname,
            inet=inet,
        )

        sys_info_model.additional_properties = d
        return sys_info_model

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
