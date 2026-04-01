import logging
import subprocess

logger = logging.getLogger("toolkit")

def chromap(config):
    """
    根据提供的配置对ATAC-seq数据进行chromap分析
    """
    skipr = config['Filter']['skipr']
    if skipr == 1:
        output_file_R2 = f"{config['Out_dir']['dir']}/linker2_R1.fastq.gz"
        subprocess.run(["rm", f"{config['Out_dir']['dir']}/linker2_R2.fastq.gz"], check=True)
    else:
        output_file_R2 = f"{config['Out_dir']['dir']}/linker2_R2.fastq.gz"
        subprocess.run(["rm", f"{config['Out_dir']['dir']}/linker2_R1.fastq.gz"], check=True)
    output_file_R1 = f"{config['Out_dir']['dir']}/output_R1.fastq.gz"
    b_file = f"{config['Out_dir']['dir']}/output_R2.fastq.gz"
    index_file = config['Reference']['index_file']
    fa_file = config['Reference']['fa_file']
    output_file = f"{config['Out_dir']['dir']}/{config['Project']}.bed"
    bc_file = config['Barcode']['file']

    cmd = [ "chromap", 
        "--preset", "atac", "-x", index_file, 
        "-r", fa_file, 
        "-1", output_file_R1, 
        "-2", output_file_R2,
        "-b", b_file,
        "--barcode-whitelist", bc_file,
        "-t", "12", "-o", output_file
]
    try: ####
        subprocess.run(cmd, check=True)
        logger.info("ATAC-seq filtering completed successfully.")
        #返回点东西让我知道成功了
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during chromap analysis: {e}")
        raise
    subprocess.run(["rm", "-r",output_file_R1, output_file_R2, b_file], check=True)


def sort_bed(config):
    """
    对chromap输出的bed文件进行排序
    """
    output_file = f"{config['Out_dir']['dir']}/{config['Project']}"
    subprocess.run(["sort", "-k1,1 -k2,2n -k3,3n -k4,4", f" --parallel={config['Threads']}", "-S 36G", output_file +".bed", ">", output_file + "_sorted.bed"], check=True)
    subprocess.run(["bgzip", output_file + "_sorted.bed" ,"@", config['Threads']], check=True)
    subprocess.run(["tabix", "-p", "bed", output_file + "_sorted.bed.gz"], check=True)

#sort -k1,1 -k2,2n -k3,3n -k4,4 --parallel=12 -S 36G KI_1018_50.bed > KI_1018_50_sorted.bed
#module load tabix
#bgzip KI_1018_50_sorted.bed
#tabix -p bed KI_1018_50_sorted.bed.gz