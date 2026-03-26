import subprocess
import logging

logger = logging.getLogger("toolkit")

def zUMIs(config_path):
    '''
    调用zUMIs
    '''
    zUMIs_dir = ()#需要设置zUMIs.sh位置/或许加入path？
    cmd = [
        zUMIs_dir,
        #"-c"-C是运行zumis自己的环境要重新下载，如果可以设置好conda
        "-y",
        config_path 
    ]
    try: ####
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during zUMIs: {e}")
        raise