"""Type gt.dispatch.boolean.local, version 100"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from gwproto.errors import MpSchemaError


def check_is_left_right_dot(v: str) -> None:
    """Checks LeftRightDot Format

    LeftRightDot format: Lowercase alphanumeric words separated by periods,
    most significant word (on the left) starting with an alphabet character.

    Args:
        v (str): the candidate

    Raises:
        ValueError: if v is not LeftRightDot format
    """
    from typing import List

    try:
        x: List[str] = v.split(".")
    except:
        raise ValueError(f"Failed to seperate {v} into words with split'.'")
    first_word = x[0]
    first_char = first_word[0]
    if not first_char.isalpha():
        raise ValueError(f"Most significant word of {v} must start with alphabet char.")
    for word in x:
        if not word.isalnum():
            raise ValueError(f"words of {v} split by by '.' must be alphanumeric.")
    if not v.islower():
        raise ValueError(f"All characters of {v} must be lowercase.")


def check_is_reasonable_unix_time_ms(v: int) -> None:
    """Checks ReasonableUnixTimeMs format

    ReasonableUnixTimeMs format: unix milliseconds between Jan 1 2000 and Jan 1 3000

    Args:
        v (int): the candidate

    Raises:
        ValueError: if v is not ReasonableUnixTimeMs format
    """
    import pendulum

    if pendulum.parse("2000-01-01T00:00:00Z").int_timestamp * 1000 > v:  # type: ignore[union-attr]
        raise ValueError(f"{v} must be after Jan 1 2000")
    if pendulum.parse("3000-01-01T00:00:00Z").int_timestamp * 1000 < v:  # type: ignore[union-attr]
        raise ValueError(f"{v} must be before Jan 1 3000")


class GtDispatchBooleanLocal(BaseModel):
    """ """

    RelayState: int = Field(
        title="RelayState",
    )
    AboutNodeAlias: str = Field(
        title="AboutNodeAlias",
    )
    FromNodeAlias: str = Field(
        title="FromNodeAlias",
    )
    SendTimeUnixMs: int = Field(
        title="SendTimeUnixMs",
    )
    TypeName: Literal["gt.dispatch.boolean.local"] = "gt.dispatch.boolean.local"
    Version: str = "100"

    @validator("AboutNodeAlias")
    def _check_about_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(
                f"AboutNodeAlias failed LeftRightDot format validation: {e}"
            )
        return v

    @validator("FromNodeAlias")
    def _check_from_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(
                f"FromNodeAlias failed LeftRightDot format validation: {e}"
            )
        return v

    @validator("SendTimeUnixMs")
    def _check_send_time_unix_ms(cls, v: int) -> int:
        try:
            check_is_reasonable_unix_time_ms(v)
        except ValueError as e:
            raise ValueError(
                f"SendTimeUnixMs failed ReasonableUnixTimeMs format validation: {e}"
            )
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class GtDispatchBooleanLocal_Maker:
    type_name = "gt.dispatch.boolean.local"
    version = "100"

    def __init__(
        self,
        relay_state: int,
        about_node_alias: str,
        from_node_alias: str,
        send_time_unix_ms: int,
    ):

        self.tuple = GtDispatchBooleanLocal(
            RelayState=relay_state,
            AboutNodeAlias=about_node_alias,
            FromNodeAlias=from_node_alias,
            SendTimeUnixMs=send_time_unix_ms,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: GtDispatchBooleanLocal) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> GtDispatchBooleanLocal:
        """
        Given a serialized JSON type object, returns the Python class object
        """
        try:
            d = json.loads(t)
        except TypeError:
            raise MpSchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise MpSchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> GtDispatchBooleanLocal:
        d2 = dict(d)
        if "RelayState" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing RelayState")
        if "AboutNodeAlias" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing AboutNodeAlias")
        if "FromNodeAlias" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing FromNodeAlias")
        if "SendTimeUnixMs" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing SendTimeUnixMs")
        if "TypeName" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing TypeName")

        return GtDispatchBooleanLocal(
            RelayState=d2["RelayState"],
            AboutNodeAlias=d2["AboutNodeAlias"],
            FromNodeAlias=d2["FromNodeAlias"],
            SendTimeUnixMs=d2["SendTimeUnixMs"],
            TypeName=d2["TypeName"],
            Version="100",
        )
