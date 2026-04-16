import snapatac2 as snap



data_path = "/mnt/d/download/HYS_sample1_sorted.bed.gz"
adata = snap.pp.read_fragment(
    data_path
)


#qc_plot(data)
snap.pp.calculate_qc_metrics(adata)
snap.pl.qc(adata)



def qc_plot(data):
    '''
    绘制质量控制图
    '''
    