"""
YAML configuration file loading and validation module
This module provides functionality for loading YAML configuration files,
validating configuration fields, and printing configuration summaries.
"""

import yaml
import logging

logger = logging.getLogger("toolkit")

DBit_seq = {
    "Project": "test",
    "Advanced": {
        "skipr": 2,
        "primer": 22,
        "hdist": 3,
        "rna_lib": "illumina",
        "primer5": "AAGCAGTGGTATCAACGCAGAGTGAATGGG"
        }
}
ATAC_seq  = {
    "Project": "test",
        "Advanced":{
            "linker1": "AGATGTGTATAAGAGACAGCATCGGCGTACGACT", 
            "linker2": "CGAATGCTCTGGCCTCTCAAGCACGTGGAT",
            "skipr": 2,
            "UMI": 0,
            "primer": 0,
            "hdist": 3,
        }
}

co_ATAC = {
    "Project": "test",
    "Advanced":{
        "linker1": "GTGGCCGATGTTTCGCATCGGCGTACGACT", 
        "linker2": "ATCCACGTGCTTGAGAGGCCAGAGCATTCG",
        "skipr": 1,
        "UMI": 0,
        "primer": 22,
        "hdist": 3,
        }
}

co_RNA = {

}

Patho_DBit = {
    "Project": "test",
    "Advanced":{
        "skipr": 1,
        "UMI": 10,
        "primer": 22,
        "hdist": 3,
        "rna_lib": "illumina",
        "primer5": "AAGCAGTGGTATCAACGCAGAGTGAATGGG"
        }
}

Patho_ATAC = {
    "Project": "test",
    "Advanced":{
        "linker1": "GTGGCCGATGTTTCGCATCGGCGTACGACT", 
        "linker2": "ATCCACGTGCTTGAGAGGCCAGAGCATTCG",
        "skipr": 1,
        "UMI": 0,
        "primer": 22,
        "hdist": 3,
        }
}

def get_config(config, key):
    if isinstance(config, dict):
        if key in config:
            return config[key]
        for v in config.values():
            result = get_config(v, key)
            if result is not None:
                return result
    elif isinstance(config, list):
        for item in config:
            result = get_config(item, key)
            if result is not None:
                return result
    return None

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
    return config

def method_check(config):
    """
    检查配置文件中的method
    """
    logger.info("Start method check.")
    method = get_config(config, "Method")
    method_dict = {
    "dbit": DBit_seq,
    "atac": ATAC_seq,
    "co_atac": co_ATAC,
    "co_rna": co_RNA,
    "patho_dbit": Patho_DBit,
    "patho_atac": Patho_ATAC
}
    if method not in method_dict:
        raise ValueError(f"Unknown Method: {method}")
    logger.info("Start merge config.")
    merge_config(config, method_dict[method])

    return config

#config, method = load_yaml("/home/sanshou/projects/tool/dbit/zUMIs.yaml")
#print(method)
    
def merge_config(config, default_config):
    for key, value in default_config.items():
        if key not in config or config[key] is None:
            config[key] = value
        elif isinstance(value, dict):
            config[key] = merge_config(config.get(key, {}), value)
    return config

def config_cal(config):
    """
    计算配置文件中的参数,还要分类dbit
    """
    config = method_check(config)
    k1 = len(get_config(config, "linker1"))
    k2 = len(get_config(config, "linker2"))
    bc2_start = get_config(config, "primer") + get_config(config, "UMI")
    bc2_end = bc2_start + 8
    bc1_start = bc2_end + k2
    bc1_end = bc1_start + 8 #8bp barcode
    restrictleft1 = bc1_end + k2 + 10
    restrictleft2 = bc2_end + k1 + 10
    seq_start = bc1_end + k1 + 19
    config['preprocess'] = {
        'k1': k1,
        'k2': k2,
        'bc2_start': bc2_start,
        'bc2_end': bc2_end,
        'bc1_start': bc1_start,
        'bc1_end': bc1_end,
        'restrictleft1': restrictleft1,
        'restrictleft2': restrictleft2,
        'seq_start': seq_start
    }

    return config

