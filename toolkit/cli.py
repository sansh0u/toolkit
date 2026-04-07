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



DEFAULT_CONFIG = {
    "Project": "test",
    "Advanced":{
        "linker1": "GTGGCCGATGTTTCGCATCGGCGTACGACT", 
        "linker2": "ATCCACGTGCTTGAGAGGCCAGAGCATTCG",
        "skipr": 1,
        "UMI": 10,
        "primer": 22,
        "hdist": 3,
        },
    "Threads": 12
}

def ask(name = str, default = None):
    return typer.prompt(name, default = default)        #回车返回默认值


@app.command()
def run(config_path: str = typer.Option(...,"--config", help="Path to the configuration YAML file")):
    """运行任务并加载配置文件"""
    config = load_yaml(config_path)
    #加个log
    config = merge_config(config, Patho_ATAC)
    config = config_cal(config)
    print(config)
    """if method == 1:"""
    os.makedirs(get_config(config, "dir"), exist_ok=True)
        #qc
    #filter(config)
        #过滤bc
    #bc_pr(config)
   # chromap(config)
    sort_bed(config)
#运行完要把上一步文件删了
    
    
    
"""
    elif method == 2:
        zUMIs(config)
    
"""

if __name__ == "__main__":
    app()