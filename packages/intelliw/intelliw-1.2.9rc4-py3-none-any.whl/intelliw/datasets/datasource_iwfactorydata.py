'''
Author: hexu
Date: 2021-10-14 14:54:05
LastEditTime: 2023-03-09 17:35:06
LastEditors: Hexu
Description: 从数据工场获取模型数据集
FilePath: /iw-algo-fx/intelliw/datasets/datasource_iwfactorydata.py
'''
import math

from intelliw.datasets.datasource_base import AbstractDataSource, DataSourceReaderException
from intelliw.utils import iuap_request
from intelliw.utils.logger import _get_framework_logger
from intelliw.config import config

logger = _get_framework_logger()


def err_handler(request, exception):
    print("请求出错,{}".format(exception))


class DataSourceIwFactoryData(AbstractDataSource):
    """
    数据工场数据源
    """

    def __init__(self, input_address, get_row_address, table_id):
        """
        智能分析数据源
        :param input_address:   获取数据 url
        :param get_row_address: 获取数据总条数 url
        :param table_id:   表Id
        """
        self.input_address = input_address
        self.get_row_address = get_row_address
        self.table_id = table_id
        self.__total = None

    def total(self):
        """获取数据总行数"""
        if self.__total is not None:
            return self.__total
        # print(self.get_row_address, self.table_id)
        data = {'tableid': self.table_id, 'tenantId': config.TENANT_ID}
        response = iuap_request.post_json(
            self.get_row_address, json=data)
        if response.status != 200:
            msg = f"获取行数失败，url: {self.get_row_address}, response: {response}"
            raise DataSourceReaderException(msg)
        row_data = response.json

        self.__total = 0
        try:
            count = row_data["data"]["count"]
            if isinstance(count, int):
                self.__total = count
        except Exception as e:
            msg = f"获取行数返回结果错误, response: {row_data}, request_url: {self.get_row_address}"
            raise DataSourceReaderException(msg)
        return self.__total

    def reader(self, page_size=100, offset=0, limit=0, transform_function=None, dataset_type='train_set'):
        return self.__Reader(self.input_address, self.table_id, self.total(), page_size, offset, limit, transform_function)

    class __Reader:
        def __init__(self, input_address, table_id, total, page_size=100, offset=0, limit=0, transform_function=None):
            """
            eg. 91 elements, page_size = 20, 5 pages as below:
            [0,19][20,39][40,59][60,79][80,90]
            offset 15, limit 30:
            [15,19][20,39][40,44]
            offset 10 limit 5:
            [10,14]
            """
            self.input_address = input_address
            self.table_id = table_id
            self.total_rows = total
            self.limit = limit if limit <= 0 or (
                offset + limit > total) else (total - offset)
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
            self.meta = []

            self.total_read = 0
            self.after_transform = 0

            """
            print("total_page={},start_page={},end_page={},start_index={},end_index={},current_page={}"
                  .format(self.total_page,
                          self.start_page,
                          self.end_page,
                          self.start_index_in_start_page,
                          self.end_index_in_end_page,
                          self.current_page))
            """

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
                if self.current_page == self.start_page or self.current_page == self.end_page:
                    # 首尾页需截取有效内容
                    start_index = 0
                    end_index = len(page['result']) - 1
                    if self.current_page == self.start_page:
                        start_index = self.start_index_in_start_page
                    if self.current_page == self.end_page:
                        end_index = self.end_index_in_end_page
                    page['result'] = page['result'][start_index: end_index + 1]

                self.current_page += 1
                self.total_read += len(page['result'])
                # 检查是否需要使用转换函数
                if self.transform_function is not None:
                    transformed = self.transform_function(page)
                    self.after_transform += len(transformed["result"])
                    return transformed
                self.after_transform = self.total_read
                return page  # 统一格式
            except Exception as e:
                logger.exception(
                    f"智能工场数据源读取失败, input_address: [{self.table_id}]")
                raise DataSourceReaderException('智能工场数据源读取失败') from e

        def _get_meta(self, data):
            if self.meta == []:
                self.meta = [{"code": k} for k in data.keys()]
            return self.meta

        def _data_process(self, data):
            result = []
            if len(data) > 0:
                self._get_meta(data[0])
            for d in data:
                val = []
                [val.append(d.get(k["code"])) for k in self.meta]
                result.append(val)
            return {"result": result, "meta": self.meta}

        def _read_page(self, page_index, page_size):
            """
            数据工场获取数据接口，分页读取数据
            :param page_index: 页码，从 0 开始
            :param page_size:  每页大小

            此接口：pageIndex 代表起始下标（不是页）， pagesize代表每页数据的数量， pagecount代表获取几页
                   但是返回的数据类型是[{},{}] 而不是 [[{},{}],[]], 所以保证pageSize和pageCount中某一个数为1的时候， 另一个参数就可以当size使用（很迷惑）
            例如： {'id': self.table_id, 'pageIndex': 1,'pageSize': 10, 'pageCount': 1} 和 {'id': self.table_id, 'pageIndex': 1,'pageSize': 1, 'pageCount': 10} 的结果完全一致
            :return:
            """
            print("pageIndex: ", page_index, "pageCount:", page_size)
            request_data = {'id': self.table_id,
                            'pageIndex': page_index, 'pageCount': page_size, 'tenantId': config.TENANT_ID}
            response = iuap_request.post_json(
                url=self.input_address, json=request_data, timeout=30)
            response.raise_for_status()
            result = response.json
            return self._data_process(result["data"])
