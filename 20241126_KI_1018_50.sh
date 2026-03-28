#!/bin/bash
#SBATCH --partition=ycga 
#SBATCH --job-name=20241126_KI_1018_50
#SBATCH --ntasks=1 --cpus-per-task=12
#SBATCH --mem=36g
#SBATCH --time=3:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=haikuo.li@yale.edu
#SBATCH -o /home/hl737/palmer_pi_fan/mouse_KI/202410_ATAC_process/KI_1018_50/sbatch_output/KI_1018_50.%j.out

#change below
memory=36
cores=12
output_folder=/home/hl737/palmer_pi_fan/mouse_KI/202410_ATAC_process/KI_1018_50/

raw_folder=/home/hl737/palmer_pi_fan/mouse_KI/202410_ATAC_raw/usftp21.novogene.com/01.RawData/KI_1018_50/
fastq_intput_11=$raw_folder/KI_1018_50_CKDL240035881-1A_22HNF7LT4_L4_1.fq.gz
fastq_intput_12=$raw_folder/KI_1018_50_CKDL240035881-1A_22HNF7LT4_L4_2.fq.gz
fastq_intput_21=$raw_folder/KI_1018_50_CKDL240035881-1A_22HM3NLT4_L4_1.fq.gz
fastq_intput_22=$raw_folder/KI_1018_50_CKDL240035881-1A_22HM3NLT4_L4_2.fq.gz
raw_fq_folder=/home/hl737/palmer_pi_fan/mouse_KI/202410_ATAC_process/KI_1018_50_merge_fq/
mkdir -p $raw_fq_folder
cat $fastq_intput_11 $fastq_intput_21 > $raw_fq_folder/KI_1018_50_1.fq.gz
cat $fastq_intput_12 $fastq_intput_22 > $raw_fq_folder/KI_1018_50_2.fq.gz
fastq_intput_1=$raw_fq_folder/KI_1018_50_1.fq.gz
fastq_intput_2=$raw_fq_folder/KI_1018_50_2.fq.gz


out_file=/home/hl737/palmer_pi_fan/mouse_KI/202410_ATAC_process/KI_1018_50/KI_1018_50.bed
chromap_input_folder=/home/hl737/palmer_pi_fan/mouse_KI/202410_ATAC_process/KI_1018_50/chromap_input/
chromap_input_2=/home/hl737/palmer_pi_fan/mouse_KI/202410_ATAC_process/KI_1018_50/bbduk/bbduk_L2_R1.fastq.gz

#may or may not change below
BC_process_script=/home/hl737/project/20240503_ATAC_practice/process/BC_process_BCB_noUMI.py
index_file=/gpfs/gibbs/pi/fan/hl737/sci_FFPE/chromap_index/GRCm38/GRCm38.primary_assembly.genome.index
fa_file=/gpfs/gibbs/pi/fan/hl737/sci_FFPE/chromap_index/GRCm38/GRCm38.primary_assembly.genome.fa
bc_file=/home/hl737/palmer_pi_fan/mouse_KI/20240614_2500barcode_AB_update.txt #2500 (AB_2&4_updated)


###########-----------------###########
#usually no need to change below
date
module purge
module load miniconda
conda activate spatial-atac
module load Java

###1. Linker filter: Filter L1 and then filter L2
mkdir -p $output_folder
bbduk_folder=$output_folder/bbduk
mkdir -p $bbduk_folder

/gpfs/gibbs/pi/fan/hl737/Downloads/bbmap/bbduk.sh in1=$fastq_intput_1 \
in2=$fastq_intput_2 \
outm1=$bbduk_folder/bbduk_L1_R1.fastq.gz \
outm2=$bbduk_folder/bbduk_L1_R2.fastq.gz \
k=30 mm=f rcomp=f restrictleft=108 skipr1=t hdist=3 \
stats=$bbduk_folder/bbduk_stats_L1.txt \
threads=$core literal=GTGGCCGATGTTTCGCATCGGCGTACGACT

/gpfs/gibbs/pi/fan/hl737/Downloads/bbmap/bbduk.sh in1=$bbduk_folder/bbduk_L1_R1.fastq.gz \
in2=$bbduk_folder/bbduk_L1_R2.fastq.gz \
outm1=$bbduk_folder/bbduk_L2_R1.fastq.gz \
outm2=$bbduk_folder/bbduk_L2_R2.fastq.gz \
k=30 mm=f rcomp=f restrictleft=70 skipr1=t hdist=3 \
stats=$bbduk_folder/bbduk_stats_L2.txt \
threads=$core literal=ATCCACGTGCTTGAGAGGCCAGAGCATTCG

rm -r $bbduk_folder/bbduk_L1_R1.fastq.gz $bbduk_folder/bbduk_L1_R2.fastq.gz


###2. BC_process.
date
chromap_input_folder=$output_folder/chromap_input/
mkdir -p $chromap_input_folder
python $BC_process_script \
--input $bbduk_folder/bbduk_L2_R2.fastq.gz \
--output_R1 $chromap_input_folder/sample_S1_L001_R1_001.fastq \
--output_R2 $chromap_input_folder/sample_S1_L001_R2_001.fastq

gzip $chromap_input_folder/sample_S1_L001_R1_001.fastq
#117:
gzip $chromap_input_folder/sample_S1_L001_R2_001.fastq
#16bp bc
rm $bbduk_folder/bbduk_L2_R2.fastq.gz


###3. Run chromap
date
cd $output_folder

chromap --preset atac -x $index_file -r $fa_file -1 $chromap_input_folder/sample_S1_L001_R1_001.fastq.gz -2 $chromap_input_2 \
-b $chromap_input_folder/sample_S1_L001_R2_001.fastq.gz --barcode-whitelist $bc_file -t 12 -o $out_file

#sort -k1,1 -k2,2n -k3,3n -k4,4 --parallel=12 -S 36G KI_1018_50.bed > KI_1018_50_sorted.bed
#module load tabix
#bgzip KI_1018_50_sorted.bed
#tabix -p bed KI_1018_50_sorted.bed.gz