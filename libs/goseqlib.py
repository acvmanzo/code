import datetime
import glob
import logging
import os
import libs.rnaseqlib as rl

def write_gene_goids(assoc_file, out_file):
    '''From the assoc_file ('gene_association.fb.gz' file from Flybase, 
    extracts the GO IDs for each gene and writes to a new file, out_file
    '''
    with open(out_file, 'w') as g:
        with open(assoc_file, 'r') as f:
            d = {}
            for l in f:
                if l[0] == '!':
                    continue
                gene_name = l.split('\t')[2]
                qual = l.split('\t')[3]
                goid  = l.split('\t')[4]
                if qual == 'NOT':
                    continue
                g.write('{}\t{}\n'.format(gene_name, goid))


def gen_gocat_dict(gocat_file):
    '''From the go cat file (gene ontology <-> gene category file; 
    gene_ontology.obo.gz),
    generates a dictionary where the keys are GO IDs and the values are lists
    of the GO categories associated with that ID.
    '''
    with open(gocat_file, 'r') as e:
        #lines = e.readlines()
        #print(lines[:100])
        goids = []
        gonames = []
        nspaces = []
        for l in e:
            if ':' not in l:
                continue
            llist = l.strip('\n').split(': ')
            #print(llist)
            field = llist[0]
            val = llist[1]
            if field  == 'id':
                goids.append(val)
            if field == 'name':
                #print(val)
                gonames.append(val)
            if field == 'namespace':
                nspaces.append(val)
        gotup = zip(goids, gonames, nspaces)
        #print(len(goids), len(gonames))

        dgo = {}
        for item in gotup:
            dgo[item[0]] = [item[1], item[2]]
        #print(dgo)
        return(dgo)

def write_go_gene_categories(gocat_file, assoc_file, out_file):
    '''From a gocat_file (gene ontology <-> gene category file;
    gene_ontology.obo.gz), and an assoc_file (gene <-> GO term; 
    gene_association.fb.gz file from Flybase), writes a new
    file (out_file) with the gene name, associated GO ID, associated categories
    (one gene and GO ID per line), and type of GO term.
    '''
    dictgo = gen_gocat_dict(gocat_file)
    with open(out_file, 'w') as g:
        with open(assoc_file, 'r') as f:
            d = {}
            for l in f:
                if l[0] == '!':
                    continue
                gene_name = l.split('\t')[2]
                qual = l.split('\t')[3]
                goid  = l.split('\t')[4]
                catname = dictgo[goid][0]
                nspace = dictgo[goid][1]
                if qual == 'NOT':
                    continue
                g.write('{}\t{}\t{}\t{}\n'.format(gene_name, goid, catname, 
                    nspace))

def write_go_categories(gocat_file, out_file):
    '''From a gocat_file (gene ontology <-> gene category file; 
    gene_ontology.obo.gz),
    writes a new file (out_file) with each GO ID and 
    associated categories.
    '''
    d = gen_gocat_dict(gocat_file)
    with open(out_file, 'w') as g:
        for k, v in d.items():
            g.write('{}\t{}\t{}\n'.format(k, v[0], v[1]))


def run_goseq(rsd, tool, fdr):
    '''Runs goseq using the script goseq.R
    Input rsd is an RNASeqData object (see rnaseq_settings.py) and the DE tool
    used (e.g., 'edger' or 'deseq'); fdr is the desired FDR for DE genes.
    '''
    #curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    if tool == 'edger':
        defile = rsd.edger_toptags_fdr_name.replace('x', '{:.2f}'.format(fdr))
        allgenefile = os.path.join(rsd.genelist_dirpath, 
                '{}_genes.txt'.format(rsd.genesubset))
        goresultfile = '{}{:.2f}_gene.txt'.format(rsd.goresults_fdr_file, fdr)
        #dbgoresultfile = 'db_' + goresultfile

        cmd = 'Rscript ~/Documents/lab/code/rnaseq_analysis/goseq.R \
        {0} {1} {2} {3} {4} {5} > goseq_{6}.log 2>&1'.format(defile, 
                allgenefile, rsd.edger_counts_file, 
                rsd.gogene_path, rsd.pwfplot_file, goresultfile, fdr)
    
    logging.debug(cmd)
    os.system(cmd)


