from typing import List, Union

from datagen_protocol.validation.humans.human import HumanDatapoint as ValidationHumanDatapoint
from datagen_protocol.schema import request as core_request_schema, DataSequence


class DataRequest(core_request_schema.DataRequest):
    datapoints: List[Union[DataSequence, ValidationHumanDatapoint]]


core_request_schema.DataRequest = DataRequest
