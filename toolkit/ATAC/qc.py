import subprocess
import logging

logger = logging.getLogger("toolkit")


def filter(config):
    """
    根据提供的配置对ATAC-seq数据进行过滤
    """
     # bbduk写入bin了，直接使用
    

    # Placeholder for actual filtering logic需要校对logo信息
    logger.info("Starting ATAC-seq quality control filtering...")
    skipr = config['Filter']['skipr']
    cmd1 =  [
        "bbduk",
        f"in={config['Sequence_file']['file1']['name']}",
        f"in2={config['Sequence_file']['file2']['name']}",
        f"outm={config['Out_dir']['dir']}/linker1_R1.fastq.gz", ####改名字
        f"outm2={config['Out_dir']['dir']}/linker1_R2.fastq.gz", ####
        f"hdist={config['Filter']['hdist']}",
        f"k={config['Filter']['k']}",
        f"literal={config['Filter']['literal']['linker1']}",
        f"threads={config['Threads']}",
        "mm=f", "rcomp=f", f"skipr{skipr}=t",
        f"restrictleft={config['Filter']['literal']['restrictleft1']}"
    ]

    cmd2 =  [
        "bbduk",
        f"in={config['Out_dir']['dir']}/linker1_R1.fastq.gz",
        f"in2={config['Out_dir']['dir']}/linker1_R2.fastq.gz",
        f"outm={config['Out_dir']['dir']}/linker2_R1.fastq.gz", ####
        f"outm2={config['Out_dir']['dir']}/linker2_R2.fastq.gz", ####
        f"hdist={config['Filter']['hdist']}",
        f"k={config['Filter']['k']}",
        f"literal={config['Filter']['literal']['linker2']}",
        f"threads={config['Threads']}",
        "mm=f", "rcomp=f", f"skipr{skipr}=t",
        f"restrictleft={config['Filter']['literal']['restrictleft2']}"
    ]

    try: ####
        subprocess.run(cmd1, check=True)
        subprocess.run(cmd2, check=True)
        logger.info("ATAC-seq filtering completed successfully.")
        #返回点东西让我知道成功了
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during ATAC-seq filtering: {e}")
        raise

    logger.info("ATAC-seq quality control filtering completed.")
    subprocess.run(["rm", "-r",f"{config['Out_dir']['dir']}/linker1_R1.fastq.gz", f"{config['Out_dir']['dir']}/linker1_R2.fastq.gz"], check=True)