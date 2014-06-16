
library("edgeR")
samples = read.table('metadata.txt', header = TRUE)
#print(samples)
counts = readDGE(samples$HTSeqPath)$counts
#print(counts)
noint = rownames(counts) %in% c("no_feature","ambiguous","too_low_aQual", "not_aligned","alignment_not_unique")
cpms = cpm(counts)
keep = rowSums(cpms >1) >= 3 & !noint
counts = counts[keep,]

colnames(counts) = samples$Sample
#print(head( counts[,order(samples$CorE)], 5 ))
d = DGEList(counts = counts, group = samples$CorE)
d = calcNormFactors(d)

#plotMDS(d, labels = samples$Sample, col = c("darkgreen","blue")[factor(samples$CorE)])

d = estimateCommonDisp(d)
d = estimateTagwiseDisp(d)

#plotMeanVar(d, show.tagwise.vars = TRUE, NBline = TRUE)
#plotBCV(d)

de = exactTest(d, pair = c("ctrl","expt"))
tt = topTags(de, n = nrow(d))
#print(head(tt$table))

nc = cpm(d, normalized.lib.sizes = TRUE) 
rn = rownames(tt$table) 
#head(nc[rn,order(samples$condition)],5)

deg = rn[tt$table$FDR < .05] 
#print(deg)
#plotSmear(d, de.tags = deg)

write.csv(tt$table, file = "toptags_edgeR.csv")
fdr05 = tt$table$FDR < 0.05
#print(fdr05)
write.table(deg, file = "toptags_edgeR_fdr05_gene", row.names = FALSE, 
            col.names = FALSE, quote=FALSE)

