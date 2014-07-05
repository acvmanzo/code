import libs.rnaseqlib as rl
import psycopg2

table = 'htseq_prot_coding_genes'

conn = psycopg2.connect("dbname=rnaseq user=andrea")
cur = conn.cursor()
#cmd = "SELECT EXISTS( SELECT 1 FROM   pg_catalog.pg_class c JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE  n.nspname = 'public' AND    c.relname = '{}');;".format(table)
#cur.execute(cmd)
#r = cur.fetchone()[0]
#print(r)
#print(r == True)

r = rl.check_table_exists(table, cur)
if r:
    print('yup')

cur.close()
conn.commit()
conn.close()
