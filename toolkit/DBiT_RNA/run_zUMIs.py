import subprocess
import logging

logger = logging.getLogger("toolkit")

def zUMIs(zumis_path, run_zumis, in1, in2, out):
    '''
    调用zUMIs,要把in1,in2,out写进去
    '''
    #需要设置zUMIs.sh位置/或许加入path？
    cmd = [
        zumis_path,
        #"-c"-C是运行zumis自己的环境要重新下载，如果可以设置好conda
        "-y",
        run_zumis 
    ]
    try: ####
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during zUMIs: {e}")
        raise

"""
def run_pipeline(config):
    stage = get_config(config, "which_Stage")

    if stage in ["Filtering"]:
        run_filtering(config)

    if stage in ["Filtering", "Mapping"]:
        run_mapping(config)

    if stage in ["Filtering", "Mapping", "Counting"]:
        run_counting(config)

    if stage in ["Filtering", "Mapping", "Counting", "Summarising"]:
        run_stats(config)
        """