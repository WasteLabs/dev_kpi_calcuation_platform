from copy import deepcopy
import logging
from typing import Any

from pydantic import BaseModel
from pydantic import Field

from .models import Schema


schema = Schema()


class AbstractParameters(BaseModel):

    def url_parameters(self):
        params = self.__dict__
        params = list(
            map(
                lambda x, y: f"{x}={y}",
                params.keys(),
                params.values(),
            ),
        )
        return "?" + "&".join(params)


class AbstractParser(BaseModel):
    content: dict[str, Any] = Field(description="Response content")

    def __generate_exc(self, key_sequence: list[str]):
        msg = f"Incorrect key in key sequence: {key_sequence}"
        logging.error(msg)
        raise RuntimeError(msg)

    def _get_key_seq_value(
            self,
            content: dict[str, Any],
            key_sequence: list[str],
    ) -> Any:
        value = deepcopy(content)
        try:
            for key in key_sequence:
                value = value[key]
            return value
        except KeyError:
            self.__generate_exc(key_sequence=key_sequence)
        except TypeError:
            self.__generate_exc(key_sequence=key_sequence)
        except IndexError:
            self.__generate_exc(key_sequence=key_sequence)
