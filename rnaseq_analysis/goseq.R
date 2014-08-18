#Taken from the user guide.

#run_goseq <- function(
#myfunction <- function(arg1, arg2, ... ){
#statements
#return(object)
#}

#options(echo=TRUE) # if you want see commands in output file
args <- commandArgs(trailingOnly = TRUE)
print(args)

defile <- args[1]
allgenefile <- args[2]
countfile <- args[3]
gogenefile <- args[4]
pwfplotfile <- args[5]
goresultfile <- args[6]
#dbgoresultfile <- args[7]

library(goseq)

# Load list of DE genes, list of all genes tested, counts, and mapping between gene ids and 
# GO categories.
de = scan(defile, what='character')
all = scan(allgenefile ,what='character')
counts = read.csv(countfile)
genesgo = read.table(gogenefile)

gene.vector = as.integer(all%in%de) # List of 0's and 1's of length all, 0 if not de, 1 otherwise.
names(gene.vector)=all
head(gene.vector)
print(paste("# genes =", length(gene.vector)))

#lengths = scan('/home/andrea/Documents/lab/RNAseq/analysis/edger/results_tophat_2str_good/prot_coding_genes/GO_analysis/gene_lengths.txt', what='integer')
#head(lengths)
#lengths = as.numeric(lengths)
#head(lengths)

# Get the summed list of counts; used as bias vector for calculating the probability weighting
# function.
countbias = rowSums(counts[-1])
print(paste("# genes in bias vector =", length(countbias)))

#Finds the probability weighting function (here based on counts, not length. Power to detect DE
#depends on counts (which in turn depends on length and expression). From the manual:
#"This is done by calculating a Probability Weighting Function or PWF which can be thought of as a
#function which gives the probability that a gene will be differentially expressed (DE), based on
#its length alone. The PWF is calculated by fitting a monotonic spline to the binary data series of
#differential expression (1=DE, 0=Not DE) as a function of gene length. The PWF is used to weight
#the chance of selecting each gene when forming a null distribution for GO category membership." 
png(pwfplotfile) 
pwf = nullp(gene.vector, bias.data = countbias, plot.fit=TRUE)
dev.off()

#GO analysis using the Wallenius distribution to form the null distribution. From the manual: "GO
#analysis of RNA-seq data requires the use of random sampling in order to generate a suitable null
#distribution for GO category membership and calculate each categories significance for over
#representation amongst DE genes.  However, this random sampling is computationally expensive. In
#most cases, the Wallenius distribution can be used to approximate the true null distribution,
#without any significant loss in accuracy"
GO.wall = goseq(pwf, gene2cat = genesgo)
head(GO.wall)
fdroverpval = p.adjust(GO.wall$over_represented_pvalue, method="BH")
fdrunderpval = p.adjust(GO.wall$under_represented_pvalue, method="BH")

GO.wall$fdr_over_rep_pval = fdroverpval
GO.wall$fdr_under_rep_pval = fdrunderpval
head(GO.wall)
#colnames(enriched.GO) <- c("category","adj_over_rep_pval")

#indices = p.adjust(GO.wall$over_represented_pvalue, method="BH")<.05
#print(enriched.GO)
write.table(GO.wall, file = goresultfile,
            row.names = FALSE, col.names = TRUE, quote=FALSE, sep=",")
#write.table(GO.wall, file = goresultfile,
            #row.names = FALSE, col.names = FALSE, quote=FALSE)
