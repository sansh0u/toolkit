#!/user/bin/env python
import typer
import os
import logging
from yaml_load import load_yaml,method_check, get_config
from logger import setup_logger
from DBiT_RNA.run_zUMIs import zUMIs
from qc import filter
from ATAC.bc_process import bc_pr
from ATAC.chromap import chromap, sort_bed
from DBiT_RNA.stpipeline import stpipeline
from DBiT_RNA.bc_pro import bc_pro 


app = typer.Typer(help = "toolkit", no_args_is_help = True)

setup_logger()
logger = logging.getLogger("toolkit")



def ask(name = str, default = None):
    return typer.prompt(name, default = default)        #回车返回默认值


@app.command()
def run(config_path: str = typer.Option(...,"--config", help="Path to the configuration YAML file")):
    """运行任务并加载配置文件"""
    print("Pipeline started")
    #logger.info("Pipeline started")
    config = load_yaml(config_path)
    config = method_check(config)
    os.makedirs(get_config(config, "dir"), exist_ok=True)
    method = get_config(config, "Method")
    print(config)
    if method in ["atac", "co_atac", "patho_atac"] :
        #qc
        filter(config)
        #过滤bc
        bc_pr(config)
        chromap(config)
        sort_bed(config)
    elif method in ["dbit", "co_rna","patho_dbit"]:
        #qc
        filter(config)
        #过滤bc
        bc_pro(config)
        stpipeline(config)
        #zUMIs(config)
#运行完要把上一步文件删了
if __name__ == "__main__":
    app()