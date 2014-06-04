#!/usr/bin/Rscript

# Script for use with WGCNA Tutorial 1, step 3. Plots all the gene significance for weight vs. module membership for all modules.

# Load the WGCNA package
library(WGCNA);
# The following setting is important, do not omit.
options(stringsAsFactors = FALSE);
# Load the expression and trait data saved in the first part
lnames = load(file = "FemaleLiver-01-dataInput.RData");
# Load network data saved in the second part.
lnames = load(file = "FemaleLiver-02-networkConstruction-auto.RData");

# Define numbers of genes and samples
nGenes = ncol(datExpr);
nSamples = nrow(datExpr);
# Recalculate MEs with color labels
MEs0 = moduleEigengenes(datExpr, moduleColors)$eigengenes;
MEs = orderMEs(MEs0);
moduleTraitCor = cor(MEs, datTraits, use = "p");
moduleTraitPvalue = corPvalueStudent(moduleTraitCor, nSamples);

# Define variable weight containing the weight column of datTrait
weight = as.data.frame(datTraits$weight_g);
names(weight) = "weight";
# names (colors) of the modules
modNames = substring(names(MEs), 3)

# Find gene module membership.
geneModuleMembership = as.data.frame(cor(datExpr, MEs, use = "p"));
MMPvalue = as.data.frame(corPvalueStudent(as.matrix(geneModuleMembership), nSamples));
names(geneModuleMembership) = paste("MM", modNames, sep="");
names(MMPvalue) = paste("p.MM", modNames, sep="");
 
# Find correlation of genes with weight.
geneTraitSignificance = as.data.frame(cor(datExpr, weight, use = "p"));
GSPvalue = as.data.frame(corPvalueStudent(as.matrix(geneTraitSignificance), nSamples));
names(geneTraitSignificance) = paste("GS.", names(weight), sep="");
names(GSPvalue) = paste("p.GS.", names(weight), sep="");

# Order the modules in descending correlation of weight with module eigengene.
modOrder = order(-abs(cor(MEs, weight, use = "p")));

# Graph the gene significance vs. module membership for each module.
for (i in 1:length(modOrder))
{
colnum = modOrder[i] # Column of the dataframe geneModuleMembership that contain data for this module.
modn = modNames[colnum] # Name of the module. 
print(modn)
modcor = moduleTraitCor[colnum,1] # Correlation of module eigengene with the trait. 

# Finding the rows with module genes.
moduleGenes = moduleColors==modn; # Returns a list with TRUE if the gene is in the module and FALSE if the gene is not in the module.
notmoduleGenes = moduleColors!=modn; # Returns a list with TRUE if the gene is not in the module.

# Finding the module membership.
modmem = geneModuleMembership[, colnum] # Returns a list of values with the module membership for every gene.
modmemsub = geneModuleMembership[moduleGenes, colnum] # Returns a list of values with the module membership for every gene clustered in the module (those that should have high module membership).
modmemnotsub = geneModuleMembership[notmoduleGenes, colnum] # Returns a list of values with the module membership for every gene not in the module (presumably lower module membership).

# Finding the gene trait significance.
gTSsub = geneTraitSignificance[moduleGenes,1] # Returns a list of values with the gene train significance for every gene in the module.
gTSnotsub = geneTraitSignificance[notmoduleGenes, 1] # Returns a list of values with the gene train significance for every gene not in the module.

# Find the correlation of each gene with the trait.
corvalall = cor(abs(modmem), abs(geneTraitSignificance[,1])) # Using all the genes.
corvalsub = cor(abs(modmemsub), abs(gTSsub)) # Using only the genes in the module.
corvalnotsub = cor(abs(modmemnotsub), abs(gTSnotsub)) # Using only the genes not in the module.

# Define the figure titles and the name of the figure.
figtitlea = paste('All Genes', 'cor', signif(corvalall,3), sep=' ')
figtitlesub = paste('Module Genes', 'cor', signif(corvalsub,3), sep=' ')
figtitlenotsub = paste('All but module genes', 'cor', signif(corvalnotsub,3), sep=' ')
figname = paste(i, modn, '.jpg', sep='')

# Plot the figure.
jpeg(figname, width=720, height=720)
par(mfrow=c(2,2), oma=c(1,1,4,1))

# Plots all the genes.
plot(abs(modmem), abs(geneTraitSignificance[,1]), main=figtitlea, xlab='Module Membership', ylab='Gene Significance', col='blue')
points(abs(modmemsub), abs(gTSsub), col='red')

# Plots only the genes in the module.
plot(abs(modmemsub), abs(gTSsub), main=figtitlesub, xlab='Module Membership', ylab='Gene Significance', col='red')

# Plots only the genes not in the module.
plot(abs(modmemnotsub), abs(gTSnotsub), main=figtitlenotsub, xlab='Module Membership', ylab='Gene Significance', col='blue')

title(paste(modn, 'module correlation', signif(modcor, 3), sep=' '), outer=TRUE)
#legend('bottom', 'Legend')
#par(v)
dev.off()

}


