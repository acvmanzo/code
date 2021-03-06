#from rnaseq.correlation import *
import cProfile
import pstats

def testconn():
    conn = psycopg2.connect("dbname=rnaseq user=andrea")
    cur = conn.cursor()


    joincmd = "SELECT t0.tracking_id, t0.berkid, a0.sample, t0.fpkm, t0.fpkm_status, t1.berkid, a1.sample, t1.fpkm, t1.fpkm_status FROM cuff_genes_fpkm_rgam009b as t0 INNER JOIN autin as a0 using (berkid) FULL OUTER JOIN cuff_genes_fpkm_rgam010f as t1 INNER JOIN autin as a1 using (berkid) USING (tracking_id) WHERE t0.tracking_id != '' AND t0.fpkm_status = 'OK' AND t1.fpkm_status = 'OK' ORDER BY tracking_id;"

    cur.execute(joincmd)
    cur.fetchall()
#testconn()

#cProfile.run('testconn()', 'conntest_fetch')
#p=pstats.Stats('conntest_fetch')
#p=pstats.Stats('conntest_fetch')
p=pstats.Stats('correlationprofile')
p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats('cumulative').print_stats(10)
