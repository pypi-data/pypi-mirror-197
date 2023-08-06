# -*- coding: utf-8 -*-

import datetime
import logging.config
import logging.config as log_conf
import os
import coloredlogs

'''
 * @Author       : YKenan
 * @Description  : Log file configuration
'''

"""
Set the log output color style
"""
coloredlogs.DEFAULT_FIELD_STYLES = {
    'asctime': {
        'color': 'green'
    },
    'hostname': {
        'color': 'magenta'
    },
    'levelname': {
        'color': 'green',
        'bold': True
    },
    'request_id': {
        'color': 'yellow'
    },
    'name': {
        'color': 'blue'
    },
    'programname': {
        'color': 'cyan'
    },
    'threadName': {
        'color': 'yellow'
    }
}


class LoggerExec:
    """
    Log Set
    """

    def __init__(self, name: str = None, log_path: str = None, level: str = "DEBUG", is_solitary: bool = True):
        """
        Log initialization
        :param name: Project Name
        :param log_path: Log file output path
        :param level: Log printing level
        :param is_solitary: When the file path is consistent (here, the log_path parameter is not a specific file name, but a file path), whether the file is formed independently according to the name parameter
        """
        self.name = name
        self.log_path = log_path
        self.level = level
        # Get Today's Time
        self.today = datetime.datetime.now().strftime("%Y%m%d")
        # Default File Name
        self.default_log_file = f"{name}_log_{self.today}.log" if name and is_solitary else f"log_{self.today}.log"

        self.log_path_name = self.getLogPath()

        # Define two log output formats
        standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' '[%(levelname)s] ===> %(message)s'
        simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] ===> %(message)s'

        # log 配置字典
        # logging_dic 第一层的所有的键不能改变
        self.logging_dic = {
            # 版本号
            'version': 1,
            # 固定写法
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': standard_format
                },
                'simple': {
                    '()': 'coloredlogs.ColoredFormatter',
                    'format': simple_format,
                    'datefmt': '%Y-%m-%d  %H:%M:%S'
                }
            },
            'filters': {},
            'handlers': {
                # 打印到终端的日志
                'sh': {
                    # 打印到屏幕
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'simple'
                },
                # 打印到文件的日志,收集 info 及以上的日志
                'fh': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'standard',
                    # 日志文件
                    'filename': self.log_path_name,
                    # 日志大小 单位: 字节
                    'maxBytes': 1024 * 1024 * 1024,
                    # 轮转文件的个数
                    'backupCount': 5,
                    # 日志文件的编码
                    'encoding': 'utf-8',
                },
            },
            'loggers': {
                # logging.getLogger(__name__) 拿到的 logger 配置
                '': {
                    # 这里把上面定义的两个 handler 都加上，即 log 数据既写入文件又打印到屏幕
                    'handlers': ['sh', 'fh'],
                    'level': 'DEBUG',
                    # 向上（更高 level 的 logger）传递
                    'propagate': True,
                },
            },
        }

        # log 日志级别输颜色样式
        self.level_style = {
            'debug': {
                'color': 'white'
            },
            'info': {
                'color': 'green'
            },
            'warn': {
                'color': 'yellow'
            },
            'error': {
                'color': 'red',
                'bold': True,
            }
        }

    def getLogPath(self) -> str:
        """
        Get log output path
        :return:
        """
        # Determine whether it exists
        if self.log_path:
            log_path_file = self.log_path if self.log_path.endswith(".log") else os.path.join(self.log_path, self.default_log_file)
            log_path = os.path.dirname(self.log_path) if self.log_path.endswith(".log") else self.log_path
            # create folder
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            return log_path_file
        else:
            return os.path.join(self.default_log_file)

    def __setting__(self):
        """
        Log Settings
        :return:
        """
        # Import the logging configuration defined above to configure this log through the dictionary method
        log_conf.dictConfig(self.logging_dic)
        # Generate a log instance where parameters can be passed to the task_id
        logger = logging.getLogger(self.name)
        # Set Color
        coloredlogs.install(level=self.level, level_styles=self.level_style, logger=logger)
        return logger


class Logger:
    """
    Log initialization
    """

    def __init__(self, name: str = None, log_path: str = None, level: str = "DEBUG", is_solitary: bool = True):
        """
        Log initialization
        :param name: Project Name
        :param log_path: Log file output path
        :param level: Log printing level
        :param is_solitary: When the file path is consistent (here, the log_path parameter is not a specific file name, but a file path), whether the file is formed independently according to the name parameter
        """
        self.name = name
        self.log_path = log_path
        self.level = level
        self.is_solitary = is_solitary

    def logger(self):
        """
        Get log
        :return:
        """
        return LoggerExec(self.name, self.log_path, self.level, self.is_solitary).__setting__()

    def debug(self, content: str):
        """
        Log debug information
        :param content: content
        :return:
        """
        return self.logger().debug(content)

    def info(self, content: str):
        """
        log info information
        :param content: content
        :return:
        """
        return self.logger().info(content)

    def warn(self, content: str):
        """
        log warn information
        :param content: content
        :return:
        """
        return self.logger().warning(content)

    def error(self, content: str):
        """
        log error information
        :param content: content
        :return:
        """
        return self.logger().error(content)
