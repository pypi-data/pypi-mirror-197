from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entry_create_attachments_review_record_status import EntryCreateAttachmentsReviewRecordStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryCreateAttachmentsReviewRecord")


@attr.s(auto_attribs=True, repr=False)
class EntryCreateAttachmentsReviewRecord:
    """  """

    _message: Union[Unset, str] = UNSET
    _status: Union[Unset, EntryCreateAttachmentsReviewRecordStatus] = UNSET

    def __repr__(self):
        fields = []
        fields.append("message={}".format(repr(self._message)))
        fields.append("status={}".format(repr(self._status)))
        return "EntryCreateAttachmentsReviewRecord({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        message = self._message
        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
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

        def get_status() -> Union[Unset, EntryCreateAttachmentsReviewRecordStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = EntryCreateAttachmentsReviewRecordStatus(_status)
                except ValueError:
                    status = EntryCreateAttachmentsReviewRecordStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, EntryCreateAttachmentsReviewRecordStatus], UNSET)

        entry_create_attachments_review_record = cls(
            message=message,
            status=status,
        )

        return entry_create_attachments_review_record

    @property
    def message(self) -> str:
        """ User message to set on review """
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
    def status(self) -> EntryCreateAttachmentsReviewRecordStatus:
        """ Review Status for entry """
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: EntryCreateAttachmentsReviewRecordStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
