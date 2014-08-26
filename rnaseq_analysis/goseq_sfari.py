#Code for running goseq analysis on Sfari genes, without differential 
#expression analysis, just to see which GO terms are over-represented
#in that list. Instead of giving the bias vector as a list of counts,
#gave it a list of gene lengths.

import libs.goseqlib as gl
import psycopg2

GOSEQFILE = 'go_all_sfari_genes.txt'
DB_GOSEQFILE = 'db_' + GOSEQFILE
TOOL = 'none'
GENE_SUBSET = 'all_sfari'
GROUP1 = 'none'
GROUP2 = 'none'
DEFDR = 0
DBTABLE = 'goseq_r6_2str'
GOCATTABLE = 'r601_go_cat'
FULL_GO_RES_FILE = 'cat+' + GOSEQFILE

conn = psycopg2.connect("dbname=sixrna user=andrea")
cur = conn.cursor()

#gl.gen_db_goseqfile(GOSEQFILE, DB_GOSEQFILE, TOOL, GENE_SUBSET, GROUP1, 
        #GROUP2, DEFDR, delim=',')
#gl.copy_goseq_dbtable(DB_GOSEQFILE, DBTABLE, cur)
cmd = gl.gocat_copy_cmd(GOCATTABLE, DBTABLE, TOOL, GENE_SUBSET, DEFDR, GROUP1,
        GROUP2)
print(cmd)
gl.write_full_go_results(cmd, FULL_GO_RES_FILE, cur)

cur.close()
conn.commit()
conn.close()
