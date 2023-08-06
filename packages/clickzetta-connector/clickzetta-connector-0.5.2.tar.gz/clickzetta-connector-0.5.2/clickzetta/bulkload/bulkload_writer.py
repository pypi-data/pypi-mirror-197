import string
import oss2
from clickzetta.proto import ingestion_pb2
from clickzetta.client import Client
from clickzetta.bulkload.bulkload_stream import BulkLoadMetaData

MAX_NUM_ROWS_PER_FILE = 64 << 20
MAX_FILE_SIZE_IN_BYTES_PER_FILE = 256 << 20


class StagingConfig:
    def __init__(self, path: string, id: string, secret: string, token: string, endpoint: string):
        self.path = path
        self.id = id
        self.secret = secret
        self.token = token
        self.endpoint = endpoint

    def create_oss_io(self):
        auth = oss2.Auth(self.id, self.secret)
        bucket = oss2.Bucket(auth, self.endpoint, self.token)
        return bucket


class BulkLoadConfig:
    def __init__(self, config: ingestion_pb2.BulkloadStreamWriterConfig):
        self.config = config

    def get_staging_config(self):
        staging_path = self.config.staging_path
        oss_path = staging_path.path_info.oss_path
        staging_config = StagingConfig(oss_path.path, oss_path.sts_ak_id, oss_path.sts_ak_secret, oss_path.sts_token,
                                       oss_path.oss_endpoint)
        return staging_config

    def get_file_format(self):
        return self.config.file_format

    def get_max_rows_per_file(self):
        if self.config.max_num_rows_per_file > 0:
            return self.config.max_num_rows_per_file
        return MAX_NUM_ROWS_PER_FILE

    def get_max_file_size_per_file(self):
        if self.config.max_size_in_bytes_per_file > 0:
            return self.config.max_size_in_bytes_per_file
        return MAX_FILE_SIZE_IN_BYTES_PER_FILE


class BulkLoadWriter:
    def __init__(self, client: Client, meta_data: BulkLoadMetaData, config: BulkLoadConfig, partition_id: int):
        self.client = client
        self.meta_data = meta_data
        self.config = config
        self.partition_id = partition_id
        self.oss_io = config.get_staging_config().create_oss_io()
        self.file_format = config.get_file_format()
        self.max_file_records = config.get_max_rows_per_file()
        self.max_file_size = config.get_max_file_size_per_file()

    def get_stream_id(self):
        return

    def get_operation(self):
        return

    def get_schema(self):
        return

    def get_table(self):
        return

    def get_partition_id(self):
        return

    def create_row(self):
        return

    def write(self):
        return

    def finish(self):
        return

    def abort(self):
        return
