from correlation import *

MAXFPKMPLOT = 500

def get_ids(sid):
    idlist = ['{}_clc'.format(sid), '{}_th'.format(sid)]
    return(idlist)

cuffpaths = ['/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM009B/tux_results/tophat_run3/cufflinks_out_3', '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM010F/tux_results/tophat_run2/cufflinks_out', '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGSJ006G_index24/tux_results/tophat_run1/cufflinks_out']
corrfile = '/home/andrea/rnaseqanalyze/sequences/CSM/correlations_clc_th/correlations.txt'
#savefigdir = '/home/andrea/rnaseqanalyze/sequences/CSM/correlations_clc_th'
savefigdir = '/home/andrea/rnaseqanalyze/sequences/CSM/correlations_clc_th_cond1'

print('opening connection')
conn = psycopg2.connect("dbname=rnaseq user=andrea")
cur = conn.cursor()
mainberkids = ['RGAM009B', 'RGAM010F']

#mainberkid = 'RGAM009B'
for mainberkid in mainberkids:
    sample = get_samplename(mainberkid, cur)
    table0 = 'clcbio_{}'.format(mainberkid)
    table1 = 'cuff_genes_fpkm_{}'.format(mainberkid)
    print(table1)
    berkids = get_ids(mainberkid)
    samples = get_ids(sample) 

    selectlist = ['clc.feature_id', 'clc.rpkm', 'th.fpkm']
    selectstring = ', '.join(selectlist) 


    print('joining and querying tables')
    #joincmd = "SELECT {2} FROM {0} as clc INNER JOIN {1} as th ON (feature_id=gene_short_name) ORDER BY tracking_id;".format(table0, table1, selectstring)
    joincmd = "SELECT {2} FROM {0} as clc INNER JOIN {1} as th ON (feature_id=gene_short_name) WHERE NOT (th.fpkm = 0 AND clc.rpkm != 0) ORDER BY tracking_id;".format(table0, table1, selectstring)
    
    print(joincmd)
    joinedarray = join_db_table(joincmd, cur)

    array = np.transpose(joinedarray)
    colnames = selectlist
    fpkms = [array[x][:].astype(np.float) for x in [colnames.index('clc.rpkm'),colnames.index('th.fpkm')]]
    r = get_correlation(fpkms)
    save_corr_file(r, berkids[0], samples[0], berkids[1], samples[1], corrfile)

    print('plotting scatter plots')
    fpkmlim = max([axislim(x) for x in fpkms])
    fig1 = plt.figure(figsize=(10, 5))
    plot_scatter(fpkms, berkids, samples, r, 121, fpkmlim)
    plot_scatter(fpkms, berkids, samples, r, 122, MAXFPKMPLOT)
    plt.tight_layout()
    plt.savefig(os.path.join(savefigdir, make_figname(berkids, samples, 'correlation')))
    plt.close()
    print('plotting histograms')
    fig1 = plt.figure(figsize=(10, 10))
    plot_hist(fpkms, berkids, samples, fpkmlim, 311)
    plot_hist(fpkms, berkids, samples, MAXFPKMHIST, 312)
    plot_hist(fpkms, berkids, samples, 0.008*MAXFPKMHIST, 313)
    plt.savefig(os.path.join(savefigdir, make_figname(berkids, samples, 'hist')))
    plt.tight_layout()
    plt.close()