def batch_run_goseq(exptlist, rnaset, tool):
    '''Runs goseq for each genotype given in exptlist. 
    Input:
    exptlist = list of genotypes 
    rnaset = object of class RNASeqData in the rnaseq_settings module
    tool = software used for analysis (e.g., 'edger' or 'deseq')
    '''
    rnaseqdict = rnaset.__dict__
    exptdirs = [os.path.join(rnaseqdict['{}_dirpath'.format(tool)], 
        rnaset.genesubset, e) for e in exptlist]
    for expt in sorted(exptdirs):
        os.chdir(expt)
        logging.info('%s', expt)
        for fdr in [0.01, 0.05, 0.1]:
            logging.info('%s', fdr)
            run_goseq(rnaset, tool, fdr)


def get_num_goseq(dbtable, tool, gene_subset, defdr, group1, group2, cur):
    '''Checks if the dbtable already contains data from a goseq analysis
    experiment with the given tool, gene_subset, defdr, group1, and group2.
    '''
    checkrowscmd = "select count (*) from (select * from {} where tool = '{}'\
            and gene_subset = '{}' and defdr = {} and group1 = '{}' and \
            group2 = '{}') as foo;".format(dbtable, tool, gene_subset, defdr, 
                    group1, group2)
    cur.execute(checkrowscmd)
    return(cur.fetchone()[0])

def gen_db_goseqfile(goseqfile, db_goseqfile, tool, gene_subset, group1, 
        group2, defdr, delim=','):
    '''Rewrites a file containing the results of goseq analysis to add a 
    column specifying the tool (e.g., edgeR), the gene subset (e.g., 
    prot_coding_genes), the fdr value of the associated DE analysis,
    and two columns specifying the groups being compared
    (ex., group1=Betaintnu_F, group2=CS_F).
    
    Input:
    degenefile = file with results of DE analysis (e.g., toptags_edgeR.csv, 
        output by edgeR.R
    db_degenefile = name of new file that will be written 
    tool = name of DE analysis tool (e.g., edgeR)
    gene_subset = subset of genes analyzed
    group1 = name of 1 group being compared (usually experimental group, like
        Betaintnu_F or lowagg)
    group2 = name of second group being compared (usually control group, like
        CS_F or normalagg)
    defdr = FDR of DE genes used for goseq analysis
    '''
    #print(goseqfile)
    with open(goseqfile, 'r') as f:
        with open(db_goseqfile, 'w') as g:
            next(f)
            for l in f:
                g.write('{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}\n'.format(delim, 
                    l.rstrip('\n'), tool, gene_subset, defdr, group1, group2))


def copy_goseq_dbtable(db_goseqfile, dbtable, cur): 
    '''Copies data from db_goseqfile into table dbtable.
    '''
    logging.debug('cwd=%s', os.getcwd())
    with open(db_goseqfile, 'r') as f:
        info = next(f)
    #print(db_goseqfile)
    #print(info)
    tool, gene_subset, defdr, group1, group2 = info.rstrip('\n').split(',')[7:]
    logging.debug('copy_to_db')
    checkrows = int(get_num_goseq(dbtable, tool, gene_subset, 
        defdr, group1, group2, cur))
    #print(checkrows)
    logging.debug('checkrows=%s', checkrows)
    if checkrows != 0:
        delcmd = "delete from {} where tool = '{}' and gene_subset = '{}' and defdr = {} and group1 = '{}' and group2 = '{}';".format(dbtable, tool, gene_subset, defdr, group1, group2)
        cur.execute(delcmd)
    cur.copy_from(open(db_goseqfile), dbtable, sep=',')


def batch_makecopy_db_goseqfile(exptlist, rnaset, tool, conn):
    '''Batch function for rewriting goseq analysis output files for inclusion
    in the database.
    Input:
    exptlist = list of experiments to copy to database
    rnaset = RNASeqData object
    tool = software used for analaysis (e.g., 'edger' or 'deseq')
    conn = open connection to database using psycopg2
    '''
    rnaseqdict = rnaset.__dict__
    groupfile = rnaseqdict['{}_group_file'.format(tool)]
    gene_subset = rnaset.genesubset
    #goseq_resdir = os.path.join(rnaseqdict['{}_dirpath'.format(tool)], gene_subset)

    #os.chdir(goseq_resdir)
    logging.info('Copying goseq files into database')
    for rd in exptlist:
        logging.info('%s', os.path.basename(rd))
        os.chdir(rd)
        if os.path.exists(groupfile):
            with open(groupfile, 'r') as f:
                group1 = next(f).rstrip('\n')
                group2 = next(f).rstrip('\n')

            goseqfiles = sorted(glob.glob('{}*'.format(rnaseqdict['goresults_fdr_file'])))
            for gsf in goseqfiles:
                print(gsf)
                db_gsf = 'db_' + gsf
                defdr = gsf.split('_')[2] 
                gen_db_goseqfile(gsf, db_gsf, tool, gene_subset, group1,
                        group2, defdr)
                cur = conn.cursor()
                copy_goseq_dbtable(db_gsf, rnaseqdict['goseq_table'], cur)
                cur.close()
            conn.commit()
        else:
            logging.info('No groups file')


