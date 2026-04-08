#!/user/bin/env python
import typer
import os
import logging
from yaml_load import load_yaml,merge_config, config_cal, get_config
from logger import setup_logger
from DBiT_RNA.run_zUMIs import zUMIs
from ATAC.qc import filter
from ATAC.bc_process import bc_pr
from ATAC.chromap import chromap, sort_bed



app = typer.Typer(help = "toolkit", no_args_is_help = True)

setup_logger()
logger = logging.getLogger("toolkit")



def ask(name = str, default = None):
    return typer.prompt(name, default = default)        #回车返回默认值


@app.command()
def run(config_path: str = typer.Option(...,"--config", help="Path to the configuration YAML file")):
    """运行任务并加载配置文件"""
    logger.info("Start pipeline.")
    config = load_yaml(config_path)
    logger.info("Successfully loaded the YAML file.")
    config = config_cal(config)
    logger.info("Successfully configured the YAML file.")
    logger.info(config)
    os.makedirs(get_config(config, "dir"), exist_ok=True)
    method = get_config(config, "Method")
    if method in ["atac", "co_atac", "patho_atac"] :
        #qc
        filter(config)
        #过滤bc
        bc_pr(config)
        chromap(config)
        sort_bed(config)
    elif method in ["dbit", "co_rna","patho_dbit"]:
        zUMIs(config)
#运行完要把上一步文件删了
if __name__ == "__main__":
    app()