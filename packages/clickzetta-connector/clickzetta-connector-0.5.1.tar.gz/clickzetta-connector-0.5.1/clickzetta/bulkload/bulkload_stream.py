import copy
import logging
from enum import Enum
from logging import getLogger
from clickzetta.client import Client
from clickzetta.proto import ingestion_pb2

_logger = getLogger(__name__)

class BulkLoadOperation(Enum):
    APPEND = 1
    UPSERT = 2
    OVERWRITE = 3

class BulkLoadOptions:
    def __init__(self, operation:BulkLoadOperation, partition_specs:str, record_keys:list) -> None:
        self.operation = operation
        self.partition_specs = partition_specs
        self.record_keys = record_keys
        self._properties = {'operation': operation, 'partition_specs': partition_specs, 'record_keys': record_keys}

    def to_api_repr(self) -> dict:
        return copy.deepcopy(self._properties)

# class BulkLoadMetaData:
#     def __init__(self, instance_id:int, info:ingestion_pb2.):
#         self.instance_id = instance_id
#         self.info = info
#
# class BulkLoadStream:
#     def __init__(self, client:Client):