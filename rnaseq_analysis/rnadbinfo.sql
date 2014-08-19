-- SQL code for manipulating/testing tables in the rnaseq database.

-- Creating a foreign database wrapper so that I can access the data in the
-- autin table from the rnaseq database.

-- CREATE EXTENSION postgres_fdw;
-- create server andreaserver FOREIGN DATA WRAPPER postgres_fdw OPTIONS (dbname 'andrea');
-- create user mapping for andrea server andreaserver options (user 'andrea');

-- -- Copied from the last dump.
-- CREATE FOREIGN TABLE autin (
    -- genotype character varying(80) NOT NULL,
    -- tube integer,
    -- sex character varying(80) NOT NULL,
    -- frozend date NOT NULL,
    -- rnad date,
    -- rnaconc real,
    -- mrnad date,
    -- cdnad date,
    -- indexnum integer,
    -- sample character varying(80),
    -- seqd date,
    -- thawed integer,
    -- toseq boolean,
    -- samplenum integer,
    -- berkid character varying(10),
    -- sentd date,
    -- qbitngul real,
    -- qbitd date,
    -- seq_received boolean,
    -- use_seq boolean
-- )
-- SERVER andreaserver;


-- ALTER FOREIGN TABLE autin ADD COLUMN use_seq boolean;

-- -- To count the number of rows in a select query:

-- select count (*) from (select autin.berkid from cuff_genes_fpkm_rgam009b inner join autin on (autin.berkid = cuff_genes_fpkm_rgam009b.sample)) as foo;


-- To join tables for correlation tests (double join method)

-- SELECT t1.tracking_id, t1.berkid, a1.sample, t1.fpkm, t1.fpkm_status, t2.berkid,
-- a2.sample, t2.fpkm, t2.fpkm_status
-- FROM 
    -- cuff_genes_fpkm_rgam009b as t1 INNER JOIN autin as a1 using (berkid)
    -- FULL OUTER JOIN
    -- cuff_genes_fpkm_rgam010f as t2 INNER JOIN autin as a2 using (berkid)
    -- USING (tracking_id) 
-- WHERE t1.tracking_id != '' AND t1.fpkm_status = 'OK' AND t2.fpkm_status = 'OK' 
-- ORDER BY tracking_id;

-- -- To check the # of rows in the joined table.

-- select count (*) from (
-- SELECT t1.tracking_id, t1.fpkm, t1.fpkm_status, t2.fpkm, t2.fpkm_status,
-- t1.berkid, t2.berkid, a1.sample, a2.sample
-- FROM 
    -- cuff_genes_fpkm_rgam009b as t1 INNER JOIN autin as a1 using (berkid)
    -- FULL OUTER JOIN 
    -- cuff_genes_fpkm_rgam010f as t2 INNER JOIN autin as a2 using (berkid)
    -- USING (tracking_id) 
-- WHERE t1.tracking_id != '' AND t1.fpkm_status = 'OK' AND t2.fpkm_status = 'OK' 
-- ORDER BY tracking_id) as foo;

-- # of rows in the joined tables are different from the single tables because
-- not all the fpkms are 'OK'. Because I ran the function without looking for
-- novel transcripts and with reference to the genome, the number of rows in the
-- single tables are the same.


-- For looking at correlation between CLCBio and Tophat.
-- DROP TABLE clcbio_rgam009b;
-- CREATE TABLE clcbio_rgam009b (
    -- feature_id varchar(200),
    -- rpkm double precision
-- );

-- \copy clcbio_rgam010f from '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM010F/clc_results/RGAM010F_RNA-Seq_rpkm.txt'; 
-- \copy clcbio_rgam009b from '/home/andrea/rnaseqanalyze/sequences/CSM/Sample_RGAM009B/clc_results/CS_MB_RGAM009B_RNA-Seq_rpkm.txt';

-- Notes:
-- Correlation between clc and th is off; th seems to assign higher fpkms than
-- clc. Doing it again excluding the samples where th gives an fpkm of 0 and clc
-- gives an fpkm of not 0. Saved results in folder 
-- savefigdir = '/home/andrea/rnaseqanalyze/sequences/CSM/correlations_clc_th_cond1'


-- Create one table to contain all the cufflinks mapping data
-- CREATE TABLE cufflinks_data (
    -- tracking_id character varying(20),
    -- class_code character varying(2),
    -- nearest_ref_id character varying(2),
    -- gene_id character varying(20),
    -- gene_short_name character varying(100),
    -- tss_id character varying(2),
    -- locus character varying(100),
    -- length character varying(2),
    -- coverage character varying(2),
    -- FPKM double precision ,
    -- FPKM_conf_lo double precision,
    -- FPKM_conf_hi double precision,
    -- FPKM_status character varying(10),
    -- berkid character varying(20),
    -- unique (tracking_id, berkid)
-- );

-- SELECT COUNT (*) FROM (
-- SELECT t0.tracking_id, t0.berkid, t0.fpkm, t0.fpkm_status, t1.berkid, t1.fpkm, t1.fpkm_status 
    -- FROM cufflinks_data as t0 
        -- FULL OUTER JOIN 
        -- cufflinks_data as t1 
            -- USING (tracking_id)
            -- WHERE t0.berkid = 'RGAM009B' AND t1.berkid = 'RGAM010F' 
            -- AND t0.tracking_id != '' AND t0.fpkm_status = 'OK' AND t1.fpkm_status = 'OK' 
            -- ORDER BY tracking_id
            -- ) as foo
 --            ;


-- Create a table of protein-coding genes; output of QueryBuilder on Flybase where I selected genes
-- that matched the class 'protein_coding_genes'

-- DROP TABLE prot_coding_genes;
-- CREATE TABLE prot_coding_genes (
    -- tracking_id character varying(20),
    -- gene_long_name character varying(100),
    -- gene_short_name character varying(100)
-- );

-- -- Copy into table.
-- -- \copy prot_coding_genes from '/home/andrea/rnaseqanalyze/references/protein_coding_genes/flybase_results_protein_coding_genes_dmel_symbol.txt';
-- \copy prot_coding_genes from '/home/andrea/rnaseqanalyze/references/gene_lists/protein_coding_genes/prot_coding_genes_r6.01_db.txt';

-- create view test as select t0.tracking_id, t0.berkid as berkid0, t0.fpkm as fpkm0, t1.berkid as berkid1, t1.fpkm as fpkm1 from cufflinks_data as t0 full outer join cufflinks_data as t1 using (tracking_id) where t0.berkid = 'RGAM009G' and t1.berkid = 'RGAM011A' and t0.tracking_id != '' and t0.fpkm_status = 'OK' and t1.fpkm_status = 'OK' order by tracking_id;

-- Testing code for doing a join with the protein_coding_genes table
-- select count (*) from (
-- select t0.tracking_id, t0.berkid as berkid0, t0.fpkm as fpkm0, t1.berkid as berkid1, t1.fpkm as fpkm1 
    -- from 
        -- cufflinks_data as t0 
        -- full outer join 
        -- cufflinks_data as t1 
            -- using (tracking_id)
        -- inner join
        -- prot_coding_genes as t2 
            -- using (tracking_id)
        -- where t0.berkid = 'RGAM009G' and t1.berkid = 'RGAM011A' and t0.tracking_id != '' and t0.fpkm_status = 'OK' and t1.fpkm_status = 'OK' 
            -- order by tracking_id
-- ) as foo
-- ;


