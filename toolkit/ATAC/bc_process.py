from Bio.SeqIO.QualityIO import FastqGeneralIterator
from gzip import open as gzopen
import logging
import subprocess
from yaml_load import get_config
#import argparse

logger = logging.getLogger("toolkit")


def bc_pr(config):
    '''
    处理BCB_UMI格式的fastq文件,提取UMI和barcode,输出到新的fastq文件
    '''
    skipr = get_config(config, "skipr")
    if skipr == 1:
        input_file = get_config(config, "dir") + "/linker2_R2.fastq.gz"
    
    else:
        input_file = get_config(config, "dir") + "/linker2_R1.fastq.gz"
    
    
    output_file_R1 = get_config(config, "dir") + "/output_R1.fastq"
    output_file_R2 = get_config(config, "dir") + "/output_R2.fastq"
    
    #ap = argparse.ArgumentParser()
    #ap.add_argument("-i", "--input", required=True, help="input file")
    #ap.add_argument("-o1", "--output_R1", required=True, help="output file R1")
    #ap.add_argument("-o2", "--output_R2", required=True, help="output file R2")
    #args = vars(ap.parse_args())
    #seq_start=117 # 22bp primer  + 8bp BC2 + 30bp linker2 + 8bp BC1 + 30bp linker1 + 19bp ME (chemV2 barcode B no UMI)

    
    seq_start = get_config(config, "seq_start")
    bc2_start = get_config(config, "bc2_start")
    bc2_end = get_config(config, "bc2_end")
    bc1_start = get_config(config, "bc1_start")
    bc1_end = get_config(config, "bc1_end")
    
    """
    logger.info(f"input_file: {input_file}")
    logger.info(f"output_file_R1: {output_file_R1}")
    logger.info(f"output_file_R2: {output_file_R2}")
    logger.info(f"seq_start: {seq_start}")
    logger.info(f"bc2_start: {bc2_start}")
    logger.info(f"bc2_end: {bc2_end}")
    logger.info(f"bc1_start: {bc1_start}")
    logger.info(f"bc1_end: {bc1_end}")
    """
    with gzopen(input_file, "rt") as in_handle_R1, open(output_file_R1, "w") as out_handle_R1, open(output_file_R2, "w") as out_handle_R2:
        #logger.info("Start BC processing")
        for title, seq, qual in FastqGeneralIterator(in_handle_R1):
            new_seq_R1 = seq[seq_start:]
            new_qual_R1 = qual[seq_start:]
            barcode = seq[bc2_start:bc2_end] + seq[bc1_start:bc1_end] # !!! BC2 + BC1
            new_qual_R2 = qual[bc2_start:bc2_end] + qual[bc1_start:bc1_end]        
            out_handle_R1.write("@%s\n%s\n+\n%s\n" % (title, new_seq_R1, new_qual_R1))
            out_handle_R2.write("@%s\n%s\n+\n%s\n" % (title, barcode, new_qual_R2))
    
    subprocess.run(["pigz", "-p", "12", "-f", output_file_R1], check=True)
    subprocess.run(["pigz", "-p", "12", "-f", output_file_R2], check=True)