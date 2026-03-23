"""
logger.py

Initialize logging system for the pipeline.
Creates logs directory and two log files:
pipeline.log and error.log
"""

import logging
import os


def setup_logger():
    """
    Setup logging configuration.
    """

    # 创建 logs 目录（如果不存在）
    os.makedirs("logs", exist_ok=True)

    # 创建 logger
    logger = logging.getLogger("toolkit")

    # 允许记录 INFO 以上日志
    logger.setLevel(logging.INFO)

    pipeline_handler = logging.FileHandler("logs/pipeline.log")
    pipeline_handler.setLevel(logging.INFO)

    error_handler = logging.FileHandler("logs/error.log")
    error_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    pipeline_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    # 添加 handler
    logger.addHandler(pipeline_handler)
    logger.addHandler(error_handler)

    return logger