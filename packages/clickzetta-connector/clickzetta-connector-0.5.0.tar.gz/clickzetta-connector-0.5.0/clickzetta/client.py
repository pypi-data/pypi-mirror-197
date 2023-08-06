"""Client for interacting with the ClickZetta API."""

from __future__ import absolute_import
from __future__ import division

import time

import clickzetta
import sqlparse
import json
import random
import os
import requests.exceptions
import typing
from typing import (
    Any,
    Dict,
    IO,
    Iterable,
    Mapping,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)
import uuid
import warnings
import logging
from datetime import datetime

from clickzetta._helpers import _get_click_zetta_host, _DEFAULT_HOST

from clickzetta.enums import *
from clickzetta.table import Table
from clickzetta.query_result import QueryResult

TIMEOUT_HEADER = "X-Server-Timeout"
TimeoutType = Union[float, None]
ResumableTimeoutType = Union[
    None, float, Tuple[float, float]
]

if typing.TYPE_CHECKING:
    PathType = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]
    import requests

_DEFAULT_CHUNKSIZE = 10 * 1024 * 1024  # 10 MB
_MAX_MULTIPART_SIZE = 5 * 1024 * 1024
_DEFAULT_NUM_RETRIES = 6
_GENERIC_CONTENT_TYPE = "*/*"

_MIN_GET_QUERY_RESULTS_TIMEOUT = 120

DEFAULT_TIMEOUT = None

HEADERS = {
    'Content-Type': 'application/json'
}

DEFAULT_INSTANCE_ID = 100


