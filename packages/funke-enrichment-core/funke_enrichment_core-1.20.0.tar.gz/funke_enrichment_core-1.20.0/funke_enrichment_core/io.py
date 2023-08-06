# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 10:46:51 2023

@author: Friedrich.Schmidt
"""

import asyncio
from datetime import datetime
from dateutil.parser import parse as datetime_parser
from funke_enrichment_core.helper import publish_data_to_pubsub_topic, warning, err
from google.cloud import bigquery
from google.api_core.exceptions import NotFound as NotFoundException


class InitPayload():
    """
    dummy class to get init input data
    """
    def __init__(self, payload):
        self.payload = payload

    async def process(self, inp_data):
        return self.payload


# class WriteToBigQuery():
#     """
#     Class to write to BQ
#     """
#     def __init__(self, table_path, table_schema, write_disposition,
#                  auto_type_casting=True, default_missing_columns=False, timeout=180):
#         self.table = table_path
#         self.job_config = bigquery.LoadJobConfig(schema=table_schema,
#                                                  write_disposition=write_disposition,
#                                                  allow_jagged_rows=default_missing_columns
#                                                 )
#         self.default_missing_columns = default_missing_columns
#         self.auto_type_casting = auto_type_casting
#         self.type_casting_mapping = {'INTEGER': int,
#                                      'STRING': str,
#                                      'FLOAT': float,
#                                      'BOOLEAN': bool,
#                                      'TIMESTAMP': datetime_parser,
#                                      'DATETIME': datetime_parser,
#                                      'RECORD': dict}
#         if isinstance(timeout, int):
#             self.timeout = timeout * 2
#         else:
#             self.timeout = 180
#
#
#     def _type_casting(self, data, schema):
#         for field in schema:
#             try:
#                 data_field = data[field.name]
#             except Exception as e:
#                 if field.mode != 'REQUIRED' and self.default_missing_columns:
#                     data_field = None
#                 else:
#                     err_msg = str(e) + ': Consider activating "default_missing_columns and check if field' \
#                                        ' "{}" is not "REQUIRED" for table "{}"'.format(field.name, self.table)
#                     raise bigquery.exceptions.BigQueryError(err_msg)
#             if data_field is not None:
#                 try:
#                     caster = self.type_casting_mapping[field.field_type]
#                 except Exception:
#                     caster = warning('Field "{}" of type "{}" can not be casted automatically '
#                                       'for table "{}"!'.format(field.name, field.field_type, self.table))
#                 try:
#                     if caster == dict:
#                         if field.mode == 'REPEATED':
#                             data[field.name] = [self._type_casting(entry, field.fields) for entry in data_field]
#                         else:
#                             data[field.name] = self._type_casting(data_field, field.fields)
#                     elif caster is not None:
#                         if field.mode == 'REPEATED':
#                             data[field.name] = [caster(entry) for entry in data_field]
#                         else:
#                             if caster == datetime_parser:
#                                 cast_to_type = datetime
#                             else:
#                                 cast_to_type = caster
#                             if type(data_field) != cast_to_type:
#                                 data[field.name] = caster(data_field)
#                 except Exception as e:
#                     warning('Failed to cast field "{}" of table "{}": '.format(field.name, self.table) + str(e))
#
#         return data
#
#
#     async def process(self, inp_data):
#         if self.auto_type_casting:
#             inp_data = self._type_casting(inp_data, self.job_config.schema)
#         job_future = save_dict_as_row_to_bq(inp_data, self.table, self.job_config)
#         await asyncio.sleep(0.1)
#         for _ in range(self.timeout):
#             if job_future.done():
#                 res = job_future.exception()
#                 if res is None:
#                     return {self.table: True}
#                 else:
#                     return {self.table: res}
#             else:
#                 await asyncio.sleep(0.5)
#
#         job_future.cancel()
#         raise TimeoutError('Failed finishing write to BigQuery job within {} seconds'.format(self.timeout))
        

