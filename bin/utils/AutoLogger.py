import os
import time
import logging
from logging.handlers import RotatingFileHandler


class AutoLoggerClass:
    """自动记录日志的类

    Methods
    _______
    __init__()
        初始化日志记录器
    debug(message: str)
        记录调试信息
    info(message: str)
        记录正常信息
    warning(message: str)
        记录警告信息
    error(message: str)
        记录错误信息
    critical(message: str)
        记录严重错误信息
    exception(message: str)
        记录异常信息
    close()
        关闭日志记录器
    get_log_path() -> str
        获取日志文件的路径
    """

    def __init__(self, ):
        """初始化日志记录器"""

        # 日志根文件夹的路径，不可以随意修改
        log_root_path = 'bin/local/logfile'

        # 如果日志根文件夹不存在，则创建日志根文件夹
        if not os.path.exists(log_root_path):
            os.makedirs(log_root_path)

        # 日志文件的名称,以日期命名,精确到秒,每次启动均会生成新的日志文件
        log_filename = time.strftime('%Y-%m-%d_%H-%M-%S.log', time.localtime())

        # 完整的日志文件路径
        self.log_path = os.path.join(log_root_path, log_filename)

        # 创建logger
        self.logger = logging.getLogger('MyLogger')

        # 设置日志级别
        self.logger.setLevel(logging.DEBUG)

        # 创建一个RotatingFileHandler，最多备份5个日志文件，每个文件最大10MB
        handler = RotatingFileHandler(self.log_path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # 将handler添加到logger
        self.logger.addHandler(handler)

    def debug(self, message: str):
        """记录调试信息"""
        self.logger.debug(message)

    def info(self, message: str):
        """记录正常信息"""
        self.logger.info(message)

    def warning(self, message: str):
        """记录警告信息"""
        self.logger.warning(message)

    def error(self, message: str):
        """记录错误信息"""
        self.logger.error(message)

    def critical(self, message: str):
        """记录严重错误信息"""
        self.logger.critical(message)

    def exception(self, message: str):
        """记录异常信息"""
        self.logger.exception(message)

    def close(self):
        """关闭日志记录器

        一定要在APP关闭之前调用，否则会导致日志丢失的Bug产生。
        """

        # 移除所有handler并关闭它们。
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            handler.close()

        # 调用logging.shutdown来确保所有日志处理器都已关闭。
        logging.shutdown()

    def get_log_path(self) -> str:
        """获取日志文件的路径

        Returns
        _______
        str: 日志文件的路径
        """

        return self.log_path
