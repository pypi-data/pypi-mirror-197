"""
A module to define the Request type.
"""
from dataclasses import dataclass, field
from enum import Enum, auto
from json import loads
from typing import Any, Dict, Final, List, Tuple, Type

# This is how we know its a SHADY request
SHADYSTR: Final[str] = "ἐπιούσιον"
SHADY_REQ_VERSION: Final[int] = 1


class BaselineValue(Enum):
    # Provided value not found in basline
    NOT_FOUND = auto()


def _update(data: Dict[str, Any], baseline: Dict[str, Any]
            ) -> List[Tuple[str, Type, Type]]:
    """
    Takes baseline and updates any shared attributes with the contents of data.
    If the types do not match in the shared attributes, baseline will not be
    updated. In staid, a tuple of (attribute name, expected, got) will be added
    to the list that is returned.

    :args data: The arguments to pass to the API
    :args baseline: The default args of the API
    :returns: A list of missmatched types
    """
    ret = list()
    for k, v in baseline.items():
        check = data.get(k, BaselineValue.NOT_FOUND)
        if (isinstance(check, Dict)):
            ret.append(_update(check, v))
        elif (check is not BaselineValue.NOT_FOUND):
            if (isinstance(check, type(v))):
                if (k.endswith("_")):
                    tmp = k[:-1]
                    baseline.update({tmp: check})
                    baseline.pop(k)
                else:
                    baseline.update({k: check})
            else:
                ret.append((k, type(v), type(check)))
    return ret


def _check_required(tmp: Dict[str, Any]) -> List[str]:
    """
    Checks to see if there are any values with a name ending in _ (IE it is required)
    in tmp and returns a list of attribute names if any are found.

    :args tmp: The data struck to search through
    :returns: A list of attributes with names that end in _
    """
    ret = list()
    for k, v in tmp.items():
        if (isinstance(v, Dict)):
            ret.append(_check_required(v))
        elif (k.endswith("_")):
            ret.append(k)
    return ret


class BadRequest(Exception):
    """
    Used when a request is received that does not folow the API baseline.
    """
    ...


@dataclass()
class Request():
    """
    Represents a request to a SHADY backend. May be warped in other json as may
    be needed for the webhook provider to work.
    """
    # The name of the api call to pass the data parameter to
    api_call: str
    # The paramters of the request in json
    data: Dict[str, Any]
    # What version of the SHADY Request Standard to process this with
    shady_request_version: int = SHADY_REQ_VERSION
    # How we know this is a Request object in json.
    _type: str = SHADYSTR

    def sanitize(self, baseline: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes the data element and the provied basline and checks that for
        every element in the basline, there is a matching attribute at the same
        location, name, and type in the data element. If these conditions are
        matched it will be added to the output dictionary. If the name and
        location exists in the basline but not the data element, and the name
        does not end in _ (IE it is required), then the value in the basline
        will be used as a default. If it is required, then the BadRequest Error
        will be thrown. In all other cases, if there are extra names /
        locations in the data element, they will be silently dropped.

        :args baseline: The baseline of the API to use (will be coppied) for
        the return value.
        :return: The sanitized baseline
        """
        ret = baseline.copy()
        missed_types = _update(self.data, ret)
        if (len(missed_types)):
            err_str = [f"Misallied type for '{x[0]}':\n\tExpected"
                       f" {x[1]}\n\tGot {x[2]}" for x in missed_types]
            raise BadRequest("\n ".join(err_str))
        remaining_required = _check_required(ret)
        if (len(remaining_required)):
            err_str = [f"Required arg '{x}' not provided."
                       for x in remaining_required]
            raise BadRequest("\n ".join(err_str))
        return ret
