"""
YAML configuration file loading and validation module
This module provides functionality for loading YAML configuration files,
validating configuration fields, and printing configuration summaries.
"""

import os
import yaml
import logging

logger = logging.getLogger("toolkit")


def load_yaml(config_path):
    """
    Load YAML configuration file. 加载并判断YAML配置文件是否存在并可解析(已完成)
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        return None
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file {config_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error reading config: {e}")
        return None
    if config is None:
        logger.error("YAML file is empty.")
        return None
    return config

#需要完善yaml参数
def validate_config(config):
    """
    Validate essential configuration fields required by pipeline
    验证pipeline运行所需的必要配置字段
    """
    error_flag = False # 错误标志位
    # Required top-level sections
    # 必要的顶级配置部分

    # project
    if not config.get("project"):
        logging.error("Missing parameter: project")
        error_flag = True

    # output directory
    if not config.get("out_dir"):
        logging.error("Missing parameter: out_dir")
        error_flag = True

    # reference
    reference = config.get("reference", {})

    star_index = reference.get("STAR_index")
    if not star_index:
        logging.error("Missing reference: STAR_index")
        error_flag = True
    elif not os.path.exists(star_index):
        logging.error(f"STAR_index not found: {star_index}")
        error_flag = True

    gtf_file = reference.get("GTF_file")
    if not gtf_file:
        logging.error("Missing reference: GTF_file")
        error_flag = True
    elif not os.path.exists(gtf_file):
        logging.error(f"GTF file not found: {gtf_file}")
        error_flag = True

    # threads
    threads = config.get("num_threads")
    if not isinstance(threads, int) or threads < 1:
        logging.error("num_threads must be an integer >=1")
        error_flag = True

    if error_flag:
        logging.error("YAML validation failed.")
        return False

    logging.info("YAML validation passed.")
    return True

"""
def load_and_validate(config_path):
    ###
    Load and validate YAML configuration.
    ###

    config = load_yaml(config_path)

    if config is None:
        return None

    if not validate_yaml(config):
        return None

    return config
"""