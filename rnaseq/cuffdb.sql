
CREATE TABLE cuffgenes_fpkm 
(
tracking_id character varying(20),
class_code character varying(2),
nearest_ref_id character varying(2),
gene_id character varying(20),
gene_short_name character varying(20),
tss_id character varying(2),
locus character varying(20),
length character varying(2),
coverage character varying(2),
FPKM real ,
FPKM_conf_lo real,
FPKM_conf_hi real,
FPKM_status character varying(5),
sample character varying(20)
);

