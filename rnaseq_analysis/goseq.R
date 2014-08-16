#Taken from the user guide.

#run_goseq <- function(
#myfunction <- function(arg1, arg2, ... ){
#statements
#return(object)
#}
library(goseq)
de = scan('de_all_fdr05.txt', what='character')

all = scan('/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str_good/prot_coding_genes/GO_analysis/prot_coding_genes_genes.txt' ,what='character')

gene.vector = as.integer(all%in%de) # List of 0's and 1's of length all, 0 if not de, 1 otherwise.
#print(gene.vector)

names(gene.vector)=all
head(gene.vector)
print(length(gene.vector))

lengths = scan('/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str_good/prot_coding_genes/GO_analysis/gene_lengths.txt', what='integer')
head(lengths)
lengths = as.numeric(lengths)
head(lengths)

genesgo = read.table('/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str/prot_coding_genes/GO_analysis/genes_go.txt')
head(genesgo)

pwf = nullp(gene.vector, 'dmel', 'gene', bias.data = lengths, plot.fit=TRUE)
GO.wall = goseq(pwf,'dmel','gene',genesgo)
head(GO.wall)
fdroverpval = p.adjust(GO.wall$over_represented_pvalue, method="BH")
fdrunderpval = p.adjust(GO.wall$under_represented_pvalue, method="BH")

GO.wall$fdr_over_rep_pval = fdroverpval
GO.wall$fdr_under_rep_pval = fdrunderpval
head(GO.wall)
#colnames(enriched.GO) <- c("category","adj_over_rep_pval")

#indices = p.adjust(GO.wall$over_represented_pvalue, method="BH")<.05
#print(enriched.GO)
write.table(GO.wall, file = 'de_all_fdr05_goseq.txt',
            row.names = FALSE, col.names = FALSE, quote=FALSE)
