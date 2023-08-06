from typing import TypeVar, TYPE_CHECKING

from pyrestsdk.type.model import Entity

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

M = TypeVar("M", bound="MobileDevice")

class MobileDevice(Entity):
    
    _id: int
    _name: str
    _serial_number: str
    _wifi_mac_address: str
    _udid: str
    _phone_number: str
    _model: str
    _model_identifier: str
    _username: str
    _type: str
    _management_id: str
    _software_updated_device_id: str
    
    def __init__(self: M, client: "JamfServiceClient") -> None:
        super().__init__(client)
        
    @property
    def id(self) -> int:
        
        return self._id
    
    @property
    def name(self) -> str:

        return self._name
    @property
    def serial_number(self) -> str:

        return self._serial_number
    @property
    def wifi_mac_address(self) -> str:

        return self._wifi_mac_address
    @property
    def udid(self) -> str:

        return self._udid
    @property
    def phone_number(self) -> str:

        return self._phone_number
    @property
    def model(self) -> str:

        return self._model
    @property
    def model_identifier(self) -> str:

        return self._model_identifier
    @property
    def username(self) -> str:

        return self._username
    @property
    def type(self) -> str:

        return self._type
    @property
    def management_id(self) -> str:

        return self._management_id
    @property
    def software_updated_device_id(self) -> str:

        return self._software_updated_device_id
    
    @classmethod
    def from_json(cls, entry, client):
        
        _new = cls(client)
        
        _new._id = entry.get("id")
        _new._name = entry.get("name")
        _new._serial_number = entry.get("serialNumber")
        _new._wifi_mac_address = entry.get("wifiMacAddress")
        _new._udid = entry.get("udid")
        _new._phone_number = entry.get("phoneNumber")
        _new._model = entry.get("model")
        _new._model_identifier = entry.get("modelIdentifier")
        _new._username = entry.get("username")
        _new._type = entry.get("type")
        _new._management_id = entry.get("managementId")
        _new._software_updated_device_id = entry.get("softwareUpdateDeviceId")
        
        return _new