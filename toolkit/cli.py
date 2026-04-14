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
from pathlib import Path
import yaml


app = typer.Typer(help = "toolkit", no_args_is_help = True)

setup_logger()
logger = logging.getLogger("toolkit")



def ask(name = str, default = None):
    return typer.prompt(name, default = default)        #回车返回默认值


@app.command()
def run(
    config_path: str = typer.Option(None,"--config", help="Path to the configuration YAML file"),
    zumis: bool = typer.Option(False, "--zumis", help="Run zUMIs"),
    zpath : str = typer.Option(None, "-l", help="Path to zUMIs.sh"),
    dbit: bool = typer.Option(False, "-dbit", help="Whether to run zUMIs on DBiT"),
    patho: bool = typer.Option(False, "-patho", help="Whether to run zUMIs on patho"),
    rna: bool = typer.Option(False, "-rna", help="Whether to run zUMIs on RNA"),
    in1: str = typer.Option(None, "-in1", help="Path to in1"),
    in2: str = typer.Option(None, "-in2", help="Path to in2"),
    out: str = typer.Option(None, "-out", help="Path to out"),
    config: str = typer.Option(None, "-config", help="Run your own YAML file")
    ):
    """运行任务并加载配置文件"""
    
    if not config_path and not zumis:
        raise typer.BadParameter("Please provide --config or --zumis")

    if config_path and zumis:
        raise typer.BadParameter("--config and --zumis cannot be used together")

    if any([zpath, dbit, patho, rna, in1, in2, out, config]) and not zumis:
            raise typer.BadParameter("Use --zumis to enable zUMIs")

    if zumis:
        BASE_DIR = Path(__file__).resolve().parent
        CONFIG_FILE = BASE_DIR / "config" / ".config.yaml"

        if zpath:
            zpath = Path(zpath)
            
            if zpath.is_dir():
                zpath = zpath / "zUMIs.sh"
            
            if not Path(zpath).exists():
                raise typer.BadParameter(f"zUMIs not found: {zpath}")
            
            if zpath.name != "zUMIs.sh":
                raise typer.BadParameter("Please provide zUMIs.sh or its directory")
            
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            if zpath.name != "zUMIs.sh":
                raise typer.BadParameter("Please provide zUMIs.sh or its directory")
            
            with open(CONFIG_FILE, "w") as f:
                yaml.safe_dump({"zumis_path": zpath}, f)

        else:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE) as f:
                    cfg = yaml.safe_load(f) or {}

                if "zumis_path" in cfg:
                    zpath = cfg["zumis_path"]
                else:
                    raise typer.BadParameter("No zUMIs path found, please provide -l once")
            else:
                raise typer.BadParameter("Please provide -l (zUMIs path) at least once")

        

        if not zpath.exists():
            raise typer.BadParameter(f"zUMIs not found: {zpath}")

        print(f"Using zUMIs: {zpath}")

            
        
    
        #if not zpath.exists():
            #raise typer.BadParameter(f"zUMIs not found: {zpath}")

        if config:
            if any([dbit, patho, rna]):
                raise typer.BadParameter("--config cannot be used with -dbit/-patho/-rna")


        mode_count = sum([dbit, patho, rna])

        if mode_count == 0:
            raise typer.BadParameter("Please select one mode: -dbit / -patho / -rna")

        if mode_count > 1:
            raise typer.BadParameter("Only one mode can be selected")

        if not all([in1, in2, out]):
            raise typer.BadParameter("Mode requires -in1 -in2 -out")

        if dbit:
            mode = "DBiT"
        elif patho:
            mode = "Patho"
        else:
            mode = "RNA"

        print(f"Running zUMIs in {mode} mode")




    if config_path:
       
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

