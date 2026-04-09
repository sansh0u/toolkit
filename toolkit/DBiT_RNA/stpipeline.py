import logging
import subprocess
from yaml_load import get_config
import os

logger = logging.getLogger("toolkit")

def stpipeline(config):
    """
    根据提供的配置对DBiT-seq数据进行chromap分析
    """
    stpipeline_id = get_config(config, 'Project')
    output_folder = f"{get_config(config, 'dir')}"
    temp_folder = f"{get_config(config, 'dir')}/temp"
    os.makedirs(temp_folder, exist_ok=True)
    output_file_R2 = f"{get_config(config, 'dir')}/linker_R1.fastq.gz"
    output_file_R1 = f"{get_config(config, 'dir')}/output_R2.fastq.gz"
    b_file = f"{get_config(config, 'dir')}/output_R2.fastq.gz"
    index_file = get_config(config, 'index_file')
    gta_file = get_config(config, 'gta_file')
    output_file = f"{get_config(config, 'dir')}/{get_config(config, 'Project')}.bed"
    bc_file = get_config(config, 'file')
    thread = str(get_config(config, 'Threads'))
    
    cmd = [ "st_pipeline_run", 
        "--output-folder", output_folder,
        "--temp-folder", temp_folder, 
        "--ids", bc_file,
        "--threads", thread,
        "--ref-map", index_file,
        "--ref-annotation", gta_file,
        "--expName", stpipeline_id,
        "--log-file", f"{output_folder}/{stpipeline_id}_log.txt",
        "--htseq-no-ambiguous", "--demultiplexing-kmer", "5",
        "--umi-start-position", "16",
        "--umi-end-position", "26",
        "--demultiplexing-overhang", "0",
        "--min-length-qual-trimming", "18",
        "--no-clean-up", "--verbose",
        output_file_R1,
        output_file_R2
]
    try: ####
        subprocess.run(cmd, check=True)
        #logger.info("ATAC-seq filtering completed successfully.")
        #返回点东西让我知道成功了
    except subprocess.CalledProcessError as e:
        #logger.error(f"Error during chromap analysis: {e}")
        raise
    subprocess.run(["rm", "-r",output_file_R1, output_file_R2, b_file], check=True)
