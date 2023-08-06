import copy
import logging
from enum import Enum
from logging import getLogger
from clickzetta.client import Client
from clickzetta.proto import ingestion_pb2
from clickzetta.bulkload import cz_table

_logger = getLogger(__name__)


class BulkLoadOperation(Enum):
    APPEND = 1
    UPSERT = 2
    OVERWRITE = 3


class BulkLoadOptions:
    def __init__(self, operation: BulkLoadOperation, partition_specs: str, record_keys: list) -> None:
        self.operation = operation
        self.partition_specs = partition_specs
        self.record_keys = record_keys
        self._properties = {'operation': operation, 'partition_specs': partition_specs, 'record_keys': record_keys}

    def to_api_repr(self) -> dict:
        return copy.deepcopy(self._properties)


class BulkLoadMetaData:
    def __init__(self, instance_id: int, info: ingestion_pb2.BulkloadStreamInfo):
        self.instance_id = instance_id
        self.info = info
        self.table = cz_table.CZTable(info.table_meta, info.identifier.schema_name, info.identifier.table_name,
                                      info.table_type)


class BulkLoadStream:
    def __init__(self, client: Client, meta_data: BulkLoadMetaData):
        self.client = client
        self.meta_data = meta_data

    def get_stream_id(self):
        return

    def get_operation(self):
        return

    def get_stream_state(self):
        return

    def get_sql_error(self):
        return

    def get_schema(self):
        return

    def get_table(self):
        return

    def get_record_keys(self):
        return

    def get_partition_specs(self):
        return

    def open_writer(self):
        return

    def commit(self):
        return

    def abort(self):
        return
