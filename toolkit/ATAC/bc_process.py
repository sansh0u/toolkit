from Bio.SeqIO.QualityIO import FastqGeneralIterator
from gzip import open as gzopen
import logging
#import argparse

logger = logging.getLogger("toolkit")


def bc_pr(config_data):
    '''
    处理BCB_UMI格式的fastq文件,提取UMI和barcode,输出到新的fastq文件
    '''
    skipr = config_data.get("Filter", {}).get("skipr", 1)
    if skipr == 1:
        input_file = config_data['Out_dir'] + "/linker2_R2.fastq.gz"
    else:
        input_file = config_data['Out_dir'] + "/linker2_R1.fastq.gz"
    output_file_R1 = config_data['Out_dir'] + "/output_R1.fastq.gz"
    output_file_R2 = config_data['Out_dir'] + "/output_R2.fastq.gz"
    #ap = argparse.ArgumentParser()
    #ap.add_argument("-i", "--input", required=True, help="input file")
    #ap.add_argument("-o1", "--output_R1", required=True, help="output file R1")
    #ap.add_argument("-o2", "--output_R2", required=True, help="output file R2")
    #args = vars(ap.parse_args())
    #seq_start=117 # 22bp primer  + 8bp BC2 + 30bp linker2 + 8bp BC1 + 30bp linker1 + 19bp ME (chemV2 barcode B no UMI)

    if config_data.get('Filter', {}).get('UMI', 10) == 0:
        seq_start = 117
    else:
        seq_start = 127

    bc2_start = config_data.get('Filter', {}).get('bc2_start', 22)
    bc2_end = config_data.get('Filter', {}).get('bc2_end', 30)

    bc1_start = config_data.get('Filter', {}).get('bc1_start', 60)
    bc1_end = config_data.get('Filter', {}).get('bc1_end', 68) 

    with gzopen(input_file, "rt") as in_handle_R1, open(output_file_R1, "w") as out_handle_R1, open(output_file_R2, "w") as out_handle_R2:
        for title, seq, qual in FastqGeneralIterator(in_handle_R1):
            new_seq_R1 = seq[seq_start:]
            new_qual_R1 = qual[seq_start:]
            barcode = seq[bc2_start:bc2_end] + seq[bc1_start:bc1_end] # !!! BC2 + BC1
            new_qual_R2 = qual[bc2_start:bc2_end] + qual[bc1_start:bc1_end]        
            out_handle_R1.write("@%s\n%s\n+\n%s\n" % (title, new_seq_R1, new_qual_R1))
            out_handle_R2.write("@%s\n%s\n+\n%s\n" % (title, barcode, new_qual_R2))
