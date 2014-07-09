-- CODE FOR MANIPULATING GENE LISTS IN SQL

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
-- \copy homologs from '/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/williams/sarah_williams_genes_diopt_output_filtered.txt'


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
    -- select gff.name_name, gff.fbgn_id, allf.pfbgn from
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
    -- select gff.name_name, gff.fbgn_id, allf.pfbgn from
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

-------------- GENERAL FUNCTIONS FOR GETTING THE ------------------- 
-----------RELEASE-SPECIFIC FBGNs OF DIOPT HOMOLOGS ---------------- 

---- Creates a view showing the current primary fbgns for genes in gene_table
---- for a specific gene source. The gene table can be homologs, or 
---- flyatlas_brain for instance. Changed tack - this is no longer useful.
-- DROP FUNCTION create_homolog_view(text,text,text);
-- CREATE FUNCTION create_homolog_view(viewname text, tablename text, gene_source text) RETURNS void
-- AS 
        -- $BODY$
        -- BEGIN
        -- EXECUTE format('
        -- create or replace view %s as 
            -- select distinct all_fbgns.pfbgn, all_fbgns.gene_sym
            -- from %s
            -- inner join
            -- all_fbgns
            -- on (fbgn = psfbgn)
            -- where %s.gene_source = %L;'
            -- ,viewname
            -- ,tablename
            -- ,tablename
            -- ,gene_source);

        -- END
        -- $BODY$
        -- LANGUAGE plpgsql;

-- -- select * from create_homolog_view('sarah_williams_pfbgns', 'homologs', 'sarah_williams');
-- select * from create_homolog_view('williams_pfbgns', 'homologs', 'williams');


-- -- -- One homolog/gene view with pfbgns of homologs -- -- --
-- create or replace view homolog_pfbgns as 
    -- select distinct all_fbgns.pfbgn, homologs.fly_sym, homologs.gene_source
    -- from homologs
    -- inner join
    -- all_fbgns
    -- on (homologs.fbgn = all_fbgns.psfbgn)
    -- UNION
    -- select distinct all_fbgns.pfbgn, flyatlas_brain.gene_sym, flyatlas_brain.gene_source
    -- from flyatlas_brain 
    -- inner join
    -- all_fbgns
    -- on (flyatlas_brain.fbgn = all_fbgns.psfbgn)
    -- where upordown = 'Up';




---- Returns the gff-specific fbgn_ids and name_names for the pfbgns in
---- the homolog view.
-- DROP FUNCTION get_homolog_gff_names(text,text,text);
-- CREATE OR REPLACE FUNCTION get_homolog_gff_names(id_index text, gff_file text, gene_source text) RETURNS TABLE (gff_fbgn_id varchar(20), gff_name_name varchar(100)) as
    -- $BODY$
    -- BEGIN
    -- RETURN QUERY EXECUTE format ('
        -- select gff.fbgn_id, gff.name_name
        -- from (
            -- select r.fbgn_id
            -- from homolog_pfbgns as h 
            -- inner join
            -- %I as r
            -- on (h.pfbgn = r.pfbgn)
            -- where h.gene_source = %L
        -- ) as h_fbgn_ids
        -- inner join
        -- gff_genes as gff
        -- on (h_fbgn_ids.fbgn_id = gff.fbgn_id)
        -- where gff.gff_file = %L 
        -- ;'
        -- ,id_index
        -- ,gene_source
        -- ,gff_file);
    -- END
    -- $BODY$
    -- LANGUAGE plpgsql;
        
-- select count(*) from (select distinct gff_fbgn_id from get_homolog_gff_names('r550_id_index', 'autkb_pfbgns', 'dmel-all-r5.50.gff')) as foo;
-- select count(*) from (select distinct gff_fbgn_id from get_homolog_gff_names('r557_id_index', 'flyatlasbrain_pfbgns', 'dmel-all-filtered-r5.57.gff')) as foo;
-- select * from get_homolog_gff_names('r550_id_index', 'sarah_williams_pfbgns', 'dmel-all-r5.50.gff')

------------------------------------------------------------------------
---- Copying Sarah's list of Brain, Williams, and autism genes. ----

-- DROP TABLE sarah_bwa;
-- CREATE TABLE sarah_bwa (
    -- name_name varchar (100),
    -- unique (name_name)
-- );

