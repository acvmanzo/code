import libs.htseqlib as hl
import psycopg2

conn = psycopg2.connect("dbname=rnaseq user=andrea")
hl.batch_run_htseq(conn)
#conn.commit()
#hl.batch_ht_copy_to_dbtable(conn)
#hl.batch_get_select_genes(conn, 'prot_coding_genes')
conn.commit()
conn.close()

#batch_edger_pairwise_DE(EXPTLIST, CTRL)
#groups_edger_DE()
#add_htseq_counts('htseq_count_results_bam2')
