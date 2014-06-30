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
    -- qbitd date
-- )
-- SERVER andreaserver;

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
    -- FPKM_status character varying(5),
    -- berkid character varying(20));

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

-- CREATE TABLE prot_coding_genes (
    -- tracking_id character varying(20),
    -- gene_long_name character varying(100),
    -- gene_short_name character varying(100)
-- );

-- Copy into table.
-- \copy prot_coding_genes from '/home/andrea/rnaseqanalyze/references/protein_coding_genes/flybase_results_protein_coding_genes_dmel_symbol.txt';

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
-- CREATE TABLE htseq (
    -- gene_name varchar(100),
    -- counts int,
    -- berkid varchar(20)
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

-- \copy (select t0.berkid, t0.sample, t1.input as total_sequenced_reads, t0.mapped as clc_mapped, t1.mapped as th_mapped, t1.mapped-t0.mapped as diff_thmap_clcmap, t0.pmapped as clc_percent_mapped, t1.pmapped as th_percent_mapped, t0.mapped-t0.multimapped as clc_unique, (t0.mapped-t0.multimapped)/t1.input::float as clc_ratio_totalseq_unique, t1.mapped-t1.multimapped as th_unique, (t1.mapped-t1.multimapped)/t1.input::float as th_ratio_totalseq_unique from aligninfo as t0 inner join aligninfo as t1 using (berkid) where t0.aligner = 'clc' and t1.aligner = 'tophat' order by sample) to 'clc_tophat_mapping.csv' csv header;


-- Creates a table for the DE gene data.
-- DROP TABLE degenes;
-- CREATE TABLE degenes (
    -- gene varchar(100),
    -- logfc double precision,
    -- logcpm double precision,
    -- pvalue double precision, 
    -- fdr double precision,
    -- tool varchar(40),
    -- group1 varchar(50),
    -- group2 varchar(50),
    -- UNIQUE (gene, group1, group2)
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


-- Creates a table to hold the list of genes from the specified gff file.
-- DROP TABLE gff_genes;
-- CREATE TABLE gff_genes (
    -- fbgn_ID varchar (20),
    -- name_Name varchar (100),
    -- annid varchar (100),
    -- gff_file varchar (50),
    -- unique (fbgn_ID, name_Name, annid, gff_file)
-- );

-- \copy gff_genes from '/home/andrea/rnaseqanalyze/references/dmel-r5.50_r5.57_lists/fbgn_name_annID_r5.50';
-- \copy gff_genes from '/home/andrea/rnaseqanalyze/references/dmel-r5.50_r5.57_lists/fbgn_name_annID_r5.57';


-- QUERY TO LOOK FOR GENES THAT ARE THE SAME IN THE R5.57 AND R5.5 FILES;
-- HOWEVER, PRIMARY FBGNS AND NAMES CHANGED BETWEEN THE TWO RELEASES
-- select count (*) from (
-- -- select fbgn_ID, name_Name from gff_genes where gff_file = 'dmel-all-filtered-r5.57.gff'
-- select fbgn_ID, name_Name from gff_genes where gff_file = 'dmel-all-r5.50.gff'
-- -- )as foo;
-- EXCEPT 
-- -- select count (*) from (
-- select t0.fbgn_ID, t0.name_Name 
-- select *
-- select t0.fbgn_ID
-- from gff_genes as t0
-- inner join
-- gff_genes as t1
-- -- using (fbgn_ID)
-- using (name_Name)
-- where t0.gff_file = 'dmel-all-filtered-r5.57.gff' AND t1.gff_file = 'dmel-all-r5.50.gff' AND 
-- -- t0.name_Name != t1.name_Name
-- t0.fbgn_ID != t1.fbgn_ID
-- -- order by fbgn_ID
-- order by name_Name
-- ) as foo
-- ;

-- select count (*) from (
-- select distinct fbgn_ID from gff_genes where gff_file = 'dmel-all-r5.50.gff'
-- ) as foo
-- ;


-- TABLE CONTAINING INFO ABOUT FBGN AND ANNOTATION IDS. COPIES INFO FROM THE 
-- FILE OUTPUT BY FBGNCONVERT.PY

-- DROP TABLE fbgn_annot_ID;
-- CREATE TABLE fbgn_annot_ID (
    -- genesymbol varchar (100),
    -- fbgn_primary varchar (20),
    -- fbgn_secondary text[],
    -- annotid_primary varchar (20),
    -- annotid_secondary text[], 
    -- unique (genesymbol, fbgn_primary, annotid_primary)
-- );

-- \copy fbgn_annot_ID from '/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/misc/fbgn_annotation_ID_fb_2014_03_fordb_braces.tsv';


-- Creates a table gfftest which has the first 5 rows of the gff_genes table;
-- used for testing joins, etc. with the fbgn_annot_ID table.
-- DROP TABLE gfftest
-- CREATE TABLE gfftest (
    -- fbgn_id varchar (20),
    -- name_name varchar (100),
    -- gff_file varchar (50)
    -- )
-- INSERT into gfftest VALUES
    -- ('FBgn0031208', 'CG11023', 'dmel-all-r5.50.gff'),
    -- ('FBgn0002121', 'l(2)gl', 'dmel-all-r5.50.gff'),
    -- ('FBgn0031209', 'Ir21a', 'dmel-all-r5.50.gff'),
    -- ('FBgn0263584', 'CR43609', 'dmel-all-r5.50.gff'),
    -- ('FBgn0051973', 'Cda5', 'dmel-all-r5.50.gff')
    -- ;


--- Lists the FBgns for entries that are in the gff_genes file but not in
--- the 'fbgn_primary' field of the Flybase_annotation_ID file.
-- select fbgn_id from gff_genes where gff_file = 'dmel-all-filtered-r5.57.gff'
-- EXCEPT
-- select t0.fbgn_id
    -- from 
    -- gff_genes as t0
    -- inner join
    -- fbgn_annot_ID as t1
    -- on t0.fbgn_ID = t1.fbgn_primary
    -- where t0.gff_file = 'dmel-all-filtered-r5.57.gff'
    -- -- order by t1.fbgn_primary
-- ;

---- Lists the FBgns and Names for entries that are in the gff_genes file but not in
---- the Flybase_annotation_ID file 
-- select count (*) from (
-- all genes in the gff file
-- select fbgn_ID, name_Name, annid
    -- from 
    -- gff_genes 
    -- where gff_file = 'dmel-all-r5.50.gff'
-- EXCEPT
-- -- subtract genes that are in the fbgn_annot table that have matching primary 
-- -- FBGNs.
-- select t0.fbgn_ID, t0.name_Name, t0.annid
    -- from 
    -- gff_genes as t0
    -- inner join
    -- fbgn_annot_ID as t1
    -- on t0.fbgn_ID = t1.fbgn_primary
    -- where t0.gff_file = 'dmel-all-r5.50.gff'
    -- -- order by t1.fbgn_primary
-- -- ) as foo
-- EXCEPT
-- -- subtract genes that are in the fbgn_annot table whose FBGNs are in the
-- -- secondary FBGN list
-- select t0.fbgn_ID, t0.name_Name, t0.annid
    -- from 
    -- gff_genes as t0
    -- inner join
    -- fbgn_annot_ID as t1
    -- -- on t0.fbgn_ID = t1.fbgn_primary
    -- on t0.fbgn_ID = ANY (t1.fbgn_secondary)
    -- where t0.gff_file = 'dmel-all-r5.50.gff'
-- EXCEPT
-- -- subtract genes that are in the fbgn_annot table where the primary 
-- -- annotation ID match
-- select t0.fbgn_ID, t0.name_Name, t0.annid
    -- from 
    -- gff_genes as t0
    -- inner join
    -- fbgn_annot_ID as t1
    -- on t0.annid = t1.annotid_primary
    -- where t0.gff_file = 'dmel-all-r5.50.gff'
-- EXCEPT
-- -- subtract genes that are in the fbgn_annot table where the annotation ID 
-- -- matches a secondary annotation
-- select t0.fbgn_ID, t0.name_Name, t0.annid
    -- from 
    -- gff_genes as t0
    -- inner join
    -- fbgn_annot_ID as t1
    -- -- on t0.fbgn_ID = t1.fbgn_primary
    -- on t0.annid = ANY (t1.annotid_secondary)
    -- where t0.gff_file = 'dmel-all-r5.50.gff'
    -- ;

-- Copies the result of the above query into a file.

-- (DOES NOT INCLUDE THE ANNOTATION QUERYING)
-- \copy ( select fbgn_ID, name_Name from gff_genes where gff_file = 'dmel-all-r5.50.gff' EXCEPT select t0.fbgn_ID, t0.name_Name from gff_genes as t0 inner join fbgn_annot_ID as t1 on t0.fbgn_ID = t1.fbgn_primary where t0.gff_file = 'dmel-all-r5.50.gff' EXCEPT select t0.fbgn_ID, t0.name_Name from gff_genes as t0 inner join fbgn_annot_ID as t1 on t0.fbgn_ID = ANY (t1.fbgn_secondary) where t0.gff_file = 'dmel-all-r5.50.gff') to '/home/andrea/rnaseqanalyze/references/fbgn_annot_ID/r5.50_ingff_notfbgn_annot_ID_fbgn_name.txt'
-- \copy ( select fbgn_ID, name_Name from gff_genes where gff_file = 'dmel-all-filtered-r5.57.gff' EXCEPT select t0.fbgn_ID, t0.name_Name from gff_genes as t0 inner join fbgn_annot_ID as t1 on t0.fbgn_ID = t1.fbgn_primary where t0.gff_file = 'dmel-all-filtered-r5.57.gff' EXCEPT select t0.fbgn_ID, t0.name_Name from gff_genes as t0 inner join fbgn_annot_ID as t1 on t0.fbgn_ID = ANY (t1.fbgn_secondary) where t0.gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/rnaseqanalyze/references/fbgn_annot_ID/r5.57_ingff_notfbgn_annot_ID_fbgn_name.txt'

-- Creates a table with info about homologs of genes in various databases.
-- DROP TABLE homologs;
-- CREATE TABLE homologs (
    -- searchterm varchar (50),
    -- humangeneid int,
    -- hgncid varchar (20),
    -- human_sym varchar (100),
    -- flygeneid int,
    -- fbgn varchar (20),
    -- fly_sym varchar (100),
    -- diopt_score int,
    -- weighted_score real,
    -- prediction_db text[],
    -- gene_source varchar (20),
    -- unique (searchterm, human_sym, fbgn, fly_sym, gene_source)
-- );

-- \copy homologs from '/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/sfari/autism_sfari_list_diopt_filtered.txt'
-- \copy homologs from '/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/autkb/all_entrezid_unique_diopt_filtered.txt'
-- \copy homologs from '/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/williams/williams_njem_diopt_filtered.txt'


-- Check if the homologs of the genes in the SFARI database are in the CLC 
-- r5.50 gff files.

    
-- -- genes in gff that are in the fbgn_annot table that have matching primary 
-- -- FBGNs.
-- select count (*) from (
-- select t1.fbgn_primary, t0.fbgn_ID, t0.name_Name, t0.annid
    -- from 
    -- gff_genes as t0
    -- inner join
    -- fbgn_annot_ID as t1
    -- on t0.fbgn_ID = t1.fbgn_primary
    -- where t0.gff_file = 'dmel-all-r5.50.gff'
    -- -- order by t1.fbgn_primary
-- -- ) as foo;
-- UNION
-- -- -- genes in gff that are in the fbgn_annot table whose FBGNs are in the
-- -- -- secondary FBGN list
-- -- select count (*) from (
-- select t1.fbgn_primary, t0.fbgn_ID, t0.name_Name, t0.annid
    -- from 
    -- gff_genes as t0
    -- inner join
    -- fbgn_annot_ID as t1
    -- on t0.fbgn_ID = ANY (t1.fbgn_secondary)
    -- where t0.gff_file = 'dmel-all-r5.50.gff'
-- -- ) as foo;
-- UNION 
-- -- -- genes in gff that are in the fbgn_annot table where the primary 
-- -- -- annotation ID match
-- -- select count (*) from (
-- select t1.fbgn_primary, t0.fbgn_ID, t0.name_Name, t0.annid
    -- from 
    -- gff_genes as t0
    -- inner join
    -- fbgn_annot_ID as t1
    -- on t0.annid = t1.annotid_primary
    -- where t0.gff_file = 'dmel-all-r5.50.gff'
-- -- ) as foo;
-- UNION
-- -- -- genes in gff that are in the fbgn_annot table where the annotation ID 
-- -- -- matches a secondary annotation
-- -- select count (*) from (
-- select t1.fbgn_primary, t0.fbgn_ID, t0.name_Name, t0.annid
    -- from 
    -- gff_genes as t0
    -- inner join
    -- fbgn_annot_ID as t1
    -- -- on t0.fbgn_ID = t1.fbgn_primary
    -- on t0.annid = ANY (t1.annotid_secondary)
    -- where t0.gff_file = 'dmel-all-r5.50.gff'
-- ) as foo;

 -- count 
-- -------
 -- 15880
-- (1 row)

 -- count 
-- -------
   -- 151
-- (1 row)

 -- count 
-- -------
 -- 15893
-- (1 row)

 -- count 
-- -------
   -- 450
-- (1 row)

-- select count (*) from (
-- select fbgn, fly_sym
-- from homologs where gene_source = 'sfari'
-- EXCEPT
-- select fbgn, fly_sym
-- from homologs
-- where gene_source = 'autkb'
-- order by fly_sym
-- ) as foo
;

-- select count (*) from (
    -- select distinct t0.fbgn, t0.fly_sym 
    -- from homologs as t0
    -- inner join
    -- homologs as t1
    -- using (fbgn)
    -- where t0.gene_source = 'sfari' and t1.gene_source = 'autkb'
-- ) as foo
    -- ;


-- TABLE CONTAINING INFO ABOUT FBGN. Second column has all 
-- the primary and secondary fbgns and the first column has the primary fbgns.
-- COPIES INFO FROM THE FILE OUTPUT BY FBGNCONVERT.PY
-- DROP TABLE all_fbgns;
-- CREATE TABLE all_fbgns (
    -- pfbgn varchar (20),
    -- psfbgn varchar (20),
    -- gene_sym varchar (100),
    -- unique (pfbgn, psfbgn)
-- );
-- \copy all_fbgns from '/home/andrea/rnaseqanalyze/references/fbgn_annot_ID/fbgn_annotation_ID_fb_2014_03_fordb_2fbgn.tsv' ;


-- As above, but with annotation IDs.
-- DROP TABLE all_annids;
-- CREATE TABLE all_annids (
    -- pannid varchar (50),
    -- psannid varchar (50),
    -- gene_sym varchar (100),
    -- unique (pannid, psannid)
-- );
-- \copy all_annids from '/home/andrea/rnaseqanalyze/references/fbgn_annot_ID/fbgn_annotation_ID_fb_2014_03_fordb_2annid.tsv' ;

-- Determining if all the genes in the gff_file is in all_fbgns. All but
-- 19 genes show up, as before, but searching through the all_fbgns table
-- is much faster.

-- select count (*) from gff_genes where gff_file = 'dmel-all-r5.50.gff';
-- select count (*) from (
-- select pfbgn
-- from all_fbgns
-- inner join
-- gff_genes
-- on (psfbgn = fbgn_id)
-- where gff_file = 'dmel-all-r5.50.gff'
-- ) as foo
-- ;

-- As above, but also searching with gene symbols. Not as specific.
-- select fbgn_id, name_name from gff_genes where gff_file = 'dmel-all-r5.50.gff'
-- except
-- select fbgn_id, name_name
    -- from gff_genes
    -- inner join
    -- all_fbgns
    -- on (gene_sym = name_name)
    -- where gff_file = 'dmel-all-r5.50.gff'
-- except
-- select fbgn_id, name_name
    -- from gff_genes
    -- inner join
    -- all_fbgns
    -- on (fbgn_id = psfbgn)
    -- where gff_file = 'dmel-all-r5.50.gff'

-- Determining if all gene homologs of sfari and autkb genes are in the 
-- all_annids table
-- select count (*) from homologs where gene_source = 'autkb';
-- -- select fly_sym from homologs where gene_source = 'autkb'
-- -- except
-- select count (*) from (
-- select fbgn 
    -- from homologs
    -- inner join
    -- all_annids
    -- on (fly_sym = psannid)
    -- where gene_source = 'autkb'
-- ) as foo
-- ;


-- Lists the gff_genes from the indicated gff_file that are duplicates.
-- select count (*) from (
-- select all fbgn_id, name_name
    -- from gff_genes
    -- inner join
    -- all_fbgns
    -- on (psfbgn = fbgn_id)
    -- where gff_file = 'dmel-all-r5.50.gff'
    -- -- order by fbgn_id
-- -- ) as foo
-- except all
-- select distinct fbgn_id, name_name
    -- from gff_genes
    -- inner join
    -- all_fbgns
    -- on (psfbgn = fbgn_id)
    -- where gff_file = 'dmel-all-r5.50.gff'
    -- order by fbgn_id
-- ) as foo
-- ;

-- Lists the pfbgn from the gff_genes from the indicated gff_file that are duplicates.
-- select pfbgn, gene_sym
    -- from gff_genes
    -- inner join
    -- all_fbgns
    -- on (psfbgn = fbgn_id)
    -- where gff_file = 'dmel-all-r5.50.gff'
-- except all
-- -- select count (*) from (
-- select distinct pfbgn, gene_sym
    -- from gff_genes
    -- inner join
    -- all_fbgns
    -- on (psfbgn = fbgn_id)
    -- where gff_file = 'dmel-all-r5.50.gff'
    -- order by pfbgn
-- -- ) as foo
-- ;

-- Determining if all gene homologs in the autkb/sfari database are in the gff files.
-- Selects the distinct primary fbgns of the autkb homologs.
-- select count (*) from (
-- select distinct pfbgn, gene_sym
    -- from homologs
    -- inner join
    -- all_fbgns
    -- on (fbgn = psfbgn)
    -- where gene_source = 'sfari' 
-- -- -- ) as foo
-- -- -- ;
-- -- except 
-- intersect
-- -- -- selects the distinct primary fbns of the gff genes
-- select count (*) from (
-- select distinct pfbgn 
    -- from gff_genes
    -- inner join
    -- all_fbgns
    -- on (psfbgn = fbgn_id)
    -- where gff_file = 'dmel-all-r5.50.gff'
-- ) as foo
-- -- ;


--- Copies the 43 genes that are in the autkb homologs list but not in the 
--- filtered 5.57 gff file into the file shown.
-- \copy (select distinct pfbgn, gene_sym from homologs inner join all_fbgns on (fbgn = psfbgn) where gene_source = 'autkb'  except select distinct pfbgn, gene_sym from gff_genes inner join all_fbgns on (psfbgn = fbgn_id) where gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/autkb/autkb_homologs_not_in_r5.57_gff' header csv;

---- Copies the 11 genes that are in the sfari homologs list but not the 
---- filtered 5.57 gff file into the file shown.
-- \copy (select distinct pfbgn, gene_sym from homologs inner join all_fbgns on (fbgn = psfbgn) where gene_source = 'sfari'  except select distinct pfbgn, gene_sym from gff_genes inner join all_fbgns on (psfbgn = fbgn_id) where gff_file = 'dmel-all-filtered-r5.57.gff') to '/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/sfari/sfari_homologs_not_in_r5.57_filtered_gff' header csv;


------------------- GETTING LISTS OF SFARI HOMOLOGS --------------------
-- Create a view of the primary fbgns of the sfari homologs.
-- create or replace view sfari_pfbgns as (
-- select distinct pfbgn, gene_sym
    -- from homologs
    -- inner join
    -- all_fbgns
    -- on (fbgn = psfbgn)
    -- where gene_source = 'sfari' 
-- );

---- All sfari_pbgns have only one matching primary or secondary fbgn in the
---- all_fbgns table.
-- select count (*) from (
-- select t1.psfbgn, t1.gene_sym 
-- from sfari_pfbgns as t0
-- inner join
-- all_fbgns as t1
-- on (t0.pfbgn = t1.psfbgn)
-- ) as foo
-- ;

-- -- Create view: fbgn_ID of gff file and primary_ID from fbgn_annot_id file.
-- create or replace view r550_id_index as (
    -- select gff.fbgn_id, allf.pfbgn from
    -- gff_genes as gff
    -- inner join
    -- all_fbgns as allf
    -- on (fbgn_id = psfbgn)
    -- where gff.gff_file = 'dmel-all-r5.50.gff')

-- Gets the r550 fbgn_ids of the sfari homologs
-- select count (*) from (
    -- select r550.fbgn_id
    -- from sfari_pfbgns as sf
    -- inner join
    -- r550_id_index as r550
    -- on (sf.pfbgn = r550.pfbgn)
    -- order by sf.pfbgn
-- ) as foo
-- ;

-- Returns a list of duplicated fbgns in the inner join of the sfari homolog 
-- pfbgns and the r550 pfbgns.
    -- select sf.pfbgn, sf.gene_sym
    -- from sfari_pfbgns as sf
    -- inner join
    -- r550_id_index as r550
    -- on (sf.pfbgn = r550.pfbgn)
    -- except all 
    -- select distinct sf.pfbgn, sf.gene_sym
    -- from sfari_pfbgns as sf
    -- inner join
    -- r550_id_index as r550
    -- on (sf.pfbgn = r550.pfbgn)
    -- ;

-- Gets the r550 name_names of the sfari homologs:
-- select count (*) from (
-- select name_name
-- from (
    -- select r550.fbgn_id
    -- from sfari_pfbgns as sf
    -- inner join
    -- r550_id_index as r550
    -- on (sf.pfbgn = r550.pfbgn)
-- ) as sf_fbgn_ids
-- inner join
-- gff_genes as gff
-- on (sf_fbgn_ids.fbgn_id = gff.fbgn_id)
-- where gff.gff_file = 'dmel-all-r5.50.gff'
-- ) as foo
-- ;

-- -- -- Create view: fbgn_ID of gff file and primary_ID from fbgn_annot_id file.
-- create or replace view r557_id_index as (
    -- select gff.fbgn_id, allf.pfbgn from
    -- gff_genes as gff
    -- inner join
    -- all_fbgns as allf
    -- on (fbgn_id = psfbgn)
    -- where gff.gff_file = 'dmel-all-filtered-r5.57.gff')
-- ;

-- -- -- Gets the r557 fbgn_ids of the sfari homologs
-- select count (*) from (
    -- select r.fbgn_id
    -- from sfari_pfbgns as sf
    -- inner join
    -- r557_id_index as r 
    -- on (sf.pfbgn = r.pfbgn)
    -- order by sf.pfbgn
-- ) as foo
-- ;

-- Returns a list of duplicated fbgns in the inner join of the sfari homolog 
-- pfbgns and the r557 pfbgns.
    -- select sf.pfbgn, sf.gene_sym
    -- from sfari_pfbgns as sf
    -- inner join
    -- r557_id_index as r
    -- on (sf.pfbgn = r.pfbgn)
    -- except all 
    -- select distinct sf.pfbgn, sf.gene_sym
    -- from sfari_pfbgns as sf
    -- inner join
    -- r557_id_index as r
    -- on (sf.pfbgn = r.pfbgn)
    -- ;

-- -- Gets the r557 name_names of the sfari homologs:
-- select count (*) from (
-- select name_name
-- from (
    -- select r.fbgn_id
    -- from sfari_pfbgns as sf
    -- inner join
    -- r557_id_index as r
    -- on (sf.pfbgn = r.pfbgn)
-- ) as sf_fbgn_ids
-- inner join
-- gff_genes as gff
-- on (sf_fbgn_ids.fbgn_id = gff.fbgn_id)
-- where gff.gff_file = 'dmel-all-filtered-r5.57.gff'
-- ) as foo
;

-- -- Following code displays how inner join works; it will return every row
-- -- for which the condition is true.
    -- drop table test1;
    -- create table test1 (
        -- col1 int,
        -- col2 int
    -- );

    -- insert into test1 values (1, 2);
    -- insert into test1 values (1, 3);
    -- insert into test1 values (1, 4);
    -- insert into test1 values (2, 5);

    -- drop table test2;
    -- create table test2 (
        -- col3 int,
        -- col4 int
    -- );

    -- insert into test2 values (7, 1);
    -- insert into test2 values (8, 9);

    -- select * from 
    -- test2 inner join test1
    -- on (col4 = col1);

----------- GETTING LISTS OF AUTKB HOMOLOGS --------------
-- -- Create a view of the primary fbgns of the autkb homologs.
-- create or replace view autkb_pfbgns as (
-- select distinct pfbgn, gene_sym
    -- from homologs
    -- inner join
    -- all_fbgns
    -- on (fbgn = psfbgn)
    -- where gene_source = 'autkb' 
-- );

-- Gets the r550 fbgn_ids of the autkb homologs
-- select count (*) from (
    -- select r550.fbgn_id
    -- from autkb_pfbgns as ak
    -- inner join
    -- r550_id_index as r550
    -- on (ak.pfbgn = r550.pfbgn)
    -- order by ak.pfbgn
-- ) as foo
-- ;

-- Returns a list of duplicated fbgns in the inner join of the autkb homolog 
-- pfbgns and the r550 pfbgns.
-- -- select count (*) from (
    -- select sf.pfbgn, sf.gene_sym
    -- from autkb_pfbgns as sf
    -- inner join
    -- r550_id_index as r550
    -- on (sf.pfbgn = r550.pfbgn)
    -- except all 
    -- select distinct sf.pfbgn, sf.gene_sym
    -- from autkb_pfbgns as sf
    -- inner join
    -- r550_id_index as r550
    -- on (sf.pfbgn = r550.pfbgn)
-- -- ) as foo
    -- ;

-- -- Gets the r550 name_names of the autkb homologs:
-- select count (*) from (
-- select gff.fbgn_id, name_name
-- from (
    -- select r550.fbgn_id
    -- from autkb_pfbgns as sf
    -- inner join
    -- r550_id_index as r550
    -- on (sf.pfbgn = r550.pfbgn)
-- ) as sf_fbgn_ids
-- inner join
-- gff_genes as gff
-- on (sf_fbgn_ids.fbgn_id = gff.fbgn_id)
-- where gff.gff_file = 'dmel-all-r5.50.gff'
-- ) as foo
-- ;

-------------- General functions for getting the ------------------- 
-----------release-specific FBGNs of DIOPT homologs ---------------- 

-- CREATE FUNCTION create_homolog_view(viewname text, gene_source text) RETURNS TABLE(f1 text, f2 text) AS $$ create or replace view $1 as (select distinct pfbgn, gene_sym from homologs inner join all_fbgns on (fbgn = psfbgn) where gene_source = $2) $$ LANGUAGE SQL;
        
CREATE TYPE hom_result AS (f1 varchar(20), f2 varchar(100));
CREATE OR REPLACE FUNCTION create_homolog_view(viewname text, gene_source text) RETURNS setof hom_result AS 
        $BODY$
        BEGIN
        -- create or replace view  as (
            return query  
            select distinct pfbgn, gene_sym
            from homologs
            inner join
            all_fbgns
            on (fbgn = psfbgn)
            where homologs.gene_source = $2;
            -- select * from $viewname;
        END
        $BODY$
        LANGUAGE plpgsql;

select create_homolog_view('williams_hom', 'williams');