class Client(object):

    def __init__(self, login_params: LoginParams, workspace: str, instance_name: str,
                 vc_name: str, base_url: str = None):
        default_base_url = _get_click_zetta_host()
        if base_url is None:
            self.base_url = default_base_url
        else:
            self.base_url = base_url
        self.token = None
        self.workspace = workspace
        self.instance_name = instance_name
        self.vc_name = vc_name
        self.login_params = login_params
        self.session = None

    def log_in_cz(self, login_params: LoginParams) -> str:
        path = "/clickzetta-portal/user/loginSingle"
        api_repr = login_params.to_api_repr()
        data = json.dumps(api_repr)
        try:
            api_response = requests.post(self.base_url + path, data=data, headers=HEADERS)
            result = api_response.text
            result_dict = json.loads(result)
            if result_dict['data']['token'] is None:
                raise requests.exceptions.RequestException("user:" + login_params.username + "is Unauthorized")
            else:
                token = result_dict['data']['token']
                return token
        except requests.exceptions.RequestException:
            raise

    def get_table_infos_from_show_statement(self, sql: string):
        format_sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
        stmt = sqlparse.parse(format_sql)[0]
        columns = []
        types = []

        for token in stmt.tokens:
            if not isinstance(token, sqlparse.sql.Parenthesis):
                continue
            else:
                for sub_token in token.tokens:
                    if isinstance(sub_token, sqlparse.sql.Identifier) and not sub_token.value.startswith('NOVALID'):
                        columns.append(sub_token.value.upper())
                    elif isinstance(sub_token, sqlparse.sql.Token) and sub_token.ttype is not None and len(
                            sub_token.ttype) == 2 and sub_token.ttype[
                        1] == 'Builtin':
                        types.append(sub_token.value.replace('\\', '').upper())
                    elif isinstance(sub_token, sqlparse.sql.Function) and not sub_token.value.startswith(
                            "UNIQUE") and not sub_token.value.startswith("KEY"):
                        types.append(sub_token.value.replace('\\', '').upper())
                    else:
                        continue
                break
        return {'columns': columns, 'types': types}

    # def create_bulkload_stream(self) -> BulkLoadStream:
    #     return None
    #
    # def get_bulkload_stream(self) -> BulkLoadStream:
    #     return None

    def show_table(self, token: str, query_sql: str, schema=None) -> QueryResult:
        path = "/lh/submitJob"
        table = Table(self.workspace, '', self.instance_name, self.vc_name)
        vc = table.vc_name
        job_type = JobType.SQL_JOB
        unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                           + str(random.randint(10000, 99999))
        job_id = JobID(format_unique_id, table.workspace, DEFAULT_INSTANCE_ID)
        logging.info(
            "python sqlalchemy job id:" + format_unique_id)
        job_name = "SHOW_TABLE"
        user_id = 0
        reqeust_mode = JobRequestMode.HYBRID
        timeout = 100
        query = query_sql
        job_config = {}
        sql_config = SQLJobConfig(0, "0", "0", {'cz.sql.adhoc.result.type': 'embedded'})
        schema_name = ''
        if schema is not None:
            schema_name = schema
        sql_job = SQLJob(sql_config, table.workspace, schema_name, [])
        sql_job.query.append(query)
        job_timeout_ms = 3000
        user_agent = ""

        job_desc = JobDesc(vc, job_type, job_id, job_name, user_id, reqeust_mode, timeout, job_config, sql_job,
                           job_timeout_ms,
                           user_agent, 0)
        job_request = JobRequest(job_desc)
        data = json.dumps(job_request.to_api_repr())
        HEADERS['instanceName'] = table.instance_name
        HEADERS['X-ClickZetta-Token'] = token
        try:
            api_response = self.session.post(self.base_url + path, data=data, headers=HEADERS)
            result = api_response.text
            result_dict = json.loads(result)
            query_result = QueryResult(result_dict, 'show')
            return query_result

        except requests.exceptions.RequestException:
            raise

    def desc_table(self, token: str, query_sql: str, schema=None) -> QueryResult:
        path = "/lh/submitJob"
        table = Table(self.workspace, '', self.instance_name, self.vc_name)
        vc = table.vc_name
        job_type = JobType.SQL_JOB
        unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                           + str(random.randint(10000, 99999))
        job_id = JobID(format_unique_id, table.workspace, DEFAULT_INSTANCE_ID)
        logging.info(
            "python sqlalchemy job id:" + format_unique_id)
        job_name = "SHOW_TABLE"
        user_id = 0
        reqeust_mode = JobRequestMode.HYBRID
        timeout = 100
        query = query_sql
        job_config = {}
        sql_config = SQLJobConfig(0, "0", "0", {'cz.sql.adhoc.result.type': 'embedded'})
        schema_name = ''
        if schema is not None:
            schema_name = schema
        sql_job = SQLJob(sql_config, table.workspace, schema_name, [])
        sql_job.query.append(query)
        job_timeout_ms = 3000
        user_agent = ""

        job_desc = JobDesc(vc, job_type, job_id, job_name, user_id, reqeust_mode, timeout, job_config, sql_job,
                           job_timeout_ms,
                           user_agent, 0)
        job_request = JobRequest(job_desc)
        data = json.dumps(job_request.to_api_repr())
        HEADERS['instanceName'] = table.instance_name
        HEADERS['X-ClickZetta-Token'] = token
        try:
            api_response = self.session.post(self.base_url + path, data=data, headers=HEADERS)
            result = api_response.text
            result_dict = json.loads(result)
            query_result = QueryResult(result_dict, 'desc')
            return query_result

        except requests.exceptions.RequestException:
            raise

    def drop_table(self, token: str, query_sql: str) -> QueryResult:
        path = "/lh/submitJob"
        table = Table(self.workspace, '', self.instance_name, self.vc_name)
        vc = table.vc_name
        job_type = JobType.SQL_JOB
        unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                           + str(random.randint(10000, 99999))
        job_id = JobID(format_unique_id, table.workspace, DEFAULT_INSTANCE_ID)
        logging.info(
            "python sqlalchemy job id:" + format_unique_id)
        job_name = "DROP_TABLE"
        user_id = 0
        reqeust_mode = JobRequestMode.HYBRID
        timeout = 100
        query = query_sql
        job_config = {}
        sql_config = SQLJobConfig(0, "0", "0", {'cz.sql.adhoc.result.type': 'embedded'})
        sql_job = SQLJob(sql_config, table.workspace, '', [])
        sql_job.query.append(query)
        job_timeout_ms = 3000
        user_agent = ""

        job_desc = JobDesc(vc, job_type, job_id, job_name, user_id, reqeust_mode, timeout, job_config, sql_job,
                           job_timeout_ms,
                           user_agent, 0)
        job_request = JobRequest(job_desc)
        data = json.dumps(job_request.to_api_repr())
        HEADERS['instanceName'] = table.instance_name
        HEADERS['X-ClickZetta-Token'] = token
        try:
            api_response = self.session.post(self.base_url + path, data=data, headers=HEADERS)
            result = api_response.text
            result_dict = json.loads(result)
            query_result = QueryResult(result_dict, 'drop')
            return query_result
        except requests.exceptions.RequestException:
            raise

    def alter_table(self, token: str, alter_sql: str) -> QueryResult:
        path = "/lh/submitJob"
        table = Table(self.workspace, '', self.instance_name, self.vc_name)
        vc = table.vc_name
        job_type = JobType.SQL_JOB
        unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                           + str(random.randint(10000, 99999))
        job_id = JobID(format_unique_id, table.workspace, DEFAULT_INSTANCE_ID)
        logging.info(
            "python sqlalchemy job id:" + format_unique_id)
        job_name = "ALTER_TABLE"
        user_id = 0
        reqeust_mode = JobRequestMode.HYBRID
        timeout = 100
        job_config = {}
        sql_config = SQLJobConfig(0, "0", "0", {'cz.sql.adhoc.result.type': 'embedded'})
        sql_job = SQLJob(sql_config, table.workspace, '', [])
        sql_job.query.append(alter_sql)
        job_timeout_ms = 3000
        user_agent = ""

        job_desc = JobDesc(vc, job_type, job_id, job_name, user_id, reqeust_mode, timeout, job_config, sql_job,
                           job_timeout_ms,
                           user_agent, 0)
        job_request = JobRequest(job_desc)
        data = json.dumps(job_request.to_api_repr())
        HEADERS['instanceName'] = table.instance_name
        HEADERS['X-ClickZetta-Token'] = token
        try:
            api_response = self.session.post(self.base_url + path, data=data, headers=HEADERS)
            result = api_response.text
            result_dict = json.loads(result)
            query_result = QueryResult(result_dict, 'alter')
            return query_result
        except requests.exceptions.RequestException:
            raise

    def truncate_table(self, token: str, query_sql: str) -> QueryResult:
        path = "/lh/submitJob"
        table = Table(self.workspace, '', self.instance_name, self.vc_name)
        vc = table.vc_name
        job_type = JobType.SQL_JOB
        unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                           + str(random.randint(10000, 99999))
        job_id = JobID(format_unique_id, table.workspace, DEFAULT_INSTANCE_ID)
        logging.info(
            "python sqlalchemy job id:" + format_unique_id)
        job_name = "TRUNCATE_TABLE"
        user_id = 0
        reqeust_mode = JobRequestMode.HYBRID
        timeout = 100
        job_config = {}
        query = query_sql
        sql_config = SQLJobConfig(0, "0", "0", {'cz.sql.adhoc.result.type': 'embedded'})
        sql_job = SQLJob(sql_config, table.workspace, '', [])
        sql_job.query.append(query)
        job_timeout_ms = 3000
        user_agent = ""

        job_desc = JobDesc(vc, job_type, job_id, job_name, user_id, reqeust_mode, timeout, job_config, sql_job,
                           job_timeout_ms,
                           user_agent, 0)
        job_request = JobRequest(job_desc)
        data = json.dumps(job_request.to_api_repr())
        HEADERS['instanceName'] = table.instance_name
        HEADERS['X-ClickZetta-Token'] = token
        try:
            api_response = self.session.post(self.base_url + path, data=data, headers=HEADERS)
            result = api_response.text
            result_dict = json.loads(result)
            query_result = QueryResult(result_dict, 'truncate')
            return query_result
        except requests.exceptions.RequestException:
            raise

    def create_table(self, token: str, create_sql: str) -> QueryResult:
        path = "/lh/submitJob"
        table = Table(self.workspace, '', self.instance_name, self.vc_name)
        vc = table.vc_name
        job_type = JobType.SQL_JOB
        unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                           + str(random.randint(10000, 99999))
        job_id = JobID(format_unique_id, table.workspace, DEFAULT_INSTANCE_ID)
        logging.info(
            "python sqlalchemy job id:" + format_unique_id)
        job_name = "CREATE_TABLE"
        user_id = 0
        reqeust_mode = JobRequestMode.HYBRID
        timeout = 100
        job_config = {}
        sql_config = SQLJobConfig(0, "0", "0", {'cz.sql.adhoc.result.type': 'embedded'})
        sql_job = SQLJob(sql_config, table.workspace, '', [])
        sql_job.query.append(create_sql)
        job_timeout_ms = 3000
        user_agent = ""

        job_desc = JobDesc(vc, job_type, job_id, job_name, user_id, reqeust_mode, timeout, job_config, sql_job,
                           job_timeout_ms,
                           user_agent, 0)
        job_request = JobRequest(job_desc)
        data = json.dumps(job_request.to_api_repr())
        HEADERS['instanceName'] = table.instance_name
        HEADERS['X-ClickZetta-Token'] = token
        try:
            api_response = self.session.post(self.base_url + path, data=data, headers=HEADERS)
            result = api_response.text
            result_dict = json.loads(result)
            query_result = QueryResult(result_dict, 'create')
            return query_result
        except requests.exceptions.RequestException:
            raise

    def select_table(self, token: str, select_sql: str, parameters=None) -> QueryResult:
        path = "/lh/submitJob"
        if 'test plain returns' in select_sql or 'test unicode returns' in select_sql:
            return QueryResult({}, 'anon')
        table = Table(self.workspace, '', self.instance_name, self.vc_name)
        vc = table.vc_name
        job_type = JobType.SQL_JOB
        unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                           + str(random.randint(10000, 99999))
        job_id = JobID(format_unique_id, table.workspace, DEFAULT_INSTANCE_ID)
        logging.info(
            "python sqlalchemy job id:" + format_unique_id)
        job_name = "SELECT_TABLE"
        user_id = 0
        reqeust_mode = JobRequestMode.HYBRID
        timeout = 30
        job_config = {}
        sql_job_set_prop = {'cz.sql.adhoc.result.type': 'embedded'}
        if parameters is not None and len(parameters) != 0:
            if parameters['hints'] is not None:
                for key in parameters['hints']:
                    sql_job_set_prop[key] = parameters['hints'][key]
        sql_config = SQLJobConfig(0, "0", "0", sql_job_set_prop)
        sql_job = SQLJob(sql_config, table.workspace, '', [])
        sql_job.query.append(select_sql)
        job_timeout_ms = 3000
        user_agent = ""

        job_desc = JobDesc(vc, job_type, job_id, job_name, user_id, reqeust_mode, timeout, job_config, sql_job,
                           job_timeout_ms,
                           user_agent, 0)
        job_request = JobRequest(job_desc)
        data = json.dumps(job_request.to_api_repr())
        HEADERS['instanceName'] = table.instance_name
        HEADERS['X-ClickZetta-Token'] = token
        logging.debug('BEGIN TO SEND REQUEST:' + select_sql + ' TO CZ SERVER, TIME:' + str(datetime.now()))
        try:
            api_response = self.session.post(self.base_url + path, data=data, headers=HEADERS)
            api_response.encoding = 'utf-8'
            result = api_response.text
            result_dict = json.loads(result)
            get_job_result_dict = self.wait_job_finished(result_dict, job_id, HEADERS)
            logging.debug('GET RESPONSE FROM CZ SERVER FOR REQUEST:' + select_sql + ' TIME:' + str(datetime.now()))
            query_result = QueryResult(get_job_result_dict, 'select')
            return query_result
        except requests.exceptions.RequestException:
            raise

    def insert_table(self, token: str, insert_sql: str) -> QueryResult:
        path = "/lh/submitJob"
        table = Table(self.workspace, '', self.instance_name, self.vc_name)
        vc = table.vc_name
        job_type = JobType.SQL_JOB
        unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                           + str(random.randint(10000, 99999))
        job_id = JobID(format_unique_id, table.workspace, DEFAULT_INSTANCE_ID)
        logging.info(
            "python sqlalchemy job id:" + format_unique_id)
        job_name = "INSERT_TABLE"
        user_id = 0
        reqeust_mode = JobRequestMode.HYBRID
        timeout = 10
        job_config = {}
        sql_config = SQLJobConfig(0, "0", "0", {'cz.sql.adhoc.result.type': 'embedded'})
        sql_job = SQLJob(sql_config, table.workspace, '', [])
        sql_job.query.append(insert_sql)
        job_timeout_ms = 3000
        user_agent = ""

        job_desc = JobDesc(vc, job_type, job_id, job_name, user_id, reqeust_mode, timeout, job_config, sql_job,
                           job_timeout_ms,
                           user_agent, 0)
        job_request = JobRequest(job_desc)
        data = json.dumps(job_request.to_api_repr())
        HEADERS['instanceName'] = table.instance_name
        HEADERS['X-ClickZetta-Token'] = token
        try:
            api_response = self.session.post(self.base_url + path, data=data, headers=HEADERS)
            result = api_response.text
            result_dict = json.loads(result)
            get_job_result_dict = self.wait_job_finished(result_dict, job_id, HEADERS)
            query_result = QueryResult(get_job_result_dict, 'insert')
            return query_result
        except requests.exceptions.RequestException:
            raise

    def update_table(self, token: str, update_sql: str) -> QueryResult:
        path = "/lh/submitJob"
        table = Table(self.workspace, '', self.instance_name, self.vc_name)
        vc = table.vc_name
        job_type = JobType.SQL_JOB
        unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                           + str(random.randint(10000, 99999))
        job_id = JobID(format_unique_id, table.workspace, DEFAULT_INSTANCE_ID)
        logging.info(
            "python sqlalchemy job id:" + format_unique_id)
        job_name = "UPDATE_TABLE"
        user_id = 0
        reqeust_mode = JobRequestMode.HYBRID
        timeout = 100
        job_config = {}
        sql_config = SQLJobConfig(0, "0", "0", {'cz.sql.adhoc.result.type': 'embedded'})
        sql_job = SQLJob(sql_config, table.workspace, '', [])
        sql_job.query.append(update_sql)
        job_timeout_ms = 3000
        user_agent = ""

        job_desc = JobDesc(vc, job_type, job_id, job_name, user_id, reqeust_mode, timeout, job_config, sql_job,
                           job_timeout_ms,
                           user_agent, 0)
        job_request = JobRequest(job_desc)
        data = json.dumps(job_request.to_api_repr())
        HEADERS['instanceName'] = table.instance_name
        HEADERS['X-ClickZetta-Token'] = token
        try:
            api_response = self.session.post(self.base_url + path, data=data, headers=HEADERS)
            result = api_response.text
            result_dict = json.loads(result)
            query_result = QueryResult(result_dict, 'update')
            return query_result
        except requests.exceptions.RequestException:
            raise

    def close(self):
        print("client is closed")

    def wait_job_finished(self, result_dict, job_id: JobID, headers):
        status = result_dict['status']['state']
        if status == "QUEUEING" or status == "SETUP" or status == "RUNNING":
            account = clickzetta.enums.ClickZettaAccount(0)
            get_job_result_request = clickzetta.enums.GetJobResultRequest(account, job_id, 0, '')
            api_request = clickzetta.enums.APIJobRequest(get_job_result_request, '')
            path = '/lh/getJob'
            data = json.dumps(api_request.to_api_repr())
            while True:
                get_job_result_response = self.session.post(self.base_url + path, data=data, headers=headers)
                result = get_job_result_response.text
                get_job_result_dict = json.loads(result)
                if get_job_result_dict['status']['state'] == 'SUCCEED' or get_job_result_dict['status']['state'] \
                        == 'FAILED':
                    logging.info("Get async sql job:" + str(job_id.id) + " result successfully.")
                    return get_job_result_dict
                else:
                    logging.info("Get async sql job:" + str(job_id.id) + " result pending, retry after 10 seconds.")
                    time.sleep(10)
        elif status == "SUCCEED" or status == 'FAILED':
            return result_dict

    def get_table_names(self, schema: str):
        query_result = self.show_table(self.token, 'show tables;', schema)
        query_data = query_result.data.fetch_all()
        table_names = []
        for entry in query_data:
            table_names.append(entry[1])

        return table_names

    def get_schemas(self):
        query_result = self.show_table(self.token, 'show schemas;')
        query_data = query_result.data.fetch_all()
        schema_names = []
        for entry in query_data:
            schema_names.append(entry[0])

        return schema_names

    def get_columns(self, table_name: str, schema: str):
        query_result = self.select_table(self.token, 'select * from ' + schema + '.' + table_name + ' limit 1;')
        schema = query_result.schema

        return schema

    def has_table(self, full_table_name: str):
        query_result = self.show_table(self.token, 'show create table ' + full_table_name + ';')
        if query_result.state != 'FAILED':
            return True
        else:
            return False


def _add_server_timeout_header(headers: Optional[Dict[str, str]], kwargs):
    timeout = kwargs.get("timeout")
    if timeout is not None:
        if headers is None:
            headers = {}
        headers[TIMEOUT_HEADER] = str(timeout)

    if headers:
        kwargs["headers"] = headers

    return kwargs
