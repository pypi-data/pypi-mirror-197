from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Union

from qm.grpc.qm_api import DigitalInputPortPolarity


@dataclass(frozen=True)
class MixerInfo:
    mixer: str
    frequency_negative: bool
    intermediate_frequency: int = field(default=0)
    intermediate_frequency_double: float = field(default=0.0)
    lo_frequency: int = field(default=0)
    lo_frequency_double: float = field(default=0.0)

    def as_dict(self) -> Dict[str, Union[str, bool, int, float]]:
        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass(frozen=True)
class AnalogOutputPortFilter:
    feedforward: List[float]
    feedback: List[float]


class Polarity(Enum):
    RISING = DigitalInputPortPolarity.RISING
    FALLING = DigitalInputPortPolarity.FALLING
