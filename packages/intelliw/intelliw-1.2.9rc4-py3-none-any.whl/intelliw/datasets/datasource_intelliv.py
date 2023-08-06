'''
Author: hexu
Date: 2021-10-14 14:54:05
LastEditTime: 2023-03-10 14:45:59
LastEditors: Hexu
Description: 从智能服务获取模型数据集
FilePath: /iw-algo-fx/intelliw/datasets/datasource_intelliv.py
'''
import math
import time

from intelliw.datasets.datasource_base import AbstractDataSource, DataSourceReaderException

from intelliw.utils import iuap_request
from intelliw.utils.logger import _get_framework_logger
from intelliw.config import config

logger = _get_framework_logger()


class DataSourceIntelliv(AbstractDataSource):
    """
    智能分析数据源
    """

    def __init__(self, input_address, get_row_address, input_model_id):
        """
        智能分析数据源
        :param input_address:   获取数据 url
        :param get_row_address: 获取数据总条数 url
        :param input_model_id:  读取的数据模型
        TODO add transformer
        TODO input_address = ${intelliv_host}/ds/model/result
        TODO get_row_address = ${intelliv_host}/ds/getRowCount/${input_model_id}/null
        """
        self.input_address = input_address
        self.get_row_address = get_row_address
        self.input_model_id = input_model_id
        self.__total = None

    def total(self):
        if self.__total is not None:
            return self.__total
        response = iuap_request.get(self.get_row_address)

        if 200 != response.status or response.json is None:
            msg = "获取行数失败，url: {}, response: {}".format(
                self.get_row_address, response)
            raise DataSourceReaderException(msg)

        row_data = response.json
        self.__total = row_data['data']
        if not isinstance(self.__total, int):
            msg = "获取行数返回结果错误, response: {}, request_url: {}".format(
                row_data, self.get_row_address)
            raise DataSourceReaderException(msg)
        return self.__total

    def reader(self, page_size=100000, offset=0, limit=0, transform_function=None, dataset_type='train_set'):
        return self.__Reader(self.input_address, self.input_model_id, self.total(), page_size, offset, limit, transform_function)

    class __Reader:
        def __init__(self, input_address, input_model_id, total, page_size=10000, offset=0, limit=0, transform_function=None):
            """
            eg. 91 elements, page_size = 20, 5 pages as below:
            [0,19][20,39][40,59][60,79][80,90]
            offset 15, limit 30:
            [15,19][20,39][40,44]
            offset 10 limit 5:
            [10,14]
            """
            self.input_address = input_address
            self.input_model_id = input_model_id
            self.limit = limit
            self.total_rows = total
            if limit <= 0:
                self.limit = total - offset
            elif offset + limit > total:
                self.limit = total - offset
            self.page_size = page_size if page_size < self.limit else self.limit
            self.total_page = math.ceil(total / self.page_size)
            self.start_page = math.ceil(
                offset / self.page_size) if offset > 0 else 1
            self.end_page = math.ceil((offset + self.limit) / page_size)
            self.start_index_in_start_page = offset - \
                (self.start_page - 1) * page_size
            self.end_index_in_end_page = offset + \
                self.limit - 1 - (self.end_page - 1) * page_size
            self.current_page = self.start_page

            self.transform_function = transform_function

            self.total_read = 0
            self.after_transform = 0
            self.meta = []

        def get_data_bar(self):
            """数据拉取进度条"""
            if self.current_page % 5 == 1:
                try:
                    proportion = round(
                        (self.total_read/self.total_rows)*100, 2)
                    logger.info(
                        f"数据获取中: 共{self.total_rows}条数据, 已获取{self.total_read}条, 进度{proportion}%")
                except:
                    pass

        @property
        def iterable(self):
            return True

        def __iter__(self):
            return self

        def __next__(self):
            if self.current_page > self.end_page:
                logger.info('共读取原始数据 {} 条，经特征工程处理后数据有 {} 条'.format(
                    self.total_read, self.after_transform))
                raise StopIteration

            self.get_data_bar()

            try:
                page = self._read_page(self.current_page, self.page_size)
                assert page is not None

                # 首尾页需截取有效内容
                if self.current_page == self.start_page or self.current_page == self.end_page:
                    start_index = 0
                    end_index = len(page['result']) - 1
                    if self.current_page == self.start_page:
                        start_index = self.start_index_in_start_page
                        self.meta = page['meta']
                    if self.current_page == self.end_page:
                        end_index = self.end_index_in_end_page
                    page['result'] = page['result'][start_index: end_index + 1]

                self.total_read += len(page['result'])
                self.current_page += 1
                if self.transform_function is not None:
                    transformed = self.transform_function(page)
                    self.after_transform += len(transformed['result'])
                    return transformed
                self.after_transform = self.total_read
                return page
            except Exception as e:
                logger.exception("智能分析数据源读取失败, input_address: [{}], model_id: [{}]".
                                 format(self.input_address, self.input_model_id))
                raise DataSourceReaderException('智能分析数据源读取失败') from e

        def _read_page(self, page_index, page_size):
            """
            调用智能分析接口，分页读取数据
            :param page_index: 页码，从 1 开始
            :param page_size:  每页大小
            :return:
            """
            request_data = {
                "modelId": self.input_model_id,
                "pager": {
                    "pageIndex": page_index,
                    "pageSize": page_size,
                    "pageCount": 0,
                    "recordCount": 0
                },
                "signDTO": {"ak": config.ACCESS_KEY,
                            "sign": config.ACCESS_SECRET,
                            "ts": int(time.time() * 1000)}
            }
            response = iuap_request.post_json(
                url=self.input_address, json=request_data, params={"AuthSdkServer": "true"}, timeout=30)
            response.raise_for_status()
            return response.json
