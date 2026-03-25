import logging
import subprocess

logger = logging.getLogger("toolkit")

def chromap(config):
    """
    根据提供的配置对ATAC-seq数据进行chromap分析
    """
    output_file_R1 = f"{config['Out_dir']}/output_R1.fastq.gz"
    output_file_R2 = f"{config['Out_dir']}/linker2_R2.fastq.gz"
    cmd = [ "chromap", 
        "--preset atac", "-x", index_file, 
        "-r", fa_file, 
        "-1", output_file_R1, 
        "-2", output_file_R2,
        "-b", chromap_input_folder + "/sample_S1_L001_R2_001.fastq.gz", "--barcode-whitelist", bc_file,
        "-t", "12", "-o", output_file
]