-- Create one table to contain all the cufflinks mapping data
-- CREATE TABLE clc_data (
    -- gene_short_name character varying(100),
    -- exp_vale double precision,
    -- trans_annot int,
    -- trans_detected int,
    -- exon_length int,
    -- unique_gene_reads int,
    -- tot_gene_reads int,
    -- unique_exon_reads int,
    -- tot_exon_reads int,
    -- ratio_exon_reads real,
    -- unique_exon_exon_reads int,
    -- total_exon_exon_reads int,
    -- unique_intron_exon_reads int,
    -- total_intron_exon_reads int,
    -- exons int,
    -- put_exons int,
    -- rpkm double precision,
    -- med_cov real,
    -- chrom varchar(200),
    -- chrom_start int,
    -- chrom_end int,
    -- berkid varchar(20)
-- );

-- Testing using htseq and SERE
-- CREATE TABLE htseq_r6_2str (
    -- gene_short_name varchar(100),
    -- counts int,
    -- berkid varchar(20),
    -- unique(gene_short_name, berkid)
-- );

-- \copy htseq from '/home/andrea/bookmarks/analysis/results_tophat/RGAM009H/tophat_out/htseq_results_edit_berkid.txt';
-- \copy htseq from '/home/andrea/bookmarks/analysis/results_tophat/RGAM009D/tophat_out/htseq_results_edit_berkid.txt';
-- \copy htseq from '/home/andrea/bookmarks/analysis/results_tophat/RGSJ006H/tophat_out/htseq_results_edit_berkid.txt';
-- \copy htseq from '/home/andrea/bookmarks/analysis/results_tophat/RGSJ007D/tophat_out/htseq_results_edit_berkid.txt';

-- select count (*) from (
-- \copy (select t0.gene_name, t0.counts as RGSJ007D, t1.counts as RGSJ006H from htseq as t0 inner join htseq as t1 using (gene_name) where t0.berkid = 'RGSJ007D' and t1.berkid = 'RGSJ006H' order by gene_name) TO '/home/andrea/bookmarks/analysis/cg34127m_htseq_test.txt';
-- ) as foo
-- ;
-- \copy prot_coding_genes  to '/home/andrea/bookmarks/analysis/test.txt';

-- alter table htseq_2str rename column gene_name to gene_short_name;
-- alter table htseq_un rename column gene_name to gene_short_name;

-- DROP TABLE htseq_gene;
-- CREATE TABLE htseq_gene (
    -- gene_short_name varchar(100),
    -- counts int,
    -- berkid varchar(20)
-- );

-- \copy htseq_gene from '/home/andrea/bookmarks/analysis/results_tophat/RGSJ007D/tophat_out/htseq_results_edit_gene_berkid.txt';
-- \copy htseq_gene from '/home/andrea/bookmarks/analysis/results_tophat/RGSJ006H/tophat_out/htseq_results_edit_gene_berkid.txt';

-- \copy (select t0.gene_short_name, t0.counts as RGSJ007D, t1.counts as RGSJ006H from htseq_gene as t0 inner join htseq_gene as t1 using (gene_short_name) inner join prot_coding_genes as t2 using (gene_short_name) where t0.berkid = 'RGSJ007D' and t1.berkid = 'RGSJ006H' order by gene_short_name) TO '/home/andrea/bookmarks/analysis/cg34127m_htseq_test_pcg.txt';
-- select t0.gene_short_name, t0.counts as RGSJ007D, t1.counts as RGSJ006H from htseq_gene as t0 inner join htseq_gene as t1 using (gene_short_name) inner join prot_coding_genes as t2 using (gene_short_name) where t0.berkid = 'RGSJ007D' and t1.berkid = 'RGSJ006H' order by gene_short_name; 
-- select t0.gene_short_name, t0.counts as RGSJ007D, t1.counts as RGSJ006H from htseq_gene as t0 inner join htseq_gene as t1 using (gene_short_name) where t0.berkid = 'RGSJ007D' and t1.berkid = 'RGSJ006H' order by gene_short_name; 

-- CREATE TABLE htseq_prot_coding_genes (
    -- gene_name varchar(100),
    -- counts int,
    -- berkid varchar(20),
    -- unique (gene_name, berkid)
-- );

-- Creates a table with the alignment stats from clc and tophat mapping; files used to populate the table are output by the script align_summary.py
-- DROP TABLE aligninfo;
-- CREATE TABLE aligninfo (
    -- berkid varchar(20),
    -- sample varchar(20),
    -- input int,
    -- mapped int,
    -- pmapped real,
    -- multimapped int,
    -- pmulti real,
    -- aligner varchar(40)
-- );

-- \copy aligninfo from '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat/tophat_all_align_summarywithal.txt';
-- \copy aligninfo from '/home/andrea/Documents/lab/RNAseq/analysis/CLC_results/clc_all_align_summarywithal.txt';
-- \copy aligninfo from '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat_2str/tophat_all_align_summarywithal.txt';

-- \copy (select t0.berkid, t0.sample, t1.input as total_sequenced_reads, t0.mapped as clc_mapped, t1.mapped as th_mapped, t1.mapped-t0.mapped as diff_thmap_clcmap, t0.pmapped as clc_percent_mapped, t1.pmapped as th_percent_mapped, t0.mapped-t0.multimapped as clc_unique, (t0.mapped-t0.multimapped)/t1.input::float as clc_ratio_totalseq_unique, t1.mapped-t1.multimapped as th_unique, (t1.mapped-t1.multimapped)/t1.input::float as th_ratio_totalseq_unique from aligninfo as t0 inner join aligninfo as t1 using (berkid) where t0.aligner = 'clc' and t1.aligner = 'tophat' order by sample) to 'clc_tophat_mapping.csv' csv header;
-- \copy (select t0.berkid, t0.sample, t1.input as total_sequenced_reads, t0.mapped as unstranded, t1.mapped as secondstr, t0.mapped-t1.mapped as diff_un_2str, t0.pmapped as un_percent_mapped, t1.pmapped as secstr_percent_mapped, t0.mapped-t0.multimapped as un_unique, (t0.mapped-t0.multimapped)/t1.input::float as un_ratio_totalseq_unique, t1.mapped-t1.multimapped as secstr_unique, (t1.mapped-t1.multimapped)/t1.input::float as secstr_ratio_totalseq_unique from aligninfo as t0 inner join aligninfo as t1 using (berkid) where t0.aligner = 'tophat' and t1.aligner = 'tophat_2str' order by sample) to 'tophat_un_2str_mapping.csv' csv header;
-- \copy (select t0.berkid, t0.sample, t1.input as total_sequenced_reads, t0.mapped as clc_mapped, t1.mapped as th_mapped, t1.mapped-t0.mapped as diff_thmap_clcmap, t0.pmapped as clc_percent_mapped, t1.pmapped as th_percent_mapped, t0.mapped-t0.multimapped as clc_unique, (t0.mapped-t0.multimapped)/t1.input::float as clc_ratio_totalseq_unique, t1.mapped-t1.multimapped as th_unique, (t1.mapped-t1.multimapped)/t1.input::float as th_ratio_totalseq_unique from aligninfo as t0 inner join aligninfo as t1 using (berkid) where t0.aligner = 'clc' and t1.aligner = 'tophat_2str' order by sample) to 'clc_tophat_mapping.csv' csv header;


