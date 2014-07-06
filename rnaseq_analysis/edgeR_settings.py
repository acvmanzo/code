


#MALES = ['Betaintnu_M', 'CG34127_M', 'en_M', 'Nhe3_M', 'NrxI_M', 'NrxIV_M', 'pten_M']
MALES = ['Betaintnu_M']
MALES_CTRL = 'CS_M'
DIRMALES = MALES
MALE_PARAMS = (DIRMALES, MALES, MALES_CTRL)

#FEMALES = ['Betaintnu_F', 'CG34127_F', 'en_F', 'Nhe3_F', 'NrxI_F', 'NrxIV_F', 'pten_F']
#FEMALES_CTRL = 'CS_F'
#DIRFEMALES = FEMALES
#FEMALE_PARAMS = (DIRFEMALES, FEMALES, FEMALES_CTRL)

AGG_DICT_ALL = {'lowagg': ['CG34127_M', 'en_M', 'NrxI_M'],
             'ctrl': ['Betaintnu_M', 'Nhe3_M', 'NrxIV_M', 'pten_M', 'CS_M']
             }
#LOWAGG = ['lowagg', 'lowagg']
#NORMAGG = ['CS', 'normagg']
#DIRAGGS = ['lowagg_vs_CS', 'lowagg_vs_normagg_CS']
#agg_params = (DIRAGGS, LOWAGG, NORMAGG)

#DEGENETABLE = 'degenes'
#DEGENEDIR = '/home/andrea/Documents/lab/RNAseq/analysis/edgeR/prot_coding_genes'
#DEGENEFILE = 'toptags_edgeR.csv'
#DB_DEGENEFILE = 'db_toptags_edgeR.csv'
#FDR_TH = 0.05
#FDR_DEGENEFILE = 'toptags_edgeR_fdr{}.csv'.format(FDR_TH)
