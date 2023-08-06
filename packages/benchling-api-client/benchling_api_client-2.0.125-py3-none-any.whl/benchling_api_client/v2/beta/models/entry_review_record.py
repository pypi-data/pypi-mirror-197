from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entry_review_record_status import EntryReviewRecordStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryReviewRecord")


@attr.s(auto_attribs=True, repr=False)
class EntryReviewRecord:
    """ Review record if set """

    _message: Union[Unset, str] = UNSET
    _status: Union[Unset, EntryReviewRecordStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("message={}".format(repr(self._message)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EntryReviewRecord({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        message = self._message
        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if message is not UNSET:
            field_dict["message"] = message
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_message() -> Union[Unset, str]:
            message = d.pop("message")
            return message

        try:
            message = get_message()
        except KeyError:
            if strict:
                raise
            message = cast(Union[Unset, str], UNSET)

        def get_status() -> Union[Unset, EntryReviewRecordStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = EntryReviewRecordStatus(_status)
                except ValueError:
                    status = EntryReviewRecordStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, EntryReviewRecordStatus], UNSET)

        entry_review_record = cls(
            message=message,
            status=status,
        )

        entry_review_record.additional_properties = d
        return entry_review_record

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

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def message(self) -> str:
        """ Reviewer's Comments """
        if isinstance(self._message, Unset):
            raise NotPresentError(self, "message")
        return self._message

    @message.setter
    def message(self, value: str) -> None:
        self._message = value

    @message.deleter
    def message(self) -> None:
        self._message = UNSET

    @property
    def status(self) -> EntryReviewRecordStatus:
        """ Review Status of the entry """
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: EntryReviewRecordStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
