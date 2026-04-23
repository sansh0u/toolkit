import gzip
import numpy as np
import random
from numba import njit

# -------------------------------
# config
# -------------------------------
FASTQ = "/mnt/d/prog/RNA2_1209_Illu_1.fq.gz"
BARCODE_FILE = "/home/sanshou/project/toolkit/toolkit/barcode/20240614_2500barcode_AB_update.txt"

MAX_READS = 100000
MISMATCH = 0


# -------------------------------
# utils
# -------------------------------
_base_map = {'A':0, 'C':1, 'G':2, 'T':3, 'N':4}

def encode(seq):
    return np.fromiter((_base_map.get(x, 4) for x in seq), dtype=np.int8)


def load_barcodes(path):
    bc1, bc2 = [], []
    with open(path) as f:
        for line in f:
            s = line.strip().upper()
            if len(s) != 16:
                continue
            bc2.append(s[:8])
            bc1.append(s[8:])
    return bc1, bc2


def read_fastq_sample(path, n):
    """
    reservoir sampling 随机抽样 reads
    """
    seqs = []
    with gzip.open(path, "rt") as f:
        read_idx = 0
        for i, line in enumerate(f):
            if i % 4 == 1:
                read_idx += 1
                seq = line.strip()

                if len(seqs) < n:
                    seqs.append(seq)
                else:
                    j = random.randint(0, read_idx - 1)
                    if j < n:
                        seqs[j] = seq
    return seqs


# -------------------------------
# core
# -------------------------------
@njit
def scan_positions(seq_mat, bc1_arr, bc2_arr, mismatch):
    n_reads, L = seq_mat.shape

    bc1_hits = np.zeros(L)
    bc2_hits = np.zeros(L)

    for r in range(n_reads):
        for i in range(L - 7):

            # bc2
            for b in range(bc2_arr.shape[0]):
                diff = 0
                for k in range(8):
                    if seq_mat[r, i+k] != bc2_arr[b, k]:
                        diff += 1
                        if diff > mismatch:
                            break
                if diff <= mismatch:
                    bc2_hits[i] += 1
                    break

            # bc1
            for b in range(bc1_arr.shape[0]):
                diff = 0
                for k in range(8):
                    if seq_mat[r, i+k] != bc1_arr[b, k]:
                        diff += 1
                        if diff > mismatch:
                            break
                if diff <= mismatch:
                    bc1_hits[i] += 1
                    break

    return bc1_hits, bc2_hits


# -------------------------------
# main
# -------------------------------
if __name__ == "__main__":

    # 读取 barcode
    bc1_list, bc2_list = load_barcodes(BARCODE_FILE)
    print(f"{len(bc1_list)} bc1 / {len(bc2_list)} bc2 loaded")

    bc1_arr = np.array([encode(x) for x in bc1_list])
    bc2_arr = np.array([encode(x) for x in bc2_list])

    # 随机抽样 reads
    seqs = read_fastq_sample(FASTQ, MAX_READS)
    print(f"sampled reads: {len(seqs)}")

    seq_mat = np.array([encode(x) for x in seqs])

    # 扫描位置
    bc1_pos, bc2_pos = scan_positions(seq_mat, bc1_arr, bc2_arr, MISMATCH)

    # 归一化
    total = len(seqs)
    bc1_ratio = bc1_pos / total
    bc2_ratio = bc2_pos / total

    # 找 peak
    bc1_peak = np.argmax(bc1_ratio)
    bc2_peak = np.argmax(bc2_ratio)

    bc1_value = bc1_ratio[bc1_peak]
    bc2_value = bc2_ratio[bc2_peak]

    print("\n=== Peak result ===")
    print(f"bc1_peak\t{bc1_peak}\t{bc1_value:.4f}")
    print(f"bc2_peak\t{bc2_peak}\t{bc2_value:.4f}")

