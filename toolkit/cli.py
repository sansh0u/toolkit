#!/user/bin/env python
import typer
import os
import logging
from yaml_load import load_yaml
from logger import setup_logger
from DBit_RNA.run_zUMIs import zUMIs
from ATAC.qc import filter
from ATAC.bc_process import bc_pr

app = typer.Typer(help = "toolkit", no_args_is_help = True)

setup_logger()
logger = logging.getLogger("toolkit")

def ask(name = str, default = None):
    return typer.prompt(name, default = default)        #回车返回默认值


@app.command()
def run(config_path: str = typer.Option("-- config", help="Path to the configuration YAML file")):
    """运行任务并加载配置文件"""
    config_data, method = load_yaml(config_path)
    #加个log
    
    if method == 1:
        os.makedirs(config_data['Out_dir'], exist_ok=True)
        #qc
        filter(config_data)
        #过滤bc
        bc_pr(config_data)
#运行完要把上一步文件删了
    elif method == 2:
        zUMIs(config_data)

if __name__ == "__main__":
    app()