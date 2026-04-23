import gzip
import numpy as np
import time

# -------------------------------
# config
# -------------------------------
FASTQ = "/mnt/d/prog/RNA2_1209_Illu_2.fq.gz"
BARCODE_FILE = "/home/sanshou/project/toolkit/toolkit/barcode/20240614_2500barcode_AB_update.txt"

MAX_READS = 100000

# -------------------------------
# utils
# -------------------------------
base2int = {'A':0, 'C':1, 'G':2, 'T':3}

def encode_kmer(seq):
    code = 0
    for c in seq:
        code = code * 4 + base2int.get(c, 0)
    return code


def load_barcodes(path):
    bc1_set = set()
    bc2_set = set()

    with open(path) as f:
        for line in f:
            s = line.strip().upper()
            if len(s) != 16:
                continue

            bc2_set.add(encode_kmer(s[:8]))
            bc1_set.add(encode_kmer(s[8:]))

    return bc1_set, bc2_set


def read_fastq_head(path, n):
    """只读取前 n 条 reads（最快）"""
    seqs = []
    with gzip.open(path, "rt") as f:
        for i, line in enumerate(f):
            if i % 4 == 1:
                seqs.append(line.strip())
                if len(seqs) >= n:
                    break
    return seqs


# -------------------------------
# core (hash + rolling)
# -------------------------------
def scan_positions_hash(seqs, bc1_set, bc2_set):
    L = len(seqs[0])
    bc1_hits = np.zeros(L)
    bc2_hits = np.zeros(L)

    mask = (4**7) - 1

    for seq in seqs:
        if len(seq) < 8:
            continue

        code = encode_kmer(seq[:8])

        for i in range(L - 7):

            if code in bc2_set:
                bc2_hits[i] += 1

            if code in bc1_set:
                bc1_hits[i] += 1

            if i < L - 8:
                next_base = base2int.get(seq[i+8], 0)
                code = ((code & mask) * 4) + next_base

    return bc1_hits, bc2_hits


# -------------------------------
# main
# -------------------------------
if __name__ == "__main__":

    t0 = time.time()

    # load barcode
    t1 = time.time()
    bc1_set, bc2_set = load_barcodes(BARCODE_FILE)
    print(f"{len(bc1_set)} bc1 / {len(bc2_set)} bc2 loaded")
    print(f"[time] load barcode: {time.time() - t1:.2f}s")

    # read fastq（只取前 N 条）
    t2 = time.time()
    seqs = read_fastq_head(FASTQ, MAX_READS)
    print(f"reads loaded: {len(seqs)}")
    print(f"[time] read fastq: {time.time() - t2:.2f}s")

    # scan
    t3 = time.time()
    bc1_pos, bc2_pos = scan_positions_hash(seqs, bc1_set, bc2_set)
    print(f"[time] scan: {time.time() - t3:.2f}s")

    # peak
    t4 = time.time()

    total = len(seqs)
    ratio = bc1_pos / total   # 用一个就够了

# 找最大的两个点
    idx = np.argsort(ratio)[-2:]

# 按位置排序（小→大）
    idx.sort()

    bc2_peak = idx[0]
    bc1_peak = idx[1]

    print("\n=== Peak result ===")
    print(f"bc2_peak\t{bc2_peak}\t{ratio[bc2_peak]:.4f}")
    print(f"bc1_peak\t{bc1_peak}\t{ratio[bc1_peak]:.4f}")
