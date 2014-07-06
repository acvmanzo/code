
# Copied from Anders et al 2013, Nat Protocols

library("edgeR")
# Loads sample info and counts into R.
samples = read.table('metadata.txt', header = TRUE)
#print(samples)
counts = readDGE(samples$HTSeqPath)$counts
print(paste("dim-counts", dim(counts)))

# Comment from paper - In edgeR, it is recommended to remove features without
# at least 1 read per million in n of the samples, where n is the size of the
# smallest group of replicates (here, n = 3 for the knockdown group)
# cpm(): finds count per million for each gene
cpms = cpm(counts)
#print(dim(cpms))

# min_reps finds the smallest # of replicates among the control or experimental
# groups.  cpms >1 is a Boolean array. rowSums(cpms>1) is the sum of Booleans
# across each row of cpms>1. keep is a Boolean vector that has the value 'True'
# if rowSums(cpms>1) is at least min_reps.
min_reps = min(table(samples$CorE))
keep = rowSums(cpms >1) >= min_reps
counts = counts[keep,]
print(paste("length-keep", length(keep), "first entry in keep", keep[1]))
print(paste("dim-counts", dim(counts)))

colnames(counts) = samples$Sample
# argument after the comma refers to columns
# 5 is the # or rows returned for the head function
print(head( counts[,order(samples$CorE)], 5 ))

# at this step, normalized by total count number for each library
d = DGEList(counts = counts, group = samples$CorE)

# computes the normalization factors; apparently by default edgeR uses 
# method "RLE"
# from manual: method="RLE" is the scaling factor method proposed by Anders and
# Huber (2010). We call it "relative log expression", as median library is
# calculated from the geometric mean of all columns and the median ratio of
# each sample to the median library is taken as the scale factor.
d = calcNormFactors(d)

# Plots an MDS plot.
# From the manual: plotMDS {limma} This function is a variation on the usual
# multdimensional scaling (or principle coordinate) plot, in that a distance
# measure particularly appropriate for the microarray context is used. The
# distance between each pair of samples (columns) is the root-mean-square
# deviation (Euclidean distance) for the top 500 (default) genes. Distances on
# the plot can be interpreted as leading log2-fold-change, meaning the typical
# (root-mean-square) log2-fold-change between the samples for the genes that
# distinguish those samples. If gene.selection is "common", then the top genes
# are those with the largest standard deviations between samples. If
# gene.selection is "pairwise" (default), then a different set of top genes is
# selected for each pair of samples. The pairwise feature selection may be
# appropriate for microarray data when different molecular pathways are
# relevant for distinguishing different pairs of samples. 
# So, for each pair of samples, finds the top 500 genes with the largest
# standard deviations. For each of these genes, finds the log2-fold-change,
# then calculates the distance between samples as the root-mean-square 
# log2-fold-change. I think it applies the classical MDS to produce the plot.
png('mds_plot.png')
plotMDS(d, labels = samples$Sample, col = c("darkgreen","blue")[factor(samples$CorE)])
dev.off()

# From the manual: Implements the method of Robinson and Smyth (2008) for estimating a common dispersion parameter by conditional maximum likelihood. 
d = estimateCommonDisp(d)

# From the manual: This function implements the empirical Bayes strategy
# proposed by Robinson and Smyth (2007) for estimating the tagwise negative
# binomial dispersions. The experimental design is assumed to be a oneway
# layout with one or more experimental groups. The empirical Bayes posterior is
# imple- mented as a conditional likelihood with tag-specific weights.
#The prior values for the dispersions are determined by a global trend. The
#individual tagwise dis- persions are then squeezed towards this trend. The
#prior degrees of freedom determines the weight given to the prior. The larger
#the prior degrees of freedom, the more the tagwise dispersions are squeezed
#towards the global trend. If the number of libraries is large, the prior
#becomes less impor- tant and the tagwise dispersion are determined more by the
#individual tagwise data.
#If trend="none", then the prior dispersion is just a constant, the common dispersion. Otherwise, the trend is determined by a moving average (trend="movingave") or loess smoother applied to the tagwise conditional log-likelihood. method="loess" applies a loess curve of degree 0 as im- plemented in loessByCol
d = estimateTagwiseDisp(d)

