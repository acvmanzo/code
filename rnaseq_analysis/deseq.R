#Script for performing DESeq analysis; largely taken from the Anders et al
#2013 Nature Protocols paper 'Count-based differential expression analysis of
#RNA sequencing data using R and Bioconductor'


library("DESeq")
# Loads sample info and counts into R.
samplesDESeq = read.table('metadata.txt', header = TRUE)
print(samplesDESeq)
cds = newCountDataSetFromHTSeqCount(samplesDESeq, directory="")

cds = estimateSizeFactors(cds)
print(cds)
print(sizeFactors(cds))

cdsB = estimateDispersions(cds, method = "blind")
vsd = varianceStabilizingTransformation(cdsB)

print(getwd())
png('pca_plot.png')
plotPCA(vsd, intgroup = "condition")
dev.off()

cds = estimateDispersions(cds)
png('est_disp.png')
plotDispEsts(cds)
dev.off()

res = nbinomTest(cds,"ctrl","expt")
png('ma_plot.png')
plotMA(res)
dev.off()

newres = res[ order(res$padj, decreasing = FALSE), ]
print('newres')
write.table(newres, file="res_DEseq.csv", quote=FALSE, row.names = FALSE)
print('writenewres')
png('raw_pval.png')
hist(res$pval, breaks = 100)
dev.off()

for (i in c(.01, .05)) {
    resSig = res[which(res$padj < i),]
    newressig = resSig[ order(resSig$padj, decreasing = FALSE), ]
    #print( resSig[ order(resSig$log2FoldChange, decreasing = TRUE), ] )
    #print( resSig[ order(resSig$log2FoldChange, decreasing = FALSE), ] )
    write.table( newressig$id, file=paste("res_DEseq_id_",i,sep="") , row.names=FALSE,
              col.names=FALSE, quote=FALSE)
    print(table( res$padj < i ))

    #write.table(resSig[ order(res$padj, decreasing=FALSE), ], 
                #file = paste("res_DEseq_", i, sep=""), 
                #row.names = FALSE, col.names = FALSE, quote=FALSE)
}
