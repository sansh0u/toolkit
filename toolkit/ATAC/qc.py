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
    cmd1 =  [
        "bbduk",
        f"in={config['Sequence_file']['file1']['name']}",
        f"in2={config['Sequence_file']['file2']['name']}",
        f"outm={config['Out_dir']}/linker1_R1.fastq.gz", ####改名字
        f"outm2={config['Out_dir']}/linker1_R2.fastq.gz", ####
        f"hdist={config.get('Filter', {}).get('hdist', 3)}",
        f"k={config.get('Filtrt', {}).get('k', 30)}",
        f"literal={config.get('Filter', {}).get('literal', {}).get('linker1', 'GTGGCCGATGTTTCGCATCGGCGTACGACT')}",
        f"threads={config['Threads']}",
        "mm=f rcomp=f ",
        f"restrictleft={config.get('Filter', {}).get('restrictleft', 108)}"
    ]

    cmd2 =  [
        "bbduk",
        f"in={config['Out_dir']}/linker1_R1.fastq.gz",
        f"in2={config['Out_dir']}/linker1_R2.fastq.gz",
        f"outm={config['Out_dir']}/linker2_R1.fastq.gz", ####
        f"outm2={config['Out_dir']}/linker2_R2.fastq.gz", ####
        f"hdist={config.get('Filter', {}).get('hdist', 3)}",
        f"k={config.get('Filter', {}).get('k', 30)}",
        f"literal={config.get('Filter', {}).get('literal', {}).get('linker2', 'ATCCACGTGCTTGAGAGGCCAGAGCATTCG')}",
        f"threads={config['Threads']}",
        "mm=f rcomp=f ",
        f"restrictleft={config.get('Filter', {}).get('restrictleft', 70)}"
    ]

    skipr = config.get("Filter", {}).get("skipr", 1)  # 获取skipr参数，默认为1
    '''
    if skipr not in [1, 2]:
        logger.error(f"Invalid skipr value: {skipr}. Must be 1 or 2.")
        raise ValueError("Invalid skipr value. Must be 1 or 2.")
    '''
    cmd1.append(f"skipr{skipr}=t")  # skipr为几，则设置为跳过R几
    cmd2.append(f"skipr{skipr}=t")
    
    try: ####
        subprocess.run(cmd1, check=True)
        subprocess.run(cmd2, check=True)
        logger.info("ATAC-seq filtering completed successfully.")
        #返回点东西让我知道成功了
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during ATAC-seq filtering: {e}")
        raise

    logger.info("ATAC-seq quality control filtering completed.")