-- Creates a table for the DE gene data.
-- DROP TABLE degenes;
-- CREATE TABLE degenes_r6_2str (
    -- gene varchar(100),
    -- logfc double precision,
    -- logcpm double precision,
    -- pvalue double precision, 
    -- fdr double precision,
    -- tool varchar(40),
    -- gene_subset varchar(50),
    -- group1 varchar(50),
    -- group2 varchar(50),
    -- UNIQUE (gene, tool, gene_subset, group1, group2)
-- );

-- \copy (select * from degenes where group1 = 'lowagg' and group2 = 'normagg' and fdr < 0.05) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/lowagg_vs_normagg_CS/toptags_edgeR_fdr05.csv' csv header;
-- \copy (select * from degenes where group1 = 'CG34127_M' and group2 = 'CS_M' and fdr < 0.05) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/CG34127_M/toptags_edgeR_fdr05.csv' csv header;

-- Selects different combinations of the DE_genes data.
-- select t0.gene, t0.group1, 2^t0.logfc as foldchange, t1.group1, 2^t1.logfc as foldchange
-- select t0.gene
    -- from degenes as t0 
        -- inner join 
        -- degenes as t1 
        -- using (gene)
        -- inner join
        -- degenes as t2
        -- using (gene) 
        -- inner join
        -- degenes as t3
        -- using (gene) 
    -- where 
    -- t0.group1 = 'en_M' and t1.group1 = 'CG34127_M' and t2.group1 = 'NrxI_M' and t3.group1 = 'pten_M' and
    -- t0.group1 = 'en_M' and t1.group1 = 'CG34127_M' and t2.group1 = 'NrxI_M' and t3.group1 = 'pten_M' and
    -- t0.fdr < 0.05 and t1.fdr < 0.05 and t2.fdr < 0.05 and t3.fdr < 0.05
    -- order by gene
-- ;

-- \copy (select gene, 2^logfc as foldchange, fdr as adjusted_pvalue from degenes where group1 = 'CG34127_M' and fdr < 0.05 order by fdr) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/CG34127_M/toptags_edgeR_fdr05_fc.csv' csv header ;
-- \copy (select gene, 2^logfc as foldchange, fdr as adjusted_pvalue from degenes where group1 = 'en_M' and fdr < 0.05 order by fdr) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/en_M/toptags_edgeR_fdr05_fc.csv' csv header ;
-- \copy (select gene, 2^logfc as foldchange, fdr as adjusted_pvalue from degenes where group1 = 'NrxI_M' and fdr < 0.05 order by fdr) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/NrxI_M/toptags_edgeR_fdr05_fc.csv' csv header ;
-- \copy (select gene, 2^logfc as foldchange, fdr as adjusted_pvalue from degenes where group1 = 'lowagg' and group2 = 'normagg' and fdr < 0.05 order by fdr) to '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes/lowagg_vs_normagg_CS/toptags_edgeR_fdr05_fc.csv' csv header ;


-- -- Finds the primary fbgn IDs of DE genes.
-- select de.gene as gene, gff.fbgn_id as fbgn_id from
-- degenes as de
-- inner join
-- gff_genes as gff
    -- on (de.gene = gff.name_name)
    -- where de.fdr < 0.05 
    -- and de.gene_subset = 'sfari_r557' 
    -- and de.group1 = 'lowagg_CS'
    -- and de.group2 = 'ctrlagg_CS'
    -- and gff.gff_file = 'dmel-all-filtered-r5.57.gff'
    -- order by gene;

-- -- Finds the human homologs of DE genes.
-- -- 1. First, finds the primary fbgns of the DE genes.
-- -- 2. Next, finds the homolog-specific fly symbol of the DE genes using 
-- --    the pfbgns.
-- -- 3. Next, finds the the human homolog, the weighted score, and the 
-- --    databases used for homolog prediction using the homolog-specific 
-- --    fly_sym.

-- select distinct hom.fly_sym, hom.human_sym, final.logfc, hom.weighted_score, 
    -- hom.prediction_db from 
-- ( select hp.fly_sym, hid.logfc from 
    -- (select de.gene as gene, gff.fbgn_id as fbgn_id, de.logfc as logfc from
    -- degenes as de
    -- inner join
    -- gff_genes as gff
        -- on (de.gene = gff.name_name)
        -- where de.fdr < 0.05 
        -- and de.gene_subset = 'sfari_r557' 
        -- and de.group1 = 'CG34127_M'
        -- and de.group2 = 'CS_M' 
        -- and gff.gff_file = 'dmel-all-filtered-r5.57.gff'
    -- ) as hid
    -- inner join 
    -- homolog_pfbgns as hp
        -- on (hp.pfbgn = hid.fbgn_id)
    -- ) as final
    -- inner join
    -- homologs as hom
    -- on (final.fly_sym = hom.fly_sym)
    -- order by final.logfc desc
    -- -- ;


