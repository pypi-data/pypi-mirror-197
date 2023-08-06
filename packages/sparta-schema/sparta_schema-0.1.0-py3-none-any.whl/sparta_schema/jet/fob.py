from pydantic.dataclasses import dataclass
from pydantic import StrictFloat, StrictStr, validator


@dataclass
class JetFob:
    sparta_route_code: StrictStr
    load_region: StrictStr
    load_port: StrictStr
    discharge_port: StrictStr
    vessel_type: StrictStr
    spec: StrictStr
    units: StrictStr
    load_from: StrictStr
    load_to: StrictStr
    cash_diff: StrictStr
    structure: StrictFloat
    price: StrictFloat
    price_unrounded: StrictFloat

    @validator('price')
    def assert_positive(cls, v):
        if v < 0:
            raise ValueError('must be a positive number')
        return v