class WriteToBigQuery():
    """
    Class to write to BQ
    """
    #TODO: richtiges truncate einbauen
    def __init__(self, table_path, table_schema, drop_table=False, ignore_unknown_values=False,
                 auto_type_casting=False, default_missing_columns=False, retry_timeout=180):
        self.bq_client = bigquery.Client()
        self.table_schema = bigquery.LoadJobConfig(schema=table_schema).schema
        self.table = self._get_table(table_path, drop_table)
        self.ignore_unkown_values = ignore_unknown_values
        self.default_missing_columns = default_missing_columns
        self.auto_type_casting = auto_type_casting
        self.type_casting_mapping = {'INTEGER': int,
                                     'STRING': str,
                                     'FLOAT': float,
                                     'BOOLEAN': bool,
                                     'TIMESTAMP': datetime_parser,
                                     'DATETIME': datetime_parser,
                                     'RECORD': dict}
        self.timeout = retry_timeout

    def _get_table(self, table_id, drop_table):
        if drop_table:
            self.bq_client.delete_table(table_id, not_found_ok=True)
        try:
            table = self.bq_client.get_table(table_id)
        except NotFoundException:
            table = bigquery.Table(table_id, schema=self.table_schema)
            if not self.bq_client.create_table(table) == table:
                raise SystemError('It seems there was an error creating the table "{}"!'.format(table_id))

        return table

    def _type_casting(self, data):
        for field in self.table_schema:
            try:
                data_field = data[field.name]
            except Exception as e:
                if field.mode != 'REQUIRED' and self.default_missing_columns:
                    data_field = None
                else:
                    err_msg = str(e) + ': Consider activating "default_missing_columns and check if field' \
                                       ' "{}" is not "REQUIRED" for table "{}"'.format(field.name, self.table)
                    raise bigquery.exceptions.BigQueryError(err_msg)
            if data_field is not None:
                try:
                    caster = self.type_casting_mapping[field.field_type]
                except Exception:
                    caster = warning('Field "{}" of type "{}" can not be casted automatically '
                                      'for table "{}"!'.format(field.name, field.field_type, self.table))
                try:
                    if caster == dict:
                        if field.mode == 'REPEATED':
                            data[field.name] = [self._type_casting(entry, field.fields) for entry in data_field]
                        else:
                            data[field.name] = self._type_casting(data_field, field.fields)
                    elif caster is not None:
                        if field.mode == 'REPEATED':
                            data[field.name] = [caster(entry) for entry in data_field]
                        else:
                            if caster == datetime_parser:
                                cast_to_type = datetime
                            else:
                                cast_to_type = caster
                            if type(data_field) != cast_to_type:
                                data[field.name] = caster(data_field)
                except Exception as e:
                    warning('Failed to cast field "{}" of table "{}": '.format(field.name, self.table) + str(e))

        return data


    async def process(self, inp_data):
        if self.auto_type_casting:
            inp_data = self._type_casting(inp_data)
        try:
            errors = self.bq_client.insert_rows_json(table=self.table,
                                                     json_rows=[inp_data],
                                                     ignore_unknown_values=self.ignore_unkown_values,
                                                     timeout=self.timeout)
        except Exception as err_msg:
            errors = err_msg

        if errors:
            err(str(errors))
        return {self.topic_path: errors}


class PublishOnPubSubTopic():
    """
    Class to publish to a pubsub topic
    """
    def __init__(self, topic_path, filter_attrs, retry_timeout=180):
        self.topic_path = topic_path
        self.filter_attrs = filter_attrs
        self.timeout = retry_timeout

    def _make_dict_json_serializable(self, json_dict):
        for key, value in json_dict.items():
            if isinstance(value, datetime):
                json_dict[key] = value.strftime("%Y-%m-%dT%H:%M:%S")
            elif isinstance(value, dict):
                json_dict[key] = self._make_dict_json_serializable(value)
            else:
                json_dict[key] = value

        return json_dict

    async def process(self, inp_data):
        pubsub_dict = self._make_dict_json_serializable(inp_data)
        job_future = publish_data_to_pubsub_topic(self.topic_path, pubsub_dict, self.filter_attrs)
        try:
            return {self.topic_path: job_future.result(timeout=self.timeout)}
        except Exception as e:
            return {self.topic_path: err(str(e))}