-- -- Used linux's cat, sort, and uniq functions to get the uniq names out.
-- -- \copy sarah_bwa from '/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/BWA_GENELIST_0626_uniq.txt'
-- -- This version already has no duplicates.
-- \copy sarah_bwa from '/home/andrea/rnaseqanalyze/references/gene_lists/brain_autism_williams_genes/BWA_compare/BWA_GENELIST_0701.txt'


-- --Checking to see if sarah_williams_pfbgns are in sarah's BWA list.
-- select * from 
        -- (select gff_fbgn_id, gff_name_name 
            -- from get_homolog_gff_names('r550_id_index', 'sarah_williams_pfbgns', 'dmel-all-r5.50.gff'))
            -- as hnames
        -- left outer join
        -- sarah_bwa as sbwa
        -- on (hnames.gff_name_name = sbwa.name_name)
        -- order by gff_name_name;

---- Copies above query into a file.
-- \copy (select * from (select gff_fbgn_id, gff_name_name from get_homolog_gff_names('r550_id_index', 'sarah_williams_pfbgns', 'dmel-all-r5.50.gff')) as hnames left outer join sarah_bwa as sbwa on (hnames.gff_name_name = sbwa.name_name) order by gff_name_name) to '/home/andrea/rnaseqanalyze/references/brain_autism_williams_genes/williams/Sarah/williams_genes_not_in_bwa.csv' header csv;


------------------------------------------------------------------------
----- Copying results from Flyatlas into the database. ------

-- drop table flyatlas_brain;
-- CREATE TABLE flyatlas_brain (
    -- probe varchar(20),
    -- fbgn varchar(20),
    -- gene_long_name varchar(100),
    -- gene_sym varchar(100),
    -- upordown varchar(20),
    -- brainmean real,
    -- brainsem real,
    -- brainpresent real,
    -- brain_vs_fly real,
    -- gene_source varchar(20),
    -- unique (probe, fbgn)
-- );

-- \copy flyatlas_brain from '/home/andrea/rnaseqanalyze/references/gene_lists/brain_autism_williams_genes/flyatlas_brain/microarray_fbgn_brain_db.txt';

-- -- Stats about fly atlas genes:
-- # rows: 
-- rnaseq=# select count (*) from flyatlas_brain;
 -- count 
-- -------
 -- 19545
-- (1 row)

-- # distinct gene symbols/fbgns:
-- rnaseq=# select count (*) from (select distinct gene_sym from flyatlas_brain ) as foo;
 -- count 
-- -------
 -- 13255
-- (1 row)

-- rnaseq=# select count (*) from (select distinct fbgn from flyatlas_brain ) as foo;
 -- count 
-- -------
 -- 13255
-- (1 row)

-- # distinct gene symbols/fbgns that are upregulated in the brain:
-- rnaseq=# select count (*) from (select distinct gene_sym from flyatlas_brain where upordown = 'Up') as foo;
 -- count 
-- -------
  -- 3878
-- (1 row)

-- # homologs in homolog_pfbgns:
-- rnaseq=# select count (*) from homolog_pfbgns where gene_source = 'fly_atlas';
 -- count 
-------
  -- 3856
-- (1 row)

-- -- Creates a flyatlas view with the current primary fbgns of the flyatlas
-- -- brain-upregulated genes. Couldn't use the create_homolog_view function
-- -- because of extra upordown condition. Never mind, just added fly_atlas items
-- -- to the homolog_pfbgns view (see create statement for that).
-- create or replace view flyatlasbrain_pfbgns as 
    -- select distinct all_fbgns.pfbgn, all_fbgns.gene_sym
    -- from flyatlas_brain 
    -- inner join
    -- all_fbgns
    -- on (fbgn = psfbgn)
    -- where flyatlas_brain.gene_source = 'fly_atlas' AND upordown = 'Up';

-- select count(*) from (select distinct gff_fbgn_id from get_homolog_gff_names('r557_id_index', 'flyatlasbrain_pfbgns', 'dmel-all-filtered-r5.57.gff')) as foo;

