'''
Author: Hexu
Date: 2022-03-30 11:47:31
LastEditors: Hexu
LastEditTime: 2023-03-16 17:14:11
FilePath: /iw-algo-fx/intelliw/utils/exception.py
Description: 错误类定义
'''
####### error class #######


import os


class ExceptionNoStack(Exception):
    def ignore_stack(self):
        return True


class PipelineException(Exception):
    pass


class ModelLoadException(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return '''模型加载异常\n
        报错信息: {}\n
        可能原因:\n
        1 是否补全load函数\n
        2 如果使用checkpoint, 检查代码是否正确加载checkpoint\n
        '''.format(self.msg)

    def ignore_stack(self):
        return True


class DatasetException(Exception):
    def ignore_stack(self):
        return True


class InferException(Exception):
    pass


class FeatureProcessException(Exception):
    def ignore_stack(self):
        return True


class DataSourceDownloadException(Exception):
    def ignore_stack(self):
        return True


class LinkServerException(Exception):
    pass


class HttpServerException(Exception):
    pass


class CheckpointException(Exception):
    def __str__(self) -> str:
        return '''
        checkpoint保存模型异常，发生错误的可能：
            1. save()方法在save_checkpoint()方法之前调用,请在训练结束后调用save()方法保存模型
            2. save_checkpoint()方法多次调用
        '''

    def ignore_stack(self):
        return True


class DataCheckException(Exception):
    def __init__(self, file) -> None:
        self.curkey = ""
        self.__put_file__(file)

    def __put_file__(self, file) -> None:
        from intelliw.utils.storage_service import StorageService
        from intelliw.config import config
        import intelliw.utils.message as message
        from intelliw.utils.global_val import gl

        try:
            self.curkey = os.path.join(config.STORAGE_SERVICE_PATH,
                                       config.SERVICE_ID, "data_check.json")
            StorageService(
                self.curkey, config.FILE_UP_TYPE, "upload"
            ).upload(file)
            gl.recorder.report(message.CommonResponse(
                500, 'data_check', 'failed', {'filepath': self.curkey}))
        except Exception as e:
            import logging
            logging.error(f"上传文件错误: {e}")

    def __str__(self) -> str:
        return f'''数据检查错误，错误详情请查看:
        {self.curkey}'''

    def ignore_stack(self):
        return False
