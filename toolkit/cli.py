#!/user/bin/env python
import typer
import os
import logging
from yaml_load import load_yaml
from logger import setup_logger
from DBiT_RNA.run_zUMIs import zUMIs
from ATAC.qc import filter
from ATAC.bc_process import bc_pr
from ATAC.chromap import chromap
from yaml_load import merge_config
app = typer.Typer(help = "toolkit", no_args_is_help = True)

setup_logger()
logger = logging.getLogger("toolkit")

DEFAULT_CONFIG = {
    "Filter": {
        "hdist": 3,
        "k": 30,
        "skipr": 1,
        
        "literal": {
            "linker1": "GTGGCCGATGTTTCGCATCGGCGTACGACT", 
            "linker2": "ATCCACGTGCTTGAGAGGCCAGAGCATTCG",
            "restrictleft1": 108,
            "restrictleft2": 70
        },
        "seq_start": 127,
        "bc2_start": 22,
        "bc2_end": 30,
        "bc1_start": 60,
        "bc1_end": 68
    },
    "Threads": 12
}

def ask(name = str, default = None):
    return typer.prompt(name, default = default)        #回车返回默认值


@app.command()
def run(config_path: str = typer.Option(...,"--config", help="Path to the configuration YAML file")):
    """运行任务并加载配置文件"""
    config, method = load_yaml(config_path)
    #加个log
    config = merge_config(config, DEFAULT_CONFIG)
    if method == 1:
        os.makedirs(config['Out_dir']['dir'], exist_ok=True)
        #qc
        filter(config)
        #过滤bc
        bc_pr(config)
        chromap(config)
#运行完要把上一步文件删了
    elif method == 2:
        zUMIs(config)

if __name__ == "__main__":
    app()