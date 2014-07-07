
library("DESeq")
# Loads sample info and counts into R.
samples = read.table('metadata.txt', header = TRUE)
cds = newCountDataSetFromHTSeqCount(samplesDESeq)

cds = estimateSizeFactors(cds)
print(sizeFactors(cds))

cdsB = estimateDispersions(cds, method = "blind")
vsd = varianceStabilizingTransformation(cdsB)
p = plotPCA(vsd, intgroup = c("condition"))