#From the manual: This function is useful for exploring the mean-variance
#relationship in the data. Raw variances are, for each gene, the pooled variance
#of the counts from each sample, divided by a scaling factor (by default the
#effective library size). The function will plot the average raw variance for
#tags 70 meanvar split into nbins bins by overall expression level. The averages
#are taken on the square-root scale as for count data the arithmetic mean is
#upwardly biased. Taking averages on the square-root scale provides a useful
#summary of how the variance of the gene counts change with respect to
#expression level (abundance). A line showing the Poisson mean-variance
#relationship (mean equals variance) is always shown to illustrate how the
#genewise variances may differ from a Poisson mean- variance relationship.
#Optionally, the raw variances and estimated tagwise variances can also be
#plotted. Estimated tagwise variances can be calculated using either qCML
#estimates of the tagwise dispersions (estimateTagwiseDisp) or Cox-Reid
#conditional inference estimates (CRDisp). A log- log scale is used for the plot.
#NB line: shows the mean-variance relationship for a NB model with common
#dispersion 
png('mean_var_plot.png')
plotMeanVar(d, show.tagwise.vars = TRUE, NBline = TRUE)
legend(20,10000000000, c("Ave raw var", "Tag var", "NB line"), 
       pch=c('X','o','-'), col=c("darkred", "lightskyblue", "dodgerblue2")) 
title('Variance vs. mean')
dev.off()

#From the manual: Plot genewise biological coefficient of variation (BCV)
#against gene abundance (in log2 counts per million).
png('biol_cv_plot.png')
plotBCV(d)
title('Disperions vs. abundance')
dev.off()

#From the manual: The functions test for differential expression between two
#groups of count libraries. They imple- ment the exact test proposed by Robinson
#and Smyth (2008) for a difference in mean between two groups of negative
#binomial random variables.  
de = exactTest(d, pair = c("ctrl","expt"))

#From the manual: Extracts info about each gene into a data frame for a given
#pair of groups, ranked by p-value or absolute log-fold change.
tt = topTags(de, n = nrow(d))
print(head(tt))
#print(nrow(d))
#Writes the output of toptags into a file.
write.csv(tt$table, file = "toptags_edgeR.csv")

#From the paper:Inspect the depth-adjusted reads per million for some of the differentially expressed genes
nc = cpm(d, normalized.lib.sizes = TRUE) 
rn = rownames(tt$table) 
head(nc[rn,order(samples$CorE)],5)

for (i in c(.01, .05)) {
    deg = rn[tt$table$FDR < i] 
    print(paste("DE genes where FDR<",i,sep=""))
    print(deg)
    #From the paper: M (‘minus’) versus A (‘add’) plots for RNA-seq data. 
    #edgeR’s plotSmear function plots the log-fold change (i.e., the log ratio of
    #normalized expression levels between two experimental conditions) against the
    #log counts per million (CPM).  
    #From the manual: To represent counts that were low (e.g. zero in 1 library and
    #non-zero in the other) in one of the two conditions, a ’smear’ of points at low
    #A value is presented in plotSmear.
    png(paste("masmear_plot",i,".png",sep=""))
    plotSmear(d, de.tags = deg)
    legend(10,3, c("DE genes"), pch=c(19), col=c("darkred")) 
    title('Log fold change vs abundance')
    dev.off()

    #Writes the output of toptags for the statistically significant genes when 
    #controlling for the FDR at the given level. 
    fdr = tt$table$FDR < i
    write.table(deg, file = paste("toptags_edgeR_",i,"gene", sep=""), 
                row.names = FALSE, col.names = FALSE, quote=FALSE)
}