-- -- SFARI list only -- --
-- CREATE OR REPLACE VIEW sfari_r557 AS (
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r557_id_index', 'dmel-all-filtered-r5.57.gff', 'sfari'))
-- ;


-- Brain-expressed genes only --
-- CREATE OR REPLACE VIEW brain_r557 AS (
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r557_id_index', 'dmel-all-filtered-r5.57.gff', 'fly_atlas')
-- order by gene_short_name)
-- ;
-- rnaseq=# select count (*) from brain_r557 ;
 -- count 
-- -------
  -- 3746
-- (1 row)

-- ---Putting all the lists together ------
-- CREATE OR REPLACE VIEW bwa_r557 AS (
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r557_id_index', 'dmel-all-filtered-r5.57.gff', 'williams')
-- UNION
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r557_id_index', 'dmel-all-filtered-r5.57.gff', 'sfari')
-- UNION
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r557_id_index', 'dmel-all-filtered-r5.57.gff', 'autkb')
-- UNION
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r557_id_index', 'dmel-all-filtered-r5.57.gff', 'fly_atlas')
-- order by gene_short_name)
-- ;

-- CREATE OR REPLACE VIEW bwa_r550 AS (
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r550_id_index', 'dmel-all-r5.50.gff', 'williams')
-- UNION
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r550_id_index', 'dmel-all-r5.50.gff', 'sfari')
-- UNION
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r550_id_index', 'dmel-all-r5.50.gff', 'autkb')
-- UNION
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r550_id_index', 'dmel-all-r5.50.gff', 'fly_atlas')
-- order by gene_short_name)
-- ;

----------- OLD ------------
-- CREATE VIEW bwa_r550 AS (
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r550_id_index', 'flyatlasbrain_pfbgns', 'dmel-all-r5.50.gff')
-- UNION
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r550_id_index', 'autkb_pfbgns', 'dmel-all-r5.50.gff')
-- UNION
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r550_id_index', 'sfari_pfbgns', 'dmel-all-r5.50.gff')
-- UNION
-- select distinct gff_fbgn_id as tracking_id, gff_name_name as gene_short_name from get_homolog_gff_names('r550_id_index', 'williams_pfbgns', 'dmel-all-r5.50.gff')
-- order by gene_short_name)
-- ;

-- -- -- -- -- Comparing my r5.50 bwa list with Sarah's r5.50 bwa list -- -- --

-- -- Genes in Sarah's list that aren't in mine -- --
-- select name_name from sarah_bwa
-- EXCEPT
-- select sarah.name_name
    -- from bwa_r550 as mine
    -- inner join
    -- sarah_bwa as sarah
    -- on (sarah.name_name = mine.gene_short_name)
-- -- order by gene_short_name
-- order by name_name
    -- ;

-- -- -- Genes in My list that aren't in Sarah's -- --
-- select gene_short_name from bwa_r550
-- EXCEPT
-- select sarah.name_name
    -- from bwa_r550 as mine
    -- inner join
    -- sarah_bwa as sarah
    -- on (sarah.name_name = mine.gene_short_name)
-- order by gene_short_name
    -- ;

---- Incorporating Ralph's list of gene he is not interested in ----
-- create table ralph_ex_genes(
    -- gene_name varchar(100)
-- );

-- \copy ralph_ex_genes from '/home/andrea/rnaseqanalyze/references/gene_lists/brain_autism_williams_genes/ralph_genes_exclude.txt';

-- -- -- Lists genes that are in my list excluding Ralph's
-- create or replace view bwa_r557_ralph_mt_ex as (
    -- select gene_short_name from bwa_r557
    -- except
    -- select gene_name from ralph_ex_genes
    -- except 
    -- select gene_name from mt_ex_genes
    -- order by gene_short_name);


-- -- List of genes encoding mitochondrial proteins that I am excluding
-- create table mt_ex_genes(
    -- gene_name varchar(100)
-- );
-- \copy mt_ex_genes from '/home/andrea/rnaseqanalyze/references/gene_lists/brain_autism_williams_genes/mt_genes_exclude.txt'SELECT EXISTS(

---- Code for checking if a table exists (c.relname)
-- SELECT EXISTS(
-- SELECT 1 
-- FROM   pg_catalog.pg_class c
-- JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
-- WHERE  n.nspname = 'public'
-- AND    c.relname = 'htseq_prot_coding_genes'
-- );;

-- -- Renaming the brain_aut_will tables to 'baw'
-- alter table brain_aut_will_r550 rename to bwa_r550;
-- alter table brain_aut_will_r557 rename to bwa_r557;
-- alter table brain_aut_will_r557_ralph_mt_excluded rename to bwa_r557_ralph_mt_ex;
