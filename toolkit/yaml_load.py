"""
YAML configuration file loading and validation module
This module provides functionality for loading YAML configuration files,
validating configuration fields, and printing configuration summaries.
"""

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
    #直接输出config，要什么调用的时候自己取

    if config:
        first_key = list(config.keys())[0]  # 获取字典的第一个键
        if first_key[0].isupper():
            method = 1
        else:
            method = 2
    return config, method


#config, method = load_yaml("/home/sanshou/projects/tool/dbit/zUMIs.yaml")
#print(method)
    
