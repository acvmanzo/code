# Script for clustering samples according to similarity in expression data.

from correlationlib import get_samplename
import numpy as np
import psycopg2
import scipy.spatial
import scipy.cluster
import matplotlib.pyplot as plt

ANALYSIS_DIR = '/home/andrea/Documents/lab/RNAseq/analysis/'
DEND_FILE = ANALYSIS_DIR + 'cufflinks_cluster_pclog2.png'
LEAF_FILE = ANALYSIS_DIR + 'cufflinks_cluster_leaves_pclog2.txt'
LEAF_DATE_FILE = ANALYSIS_DIR + 'cufflinks_cluster_leaves_date_pclog2.txt'



def plot_dend(dend_file, leaf_file, gene_subset_table):
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    cur = conn.cursor()

    berkidcmd = "select distinct berkid from cufflinks_data;"
    cur.execute(berkidcmd)
    berkids = np.array(sorted([x[0] for x in cur.fetchall()]))
    samples = [get_samplename(b, cur) for b in berkids]
    #print(samples)
    cur.close()

    all_fpkm = []
    all_tracking_ids = []

    cur = conn.cursor()
    for berkid in berkids:
        #if gene_subset_table:
        fpkmcmd = "select tracking_id, fpkm from cufflinks_data as t0 inner join prot_coding_genes as t2 using(tracking_id) where t0.berkid = '{0}' and t0.tracking_id != '' order by tracking_id;".format(berkid) 
        #fpkmcmd = "select tracking_id, fpkm from cufflinks_data where berkid = '{}' and tracking_id != '' order by tracking_id;".format(berkid)
        cur.execute(fpkmcmd)
        results = cur.fetchall()
        tracking_id = [x[0] for x in results]
        fpkm = [x[1] for x in results]

        all_fpkm.append(fpkm)
        all_tracking_ids.append(tracking_id)
    cur.close()
    conn.close()

    # Hacky test to make sure the genes being compared are the same.
    all_tracking_ids = np.transpose(np.array(all_tracking_ids, dtype=str))
    hack_test = []
    for row in all_tracking_ids:
        hack_test.append(all(row))
    assert(all(hack_test))

    #all_fpkm = np.array(all_fpkm)
    #take add pseudocount and take log2
    all_fpkm = np.log2(np.array(all_fpkm)+1)


    blabels = samples
    #print(type(blabels))
    dist_fpkm = scipy.spatial.distance.pdist(all_fpkm, 'euclidean')
    avg_cluster = scipy.cluster.hierarchy.average(dist_fpkm)
    plt.figure(figsize=[70,40])
    dend = scipy.cluster.hierarchy.dendrogram(avg_cluster, labels=blabels, leaf_rotation=90)
    plt.savefig(dend_file)
    with open(leaf_file, 'w') as f:
        for label in dend['ivl']:
            f.write('{}\n'.format(label))
    

def dend_analyze(leaf_file, leaf_date_file):
    leaves = []
    with open(leaf_file, 'r') as f:
        for l in f:
            leaves.append(l.strip('\n'))

    rnads = []
    mrnads = []
    cdnads = []
    seqds = []


    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    cur = conn.cursor()
    for leaf in leaves:
        cmd = "select rnad, mrnad, cdnad, seqd from autin where sample = '{}'".format(leaf)
        cur.execute(cmd)
        results = cur.fetchall()
        rnads.append(results[0][0])
        mrnads.append(results[0][1])
        cdnads.append(results[0][2])
        seqds.append(results[0][3])

    datas = zip(leaves, rnads, mrnads, cdnads, seqds)
    with open(leaf_date_file, 'w') as g:
        g.write('Sample\tRNA\tmRNA\tcDNA\tseq\n')
    for data in datas:
        with open(leaf_date_file, 'a') as g:
            g.write('{}\t{}\t{}\t{}\t{}\n'.format(data[0], data[1].isoformat(), 
                data[2].isoformat(), data[3].isoformat(), data[4].isoformat()))

plot_dend(DEND_FILE, LEAF_FILE, True)
dend_analyze(LEAF_FILE, LEAF_DATE_FILE)