def gocat_copy_cmd(gocat_table, goseq_table, tool, gene_subset, defdr, group1,
        group2):
    '''Generates sql command for writing a file with both the GO results 
    and the associated GO categories.
    '''

    cmd = ("COPY ("
            "select gc.go_id, gc.go_cat, go_nspace, gs.fdr_over_pval, "
            "gs.fdr_under_pval, gs.num_de, gs.num_total, gs.tool, "
            "gs.gene_subset, gs.defdr, gs.group1, gs.group2 "
            "from {} as gc inner join {} as gs "
            "using (go_id) "
            "where tool = '{}' and gene_subset = '{}' and defdr = {} "
            "and group1 = '{}' and group2 = '{}' and num_de > 0 "
            "order by gs.fdr_over_pval, num_de DESC"
            ") TO STDOUT CSV HEADER"
            ";").format(gocat_table, goseq_table, tool,
                    gene_subset, defdr, group1, group2)
    return(cmd)

def write_full_go_results(cmd, outfile, cur):
    '''Writes a file with both the GO results and the associated GO categories.
    '''
    logging.debug("copy command: %s", cmd)
    with open(outfile, 'w') as g:
        cur.copy_expert(cmd, g)
    #print(cmd)
    #cur.execute(cmd)
    #print(cur.fetchall())

def batch_write_full_go_results(exptlist, rnaset, tool, conn):
    '''Batch function for writing a file with both the GO results and the
    associated GO categories. 
    Input:
    exptlist = list of experiments to copy to database
    rnaset = RNASeqData object
    tool = software used for analaysis (e.g., 'edger' or 'deseq')
    conn = open connection to database using psycopg2
    '''
        
    rnaseqdict = rnaset.__dict__
    groupfile = rnaseqdict['{}_group_file'.format(tool)]
    gene_subset = rnaset.genesubset
    gocat_table = rnaset.gocat_table
    goseq_table = rnaset.goseq_table

    logging.info('Getting associated GO categories')
    for rd in exptlist:
        logging.info('%s', os.path.basename(rd))
        os.chdir(rd)
        if os.path.exists(groupfile):
            with open(groupfile, 'r') as f:
                group1 = next(f).rstrip('\n')
                group2 = next(f).rstrip('\n')

            goseqfiles = sorted(glob.glob('{}*'.format(rnaseqdict['goresults_fdr_file'])))
            for gsf in goseqfiles:
                print(gsf)
                outfile = 'cat+' + gsf
                defdr = gsf.split('_')[2] 
                cat_cmd = gocat_copy_cmd(gocat_table, goseq_table, tool, 
                    gene_subset, defdr, group1, group2)
                cur = conn.cursor()
                write_full_go_results(cat_cmd, outfile, cur)
                cur.close()
        else:
            logging.info('No groups file')


if __name__ == '__main__':
    import psycopg2
    assoc_file = 'gene_association.fb'
    gocat_file = 'gene_ontology.obo'
    #out_file = 'go_id_cat.txt'
    #out_file = 'go_id_gene_cat.txt'
    #out_file = 'go_id_gene.txt'
    
    #gl.write_gene_goids(assoc_file, out_file)
    #gl.run_goseq(rnaset, tool='edger', fdr=0.05)
    #print(gl.get_gocat(gocat_file))
    #gl.get_go_categories(gocat_file, out_file)
    #gl.write_gene_categories(gocat_file, assoc_file, out_file)
    #conn = psycopg2.connect("dbname={} user=andrea".format('sixrna'))
    #cur = conn.cursor()
    #gocattable = 'r601_go_cat'
    #dbtable = 'goseq_r6_2str'
    #tool = 'edger'
    #gene_subset = 'pcg_r601'
    #defdr = 0.10
    #group1 = 'Betaintnu_F'
    #group2 = 'CS_F'
    #outfile = 'cattest.csv'
    #join_gocat_cmd(gocattable, dbtable, tool, gene_subset, defdr, group1, 
            #group2, outfile, cur)