-- \copy (
-- select count (*) from (
-- select distinct gene from degenes where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.5
-- ) 
-- as foo;
-- to '/home/andrea/Documents/lab/RNAseq/analysis/edger/prot_coding_genes/GO_analysis/de_all_fdr05.txt'
-- select count (*) from (
-- \copy ( select distinct g.fbgn_id from degenes as d inner join gff_genes as g on (g.name_name = d.gene) where d.tool = 'edger' and d.gene_subset = 'bwa_r557_ralph_mt_ex' and d.fdr < 0.05 and g.gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/Documents/lab/RNAseq/analysis/edger/bwa_r557_ralph_mt_ex/GO_analysis/de_all_fdr05.txt'
-- as foo;
-- \copy ( select distinct g.fbgn_id from degenes_un as d inner join gff_genes as g on (g.name_name = d.gene) where d.tool = 'edger' and d.gene_subset = 'prot_coding_genes_ralph_mt_ex' and d.fdr < 0.05 and d.group1 != 'lowagg_CS' and d.group1 != 'aut_mut_m' and d.group1 != 'aut_mut_f' and d.group1 != 'lowagg_all' and g.gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_un/prot_coding_genes_ralph_mt_ex/GO_analysis/de_allgen_fdr05.txt'
-- \copy ( select distinct g.fbgn_id from degenes_un as d inner join gff_genes as g on (g.name_name = d.gene) where d.tool = 'edger' and d.gene_subset = 'bwa_r557_ralph_mt_ex' and d.fdr < 0.05 and d.group1 != 'lowagg_CS' and d.group1 != 'aut_mut_m' and d.group1 != 'aut_mut_f' and d.group1 != 'lowagg_all' and g.gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_un/bwa_r557_ralph_mt_ex/GO_analysis/de_allgen_fdr05.txt'
-- \copy ( select distinct g.name_name from degenes_un as d inner join gff_genes as g on (g.name_name = d.gene) where d.tool = 'edger' and d.gene_subset = 'prot_coding_genes_ralph_mt_ex' and d.fdr < 0.05 and d.group1 != 'lowagg_CS' and d.group1 != 'aut_mut_m' and d.group1 != 'aut_mut_f' and d.group1 != 'lowagg_all' and g.gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_un/prot_coding_genes_ralph_mt_ex/GO_analysis/de_allgen_name_fdr05.txt'

-- \copy ( select distinct g.fbgn_id from degenes_un as d inner join gff_genes as g on (g.name_name = d.gene) where d.tool = 'edger' and d.gene_subset = 'prot_coding_genes_ralph_mt_ex' and d.fdr < 0.05 and (d.group1 = 'NrxI_M' or d.group1 = 'CG34127_M' or d.group1 = 'NrxI_M') and d.group2 = 'CS_M' and g.gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_un/prot_coding_genes_ralph_mt_ex/GO_analysis/de_CGenNIM_fdr05.txt'
-- \copy ( select distinct g.fbgn_id from degenes as d inner join gff_genes as g on (g.name_name = d.gene) where d.tool = 'edger' and d.gene_subset = 'bwa_r557_ralph_mt_ex' and d.fdr < 0.05 and d.group1 = 'NrxI_M' and d.group2 = 'CS_M' and g.gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/Documents/lab/RNAseq/analysis/edger/bwa_r557_ralph_mt_ex/GO_analysis/de_NrxI_M_fdr05.txt'

-- -- Create table with gene lengths for every gene.
-- create table r601_gene_length (
    -- gene_name varchar(100),
    -- gene_bp int,
    -- unique (gene_name, gene_bp)
-- );

-- \copy r601_gene_length from '/home/andrea/rnaseqanalyze/references/dmel-r6.01/dmel-all-r6.01_gene_length.txt';
-- select count (*) from (
-- select gene_name, gene_bp 
-- from r601_gene_length
-- inner join
-- pcg_r601
-- on (gene_name = gene_short_name)
-- ) as foo
-- ;
-- \copy (select gene_name, gene_bp from r601_gene_length inner join pcg_r601 on (gene_name = gene_short_name)) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_r6_2str/sfari_r601_goseq/pcg_r601_gene_lengths.txt'


-- Create table with GO id for every gene.
-- drop table r601_gene_go;
-- create table r601_gene_go (
    -- gene_name varchar(100),
    -- go_id varchar(20),
    -- go_cat varchar(500),
    -- go_nspace varchar(100),
    -- unique (gene_name, go_id, go_cat)
-- );

-- \copy r601_gene_go from '/home/andrea/rnaseqanalyze/references/dmel-r6.01/go_id_gene_cat_uniq.txt'

-- -- Create table with go category for every GO ID.
-- create table r601_go_cat (
    -- go_id varchar(20),
    -- go_cat varchar(500),
    -- go_nspace varchar(100),
    -- unique (go_id, go_cat, go_nspace)
-- )
-- ;

-- \copyr601_go_cat from '/home/andrea/rnaseqanalyze/references/dmel-r6.01/go_id_cat.txt';

-- Brain genes.
-- \copy (select tracking_id from brain_r557 intersect select fbgn_id from gff_genes where gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/brain_r557/GO_analysis/brain_fbgns.txt';

-- Protein coding genes.
-- \copy (select gene_name from prot_coding_genes inner join r557_gene_length on (gene_short_name = gene_name) order by gene_name) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/all_genes.txt';
-- \copy (select tracking_id from prot_coding_genes intersect select fbgn_id from gff_genes where gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/GO_analysis/all_fbgns.txt';

-- Gene lengths for protein coding genes.
-- \copy (select gene_bp from prot_coding_genes inner join r557_gene_length on (gene_short_name = gene_name) order by gene_name) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/gene_lengths.txt';

-- GO IDs for protein coding genes.
-- \copy (select distinct gene_name, go_id from prot_coding_genes inner join r557_gene_go on (gene_short_name = gene_name) order by gene_name) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/genes_go.txt';

-- DE genes for protein coding genes.
-- \copy ( select distinct gene from degenes where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.05 and group1 != 'lowagg_all' and group1 != 'lowagg_CS' and group1 != 'aut_mut_m' and group1 != 'aut_mut_f') to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/GO_analysis/de_all_fdr05.txt'
-- \copy ( select distinct g.fbgn_id from degenes as d inner join gff_genes as g on (g.name_name = d.gene) where d.tool = 'edger' and d.gene_subset = 'prot_coding_genes' and d.fdr < 0.05 and (d.group1 != 'lowagg_all' and d.group1 != 'lowagg_CS' and d.group1 != 'aut_mut_m' and d.group1 != 'aut_mut_f') and gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/GO_analysis/fbgn_de_all_fdr05.txt'
-- select distinct g.fbgn_id 
-- from degenes as d 
    -- inner join gff_genes as g 
    -- on (g.name_name = d.gene) 
    -- where d.tool = 'edger' and d.gene_subset = 'prot_coding_genes' and 
    -- d.fdr < 0.1 and gff_file = 'dmel-all-filtered-r5.57.gff' 
    -- and group1 = 'NrxIV_F'
    -- ;

-- Create GOseq table.
-- drop table goseq_r6_2str cascade;
-- create table goseq_r6_2str (
    -- go_id varchar(20),
    -- over_pval double precision,
    -- under_pval double precision,
    -- num_DE int,
    -- num_total int,
    -- fdr_over_pval double precision,
    -- fdr_under_pval double precision, 
    -- tool varchar(40),
    -- gene_subset varchar(50),
    -- defdr double precision,
    -- group1 varchar(50),
    -- group2 varchar(50),
    -- unique (go_id, gene_subset, defdr, group1, group2)
-- );

-- \copy goseq from '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/GO_analysis/db_de_all_fdr05_goseq.txt' (delimiter ' ');

-- Get GO categories from GO IDs for enriched GO terms.
-- select gc.go_id, gc.go_cat, go_nspace, gs.fdr_over_pval, gs.fdr_under_pval, gs.num_de, gs.num_total, gs.tool, gs.gene_subset, gs.defdr, gs.group1, gs.group2
-- from r601_go_cat as gc
-- inner join
-- goseq_r6_2str as gs
-- using (go_id)
-- -- where gs.fdr_over_pval < 0.05 or gs.fdr_under_pval < 0.05
-- order by gs.fdr_over_pval
-- ;

-- select g.fbgn_id, g.name_name, d.logfc, d.fdr
-- from degenes as d 
-- inner join gff_genes as g 
-- on (g.name_name = d.gene) 
-- where d.tool = 'edger' and d.gene_subset = 'prot_coding_genes' and gff_file = 'dmel-all-filtered-r5.57.gff'
-- and g.name_name ~ 'Rp...'
-- -- and d.fdr < 0.1 
-- and group1 = 'Betaintnu_F' 
-- -- order by fdr;
-- order by @d.logfc desc
-- ;

-- -- -- Genes that are in the 3 aggression mutants but not in the other males.
-- create view degenes_pcg_r601_agg_05 as (
-- select g.fbgn_id 
-- from degenes_r6_2str as d 
-- inner join gff_genes as g on (g.name_name = d.gene) 
-- where d.tool = 'edger' and d.gene_subset = 'pcg_r601' and d.fdr < 0.05 and 
-- gff_file = 'dmel-all-r6.01.gff' and group1 = 'NrxI_M' 
-- UNION
-- select g.fbgn_id 
-- from degenes_r6_2str as d 
-- inner join gff_genes as g on (g.name_name = d.gene) 
-- where d.tool = 'edger' and d.gene_subset = 'pcg_r601' and d.fdr < 0.05 and 
-- gff_file = 'dmel-all-r6.01.gff' and group1 = 'CG34127_M' 
-- UNION
-- select g.fbgn_id 
-- from degenes_r6_2str as d 
-- inner join gff_genes as g on (g.name_name = d.gene) 
-- where d.tool = 'edger' and d.gene_subset = 'pcg_r601' and d.fdr < 0.05 and 
-- gff_file = 'dmel-all-r6.01.gff' and group1 = 'en_M' 
-- EXCEPT
-- select g.fbgn_id 
-- from degenes_r6_2str as d 
-- inner join gff_genes as g on (g.name_name = d.gene) 
-- where d.tool = 'edger' and d.gene_subset = 'pcg_r601' and d.fdr < 0.05 and 
-- gff_file = 'dmel-all-r6.01.gff' and group1 = 'NrxIV_M' 
-- -- INTERSECT
-- EXCEPT
-- select g.fbgn_id 
-- from degenes_r6_2str as d 
-- inner join gff_genes as g on (g.name_name = d.gene) 
-- where d.tool = 'edger' and d.gene_subset = 'pcg_r601' and d.fdr < 0.05 and 
-- gff_file = 'dmel-all-r6.01.gff' and group1 = 'pten_M' 
-- -- INTERSECT
-- except
-- select g.fbgn_id 
-- from degenes_r6_2str as d 
-- inner join gff_genes as g on (g.name_name = d.gene) 
-- where d.tool = 'edger' and d.gene_subset = 'pcg_r601' and d.fdr < 0.05 and 
-- gff_file = 'dmel-all-r6.01.gff' and group1 = 'Nhe3_M'
-- -- INTERSECT
-- except
-- select g.fbgn_id 
-- from degenes_r6_2str as d 
-- inner join gff_genes as g on (g.name_name = d.gene) 
-- where d.tool = 'edger' and d.gene_subset = 'pcg_r601' and d.fdr < 0.05 and 
-- gff_file = 'dmel-all-r6.01.gff' and group1 = 'Betaintnu_M' 
-- )
-- ;


-- -- Shows samples the above are DE in:
-- \copy (select g.name_name, g.fbgn_id, avg(d.fdr) as avg_adjpval, 2^avg(d.logfc) as avg_fc, array_agg(d.group1) from degenes_pcg_r601_agg_05 as agg inner join gff_genes as g on (agg.fbgn_id = g.fbgn_id) inner join degenes_r6_2str as d on (g.name_name = d.gene) where d.fdr < 0.05 and d.tool = 'edger' and g.gff_file = 'dmel-all-r6.01.gff' and d.gene_subset = 'pcg_r601' and d.group1 ~ '..M' group by g.name_name, g.fbgn_id order by g.name_name) to '/home/andrea/Documents/lab/RNAseq/analysis/decounts/results_tophat_r6_2str/pcg_r601/lowagg_males_degenes_edger_0.05.csv' csv header;



-- CREATE TABLE tempfbgns (
    -- fbgn varchar(20)
-- ;

-- \copy (select tracking_id from sfari_r557) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/GO_analysis/sfari_fbgns.txt';

-- -- INNER JOIN BETWEEN SFARI_R557 AND DEGENES FDR < 0.05
-- select count (*) from (
-- select s.tracking_id, s.gene_short_name, d.logfc, d.fdr
-- select distinct s.tracking_id, s.gene_short_name
-- from degenes as d 
-- inner join 
-- sfari_r557 as s
-- on (d.gene = s.gene_short_name)
-- where d.tool = 'edger' and d.gene_subset = 'prot_coding_genes' and d.fdr < 0.05 and
-- (d.group1 != 'lowagg_all' and d.group1 != 'lowagg_CS' and d.group1 != 'aut_mut_m' 
    -- and d.group1 != 'aut_mut_f')
-- ) as foo
-- ;

-- select s.tracking_id, s.gene_short_name, d.logfc, d.fdr
-- from degenes as d 
-- inner join 
-- sfari_r557 as s
-- on (d.gene = s.gene_short_name)
-- where d.tool = 'edger' and d.gene_subset = 'prot_coding_genes' and d.fdr < 0.1
-- and d.group1 = 'Betaintnu_F'
-- ;
-- \copy (select distinct s.tracking_id from degenes as d inner join sfari_r557 as s on (d.gene = s.gene_short_name) where d.tool = 'edger' and d.gene_subset = 'prot_coding_genes' and d.fdr < 0.05 and (d.group1 != 'lowagg_all' and d.group1 != 'lowagg_CS' and d.group1 != 'aut_mut_m' and d.group1 != 'aut_mut_f')) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/GO_analysis/degenes_ij_sfari_fdr05.txt';

-- Checking number of genes in sfari list that is in the filtered gff list.
-- select count (*) from (
-- select s.tracking_id 
-- from sfari_r557 as s
-- inner join
-- gff_genes as g
-- on (s.tracking_id = g.fbgn_id)
-- where g.gff_file = 'dmel-all-filtered-r5.57.gff'
-- ) as foo
-- ;

-- -- Getting pooled list of DE genes using sfari_r557 DE comparison.
-- select g.fbgn_id
-- from degenes as d 
-- inner join gff_genes as g on (g.name_name = d.gene) 
-- where d.tool = 'edger' and d.gene_subset = 'sfari_r557' and d.fdr < 0.1 and 
-- gff_file = 'dmel-all-filtered-r5.57.gff' and
-- (d.group1 != 'lowagg_all' and d.group1 != 'lowagg_CS' and d.group1 != 'aut_mut_m' 
    -- and d.group1 != 'aut_mut_f')

-- \copy (select g.fbgn_id from degenes as d inner join gff_genes as g on (g.name_name = d.gene) where d.tool = 'edger' and d.gene_subset = 'sfari_r557' and d.fdr < 0.1 and gff_file = 'dmel-all-filtered-r5.57.gff' and (d.group1 != 'lowagg_all' and d.group1 != 'lowagg_CS' and d.group1 != 'aut_mut_m' and d.group1 != 'aut_mut_f')) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/sfari_r557/GO_analysis/de_sfari_fbgns_fdr10.txt';


-- select gene
-- from degenes 
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 and 
-- group1 = 'NrxI_M' 
-- INTERSECT
-- select gene
-- from degenes 
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 and 
-- group1 = 'NrxIV_M'
-- INTERSECT
-- select gene
-- from degenes 
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 and 
-- group1 = 'pten_M'
-- INTERSECT
-- select gene
-- from degenes 
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 and 
-- group1 = 'CG34127_M'
-- INTERSECT
-- select gene
-- from degenes 
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 and 
-- group1 = 'Betaintnu_M'
-- INTERSECT
-- select gene
-- from degenes 
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 and 
-- group1 = 'Nhe3_M'
-- INTERSECT
-- select gene
-- from degenes 
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 and 
-- group1 = 'en_M'
-- ;


-- select count (*) from (
-- select gene
-- from degenes 
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 and 
-- group1 = 'NrxI_M' ) as foo
-- ;
-- select count (*) from (
-- select gene
-- from degenes 
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 and 
-- group1 = 'NrxIV_M' ) as foo
-- ;

-- -- Gives all the genes and group1s from degenes that have fdr < specified amount.
-- \copy ( select gene, group1 from degenes where tool = 'edger' and gene_subset = 'prot_coding_genes' and group1 != 'lowagg_CS' and group1 != 'lowagg_all' and group1 != 'aut_mut_m' and group1 != 'aut_mut_f' and fdr < 0.02 order by group1) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/GO_analysis/de_all_fdr02_group.txt' ; 

-- -- Counts the distinct genes that are DE with the given parameters for all male genotypes.
-- select count (*) from (
-- select distinct gene from degenes where tool = 'edger' and gene_subset = 'prot_coding_genes' and group1 != 'lowagg_CS' and group1 != 'lowagg_all' and group1 != 'aut_mut_m' and group1 != 'aut_mut_f' and group1 ~ '.._M' and fdr < 0.1) 
-- as foo;

-- -- Creates a view where each row is a row number, gene, and the \# of times it appears in the list of DE genes in female samples (fdr < 0.1).
-- create or replace view decountf as (
-- select row_number() OVER (ORDER BY count (*) DESC), gene, count (*) from degenes 
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 
-- and group1 ~ '.._F'
-- group by gene
-- )
-- -- -- order by count (*) DESC
-- ;
-- create or replace view decountf_brain_edger_fdr10_2str_ as (
-- select row_number() OVER (ORDER BY count (*) DESC), gene, count (*) from degenes 
-- where tool = 'edger' and gene_subset = 'brain_r557' and fdr < 0.1 
-- and group1 ~ '.._F'
-- group by gene
-- order by count (*) DESC
-- )
-- ;
-- \copy ( select row_number() OVER (ORDER BY count (*) DESC), gene, count (*) from degenes_2str where tool = 'edger' and gene_subset = 'brain_r557' and fdr < 0.1 and group1 ~ '.._M' group by gene order by count (*) DESC) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/brain_r557/GO_analysis/decountm_brain_edger_fdr10.txt';


-- select c.gene, c.count from 
-- decountm as c
-- inner join
-- degenes as g
-- using (gene)
-- where g.tool = 'edger' and g.gene_subset = 'prot_coding_genes' and g.fdr < 0.1 
-- and g.group1 = 'NrxIV_M'
-- ;


-- select i.berkid, i.sample, i.input, i.mapped, i.pmapped, i.multimapped, i.pmulti, h.sumcount as htseqcounts, h.sumcount/i.mapped as phtseqcounts
-- from autin as a 
-- inner join 
-- aligninfo as i
-- using (berkid)
-- inner join
-- basecall as b
-- using (berkid)
-- inner join
-- sumhtseqcount as h
-- using (berkid)
-- where a.use_seq = True and i.aligner = 'tophat_2str' and h.aligner='tophat_2str'
-- order by sample;
-- \copy ( select i.berkid, i.sample, i.input, i.mapped, i.pmapped, i.multimapped, i.pmulti, h.sumcount as htseqcounts, h.sumcount/i.mapped as phtseqcounts from autin as a inner join aligninfo as i using (berkid) inner join basecall as b using (berkid) inner join sumhtseqcount as h using (berkid) where a.use_seq = True and i.aligner = 'tophat_2str' and h.aligner='tophat_2str' order by sample) to '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat_2str/all_mapping_stats.txt' header csv;

-- CREATE FOREIGN TABLE basecall (
    -- seq_d date,
    -- lane int,
    -- berkid varchar(20),
    -- ref varchar(10),
    -- indexseq varchar(40),
    -- descrip varchar(40),
    -- control varchar(5),
    -- project varchar(20),
    -- yield int,
    -- per_pf real,
    -- numreads int,
    -- per_rcpl real,
    -- per_pir real,
    -- per_1mri real,
    -- per_q30 double precision,
    -- mean_qualscore double precision
-- )
-- SERVER andreaserver;

-- CREATE TABLE sumhtseqcount_2str(
    -- berkid varchar(20) UNIQUE,
    -- sample varchar(20),
    -- sumcount int,
    -- aligner varchar(50)
-- )
-- \copy sumhtseqcount_2str from '/home/andrea/Documents/lab/RNAseq/analysis/results_tophat_2str/db_htseq_all_2str_unique_summary.txt'

-- -- Get # DE genes for each genotype.
-- select group1, count (*) 
-- from degenes
-- where tool = 'deseq' and gene_subset = 'prot_coding_genes' and fdr < 0.1
-- group by group1
-- order by group1
-- ;

-- select group1, count (*) 
-- from degenes
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1
-- group by group1
-- order by group1
-- ;
-- \copy ( select group1, count (*) from degenes where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.10 group by group1 order by group1) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/GO_analysis/num_de_genes_fdr10.txt' header csv;

-- select count (*) from (
-- select d0.gene, d0.tool, 2^d0.logfc as deseq_foldchange, d0.fdr as deseq_adjpval, 
-- d1.tool, 2^d1.logfc as edger_foldchange, d1.fdr as edger_adjpval
-- from degenes as d0
-- inner join
-- degenes as d1
-- on (d0.gene = d1.gene)
-- where d0.gene_subset = 'prot_coding_genes' and d0.group1 = 'NrxI_F' and d0.group2 = 'CS_F'  and d0.fdr < 0.1 and d0.tool = 'deseq'
-- and d1.gene_subset = 'prot_coding_genes' and d1.group1 = 'NrxI_F' and d1.group2 = 'CS_F' and d1.fdr < 0.1 and d1.tool = 'edger'
-- order by deseq_adjpval
-- ) as foo
-- ;

-- select *
-- select de.group1, de.tool, dd.tool, count (de.tool), count (dd.tool)
-- , count (de.group1, de.tool), count (*)
-- from degenes as de
-- inner join
-- degenes as dd
-- using (group1)
-- where de.tool = 'edger' and de.gene_subset = 'prot_coding_genes' and de.fdr < 0.1
-- and dd.tool = 'deseq' and dd.gene_subset = 'prot_coding_genes' and dd.fdr < 0.1
-- -- group by de.group1, de.tool, dd.tool
-- order by de.group1
-- ;

-- -- Get # DE genes inner join sfari for each genotype
-- select group1, count (*) 
-- from degenes
-- inner join
-- sfari_r557
-- on (gene_short_name = gene)
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1
-- group by group1
-- order by group1
-- ;
-- \copy ( select group1, count (*) from degenes inner join sfari_r557 on (gene_short_name = gene) where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.05 group by group1 order by group1) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/GO_analysis/num_degenesijsfari_fdr05.txt'

-- -- VIEW SHOWING # OF TIMES EACH GENE IS IN A DE LIST WHERE GROUP1 IS ONE OF THE FEMALE GENOTYPES
-- create or replace view decountf as (
-- select row_number() OVER (ORDER BY count (*) DESC), gene, count (*) from degenes 
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 
-- and group1 ~ '.._F'
-- group by gene;

-- -- FOR A GENE LIST, SEE HOW MANY TIMES IT IS IN A DE LIST

-- drop function testfn(text,real);
-- create function testfn(detable text, selfdr real) returns table (gene varchar(100), logfc double precision)
-- as 
-- $BODY$
-- BEGIN
-- RETURN QUERY EXECUTE format('
    -- select gene, logfc from %s where fdr < %L
    -- '
    -- ,detable
    -- ,selfdr);
-- END
-- $BODY$
-- LANGUAGE plpgsql;

-- select * from testfn('degenes', 0.10);

-- DROP FUNCTION find_decount(text,text,text,text,real,text);
-- CREATE FUNCTION find_decount(selgroup1 text, decounttable text, degenetable text, tool text, gene_subset text, selfdr real, gff_file text) RETURNS TABLE (fbgn_id varchar(20), gene varchar(100), count bigint, logfc double precision, fdr double precision, group1 varchar(50))
-- AS
        -- $BODY$
        -- BEGIN
        -- RETURN QUERY 
        -- EXECUTE format('
        -- select g.fbgn_id, dc.gene, dc.count, d.logfc, d.fdr, d.group1 
        -- from %s as dc
        -- inner join
        -- %s as d
        -- using (gene)
        -- inner join
        -- gff_genes as g
        -- on (d.gene = g.name_name)
        -- where d.tool = %L and d.gene_subset = %L and d.fdr < %s and d.group1 = %L and gff_file = %L'
        -- ,decounttable
        -- ,degenetable
        -- ,tool
        -- ,gene_subset
        -- ,selfdr
        -- ,selgroup1
        -- ,gff_file);

        -- END
        -- $BODY$
        -- LANGUAGE plpgsql;

-- select fbgn_id, gene, count, logfc, fdr, group1
-- from decountf as dcf
-- inner join
-- degenes as d
-- using (gene)
-- inner join
-- gff_genes as g
-- on (d.gene = g.name_name)
-- where tool = 'edger' and gene_subset = 'prot_coding_genes' and fdr < 0.1 
-- and group1 = 'Betaintnu_F' and gff_file = 'dmel-all-filtered-r5.57.gff'

-- ;

-- -- GET FBGNS of DECOUNTF -- --
-- select *
-- from decountf
-- inner join
-- gff_genes
-- on (gene = name_name)
-- where gff_file = 'dmel-all-filtered-r5.57.gff'
-- order by count DESC
-- ;
-- \copy (  select * from decountf inner join gff_genes on (gene = name_name) where gff_file = 'dmel-all-filtered-r5.57.gff' order by count DESC ) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/GO_analysis/decountf_fdr10_fbgns.txt' header csv;
-- \copy (  select * from decountm_prot_coding_genes_edger_fdr10_2str inner join gff_genes on (gene = name_name) where gff_file = 'dmel-all-filtered-r5.57.gff' order by count DESC ) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str_good/prot_coding_genes/GO_analysis/decountm_fdr10_fbgns.txt' header csv;

-- select g.fbgn_id, f.gene as gene_F, f.count as count_F, f.row_number as row_F,
        -- m.gene as gene_M, m.count as count_M, m.row_number as row_M, 
        -- coalesce(f.count, 0) + coalesce(m.count,0) as sum_counts
-- from 
-- decountf_prot_coding_genes_edger_fdr10_2str as f
-- full outer join
-- decountm_prot_coding_genes_edger_fdr10_2str as m
-- on (f.gene = m.gene)
-- inner join
-- gff_genes as g
-- on (f.gene = g.name_name or m.gene = g.name_name)
-- where g.gff_file = 'dmel-all-filtered-r5.57.gff'
-- order by sum_counts DESC, f.count DESC, m.count DESC
-- ;

-- \copy ( select g.fbgn_id, f.gene as gene_F, f.count as count_F, f.row_number as row_F, m.gene as gene_M, m.count as count_M, m.row_number as row_M, coalesce(f.count, 0) + coalesce(m.count,0) as sum_counts from decountf_prot_coding_genes_edger_fdr10_2str as f full outer join decountm_prot_coding_genes_edger_fdr10_2str as m on (f.gene = m.gene) inner join gff_genes as g on (f.gene = g.name_name or m.gene = g.name_name) where g.gff_file = 'dmel-all-filtered-r5.57.gff' order by sum_counts DESC, f.count DESC, m.count DESC) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str_good/prot_coding_genes/GO_analysis/decount/decountf+m_fdr10_fbgns.txt' header csv ;

-- -- Returns a list of DE genes, along with the number of samples and which samples they are considered DE.
-- select gene, g.fbgn_id, 
-- avg(coalesce(df.count,0)) as avg_f, avg(coalesce(dm.count, 0)) as avg_m, 
-- avg(coalesce(df.count, 0) + coalesce(dm.count, 0)) as avg_mf, 
-- 2^avg(d.logfc) as avg_fc,
-- 2^avg(d.fdr) as avg_adjpval,
-- array_agg(group1)
-- from decountf as df
-- full outer join
-- decountm as dm
-- using (gene)
-- inner join
-- degenes_r6_2str as d
-- using (gene)
-- inner join 
-- gff_genes as g
-- on (gene = g.name_name)
-- where d.fdr < 0.10 and d.tool = 'edger'
-- and g.gff_file = 'dmel-all-r6.01.gff'
-- and d.gene_subset = 'pcg_r601'
-- group by gene, g.fbgn_id
-- order by avg_mf DESC
-- ;

-- \copy ( select gene, g.fbgn_id, avg(coalesce(df.count, 0) + coalesce(dm.count, 0)) as num_samples, 2^avg(logfc) as avg_fc, 2^avg(logcpm) as avg_cpm, array_agg(group1) from decountf_prot_coding_genes_edger_fdr10_2str as df full outer join decountm_prot_coding_genes_edger_fdr10_2str as dm using (gene) inner join degenes_2str as d using (gene) inner join gff_genes as g on (gene = g.name_name) where d.group1 != 'lowagg_CS' and d.group1 != 'aut_mut_m' and d.group1 != 'aut_mut_f' and d.group1 != 'lowagg_all' and d.fdr < 0.10 and (d.group2 = 'CS_M' or d.group2 = 'CS_F') and d.tool = 'edger' and d.gene_subset = 'prot_coding_genes' and g.gff_file = 'dmel-all-filtered-r5.57.gff' group by gene, g.fbgn_id order by num_samples DESC) to '/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str_good/prot_coding_genes/GO_analysis/decount/decountf+m_fdr10_groups.txt' csv header;

-- -- Get info from autin sorted and grouped by different fields

-- select genotype, sex, sample, rnaconc, qbitngul, use_seq from autin order by qbitngul;


-- -- Gene lists for GOseq.
-- \copy (select gene_short_name from pcg_r601 order by gene_short_name) to '/home/andrea/rnaseqanalyze/references/gene_lists/goseq_lists/pcg_r601_genes.txt';
-- \copy (select gene_short_name from sfari_r601 order by gene_short_name) to '/home/andrea/rnaseqanalyze/references/gene_lists/goseq_lists/sfari_r601_genes.txt';
-- \copy (select gene_short_name from bwa_r601 order by gene_short_name) to '/home/andrea/rnaseqanalyze/references/gene_lists/goseq_lists/bwa_r601_genes.txt';
-- \copy (select tracking_id from pcg_r601 order by tracking_id) to '/home/andrea/rnaseqanalyze/references/gene_lists/goseq_lists/pcg_r601_fbgns.txt';
-- \copy (select tracking_id from sfari_r601 order by tracking_id) to '/home/andrea/rnaseqanalyze/references/gene_lists/goseq_lists/sfari_r601_fbgns.txt';
-- \copy (select tracking_id from bwa_r601 order by tracking_id) to '/home/andrea/rnaseqanalyze/references/gene_lists/goseq_lists/bwa_r601_fbgns.txt';

-- -- Gene lists with current gene models:
-- \copy (select gene_short_name from pcg_r601 inner join gff_genes on (name_name = gene_short_name) where gff_file = 'dmel-all-r6.01.gff' order by gene_short_name) to '/home/andrea/rnaseqanalyze/references/gene_lists/goseq_lists/pcg_r601_genes.txt';
-- \copy (select gene_short_name from sfari_r601 inner join gff_genes on (name_name = gene_short_name) where gff_file = 'dmel-all-r6.01.gff' order by gene_short_name) to '/home/andrea/rnaseqanalyze/references/gene_lists/goseq_lists/sfari_r601_genes.txt';
-- \copy (select gene_short_name from bwa_r601 inner join gff_genes on (name_name = gene_short_name) where gff_file = 'dmel-all-r6.01.gff' order by gene_short_name) to '/home/andrea/rnaseqanalyze/references/gene_lists/goseq_lists/bwa_r601_genes.txt';

-- -- Figuring out the overlap between protein coding genes, gff_genes, and htseq results.
-- select count (*) 
-- from htseq_r6_2str 
-- inner join
-- gff_genes
-- on (gene_short_name = name_name)
-- where gff_file = 'dmel-all-r6.01.gff'
-- and berkid = 'RGAM014A'
-- ;

-- select count (*) 
-- from pcg_r601
-- inner join
-- gff_genes
-- on (tracking_id = fbgn_id)
-- where gff_file = 'dmel-all-r6.01.gff'
-- ;

-- select count (*)
-- from pcg_r601
-- inner join
-- htseq_r6_2str
-- using (gene_short_name)
-- where berkid = 'RGAM014A'
-- ;

-- OK, pcg_r601 has genes that are not in the gff file. Looks like extra genes
-- are the non current ones (from field gene model status). I'm just going to
-- recopy the gene list to avoid future confusion.
-- select gene_short_name
-- from pcg_r601
-- EXCEPT
-- select name_name 
-- from gff_genes
-- where gff_file = 'dmel-all-r6.01.gff'
-- ;



-- -- Get homologs of decount genes
-- select count (*) from (
-- select count (*) from (
-- select distinct gene
-- select d.gene, h.fly_sym
-- select gene, f.gene, m.gene, i.fbgn_id, hp.pfbgn, h.fly_sym, h.human_sym
-- select gene, array_agg(human_sym)
-- from decountf as f
-- full outer join
-- decountm as m
-- using (gene)
-- inner join
-- r601_id_index as i
-- on (gene = i.name_name)
-- inner join
-- homolog_pfbgns as hp
-- using (pfbgn)
-- inner join
-- homologs as h
-- using (fly_sym)
-- where h.gene_source = 'sfari' and hp.gene_source = 'sfari'
-- group by gene
-- order by gene

-- select gene, array_agg(human_sym) "
-- "from {} as d "
-- "full outer join "
-- "{} as m "
-- "using (gene) "
-- "left outer join homologs as h "
-- "on (gene = fly_sym) "
-- "where gene_source = '{}' group by gene order by gene) "

-- left outer join
-- homologs as h
-- on (gene = fly_sym)
-- where gene_source = 'sfari'
-- -- group by gene
-- order by gene
-- -- ) as foo
-- ;


-- -- create view of sfari go categories
-- create or replace view sfari_gocat as (
-- select gc.go_id, gc.go_cat, go_nspace, gs.fdr_over_pval, gs.fdr_under_pval,
-- gs.num_de, gs.num_total, gs.tool, gs.gene_subset, gs.defdr, gs.group1,
-- gs.group2 
-- from r601_go_cat as gc 
-- inner join 
-- goseq_r6_2str as gs 
-- using (go_id)
-- where tool = 'none' and gene_subset = 'all_sfari' and defdr = 0 and group1 =
-- 'none' and group2 = 'none' and num_de > 0
-- order by gs.fdr_over_pval )
-- ;

-- -- Find the inner join between GO categories of DE genes and sfari genes.
-- select g.go_id, s.go_cat, g.num_de, g.fdr_over_pval as g_overpval, 
-- s.fdr_over_pval as s_overpval, g.defdr, h.human_sym
-- -- array_agg(human_sym)
-- from goseq_r6_2str as g
-- inner join
-- sfari_gocat as s
-- using (go_id)
-- inner join
-- sfari_go_hom as h
-- using(go_id)
-- where g.group1 = 'Betaintnu_F'
-- and g.tool = 'edger' and g.defdr = 0.05
-- and g.gene_subset = 'pcg_r601'
-- and g.num_de > 0
-- -- group by g.go_id, s.go_cat, g.num_de, g.fdr_over_pval, s.fdr_over_pval, g.defdr
-- order by g.fdr_over_pval
-- ;

-- -- Find the genes in the sfari list, their human homologs, and the relevant
-- -- GO categories with the given GO id.
-- create view sfari_go_hom as (
-- select s.gene_short_name, g.go_id, g.go_cat, h.human_sym from
-- -- select * from
-- sfari_r601 as s
-- inner join
-- r601_gene_go as g
-- on (gene_short_name = gene_name)
-- inner join
-- r601_id_index as i
-- on (gene_short_name = i.name_name)
-- inner join
-- homolog_pfbgns as hp
-- using (pfbgn)
-- inner join
-- homologs as h
-- using (fly_sym)
-- where h.gene_source = 'sfari' and hp.gene_source = 'sfari' 
-- ) 
-- ;
-- and g.go_id = 'GO:0006412'
-- ;

-- -- Find the overlap of GO categories in DE genes.
-- select go_id, go_cat, array_agg(group1)
-- select *
-- select r.go_id, r.go_cat, array_agg(g.fdr_over_pval) as fdr_over_pval, array_agg(num_de) as num_de, array_agg(num_total) as num_total, count(g.group1), array_agg(g.group1)
-- from goseq_r6_2str as g
-- inner join
-- r601_go_cat as r
-- using (go_id)
-- where tool = 'edger' and gene_subset = 'sfari_r601'
-- and defdr = 0.10
-- and num_de > 0
-- and fdr_over_pval < 0.25
-- -- and go_id = 'GO:0007052'
-- group by r.go_id, r.go_cat
-- order by fdr_over_pval
-- ;

-- create or replace view decountm_test as (
-- select row_number() OVER (ORDER BY count (*) DESC),
-- gene, count (*), array_agg(group1)
-- from degenes_r6_2str
-- where tool = 'edger' and gene_subset = 'pcg_r601'
-- and fdr < 0.05
-- and group1 ~ '.._M'
-- -- and group1 != 'pten_F' and group1 != 'Betaintnu_F'
-- group by gene 
-- order by count (*) DESC)
-- ;

-- select gene, count, array_agg, array_agg(go_cat) from
-- decountf_test
-- inner join
-- r601_gene_go
-- on (gene_name = gene)
-- group by gene, count, array_agg
-- order by count DESC, gene
