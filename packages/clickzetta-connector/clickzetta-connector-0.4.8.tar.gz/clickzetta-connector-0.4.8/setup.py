import io
import os
import shutil
import subprocess

import setuptools

PROJECT_SRC_DIR = os.path.abspath(os.path.join(os.getcwd(), "../../.."))
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROTO_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "clickzetta/proto/source_file"))
PROTO_OUT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "clickzetta/proto"))


def delete_proto_source_file(path):
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))


proto_files = [
    "proto/table_meta.proto",
    "proto/metadata_entity.proto",
    "proto/account.proto",
    "proto/role_meta.proto",
    "proto/job_meta.proto",
    "proto/workspace_meta.proto",
    "proto/virtual_cluster_meta.proto",
    "proto/virtual_cluster.proto",
    "proto/virtual_cluster_size.proto",
    "proto/schema.proto",
    "proto/data_type.proto",
    "proto/file_meta_data.proto",
    "proto/operator.proto",
    "proto/object_identifier.proto",
    "proto/expression.proto",
    "proto/table_common.proto",
    "proto/file_format_type.proto",
    "proto/statistics.proto",
    "proto/input_split.proto",
    "proto/file_system.proto",
    "proto/property.proto",
    "proto/bucket_info.proto",
    "proto/virtual_value_info.proto",
    "proto/rm_app_meta.proto",
    "proto/share_meta.proto",
    "proto/function_meta.proto",
    "proto/connection_meta.proto",
    "proto/job_result_cache_meta.proto",
    "proto/network_policy.proto",
    "storage/ingestion/proto/ingestion.proto",
    "storage/ingestion/proto/kudu_common.proto",
    "storage/ingestion/proto/row_operations.proto",
    "storage/ingestion/proto/hash.proto",
    "storage/ingestion/proto/compression.proto",
    "storage/ingestion/proto/block_bloom_filter.proto",
    "storage/ingestion/proto/pb_util.proto"
]

delete_proto_source_file(PROTO_DIR)

for proto_file in proto_files:
    shutil.copy2(os.path.join(PROJECT_SRC_DIR, proto_file), PROTO_DIR)

for source_file in os.listdir(PROTO_DIR):
    subprocess.call(
        'python -m grpc_tools.protoc -I . --python_out=' + PROTO_OUT_DIR + ' --grpc_python_out=' + PROTO_OUT_DIR
        + ' --proto_path=' + PROTO_DIR + ' '
        + os.path.abspath(os.path.join(PROTO_DIR, source_file)), shell=True)

delete_proto_source_file(PROTO_DIR)
# Package metadata.

name = "clickzetta-connector"
description = "clickzetta python connector"

# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 3 - Alpha"
dependencies = [
    "proto-plus >= 1.22.0, <2.0.0dev",
    "packaging >= 14.3, <24.0.0dev",
    "protobuf>=3.19.5,<5.0.0dev,!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5",
    "python-dateutil >= 2.7.2, <3.0dev",
    "requests >= 2.21.0, < 3.0.0dev",
]
extras = {
    "pandas": ["pandas>=1.0.0", "db-dtypes>=0.3.0,<2.0.0dev"],
    "ipywidgets": ["ipywidgets==7.7.1"],
    "geopandas": ["geopandas>=0.9.0, <1.0dev", "Shapely>=1.6.0, <2.0dev"],
    "ipython": ["ipython>=7.0.1,!=8.1.0"],
    "tqdm": ["tqdm >= 4.7.4, <5.0.0dev"],
}

all_extras = []

for extra in extras:
    all_extras.extend(extras[extra])

extras["all"] = all_extras

# Setup boilerplate below this line.

package_root = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(package_root, "clickzetta/version.py")) as fp:
    exec(fp.read(), version)
version = version["__version__"]

packages = ['clickzetta', 'clickzetta.dbapi', 'clickzetta.bulkload', 'clickzetta.proto', 'clickzetta.proto.source_file']

setuptools.setup(
    name=name,
    version=version,
    description=description,
    url='https://www.zettadecision.com/',
    author="mocun",
    author_email="hanmiao.li@clickzetta.com",
    platforms="Posix; MacOS X;",
    packages=packages,
    install_requires=dependencies,
    extras_require=extras,
    python_requires=">=3.7, <3.11",
    include_package_data=True,
    zip_safe=False,
)
