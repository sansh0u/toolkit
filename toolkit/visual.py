import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 读取数据
df = pd.read_csv(
    "/mnt/d/prog/KI_0209_sorted.bed.gz",
    sep="\t",
    header=None,
    names=["chr", "start", "end", "name", "score"],
    compression="infer"
)

# 计算长度并过滤
df["length"] = df["end"] - df["start"]
df = df[df["length"] > 0]

def plot_fragment_distribution(df, out, bins=500, max_len=1000, log_y=False):

    df = df[df["length"] <= max_len]

    plt.figure(figsize=(6, 4))

    counts, bin_edges = np.histogram(
        df["length"],
        bins=bins,
        range=(0, max_len)
    )

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    
    plt.plot(bin_centers, counts)

    if log_y:
        plt.yscale("log")

    plt.xlim(0, max_len)

    plt.xlabel("Fragment size")
    plt.ylabel("Count")
    plt.title("Fragment Size Distribution")

    plt.tight_layout()

    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(out, dpi=300)
    plt.close()


plot_fragment_distribution(df, "fragment.png")