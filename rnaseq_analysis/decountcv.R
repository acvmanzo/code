
library("ggplot2")
args <- commandArgs(trailingOnly = TRUE)
print(args)

cvffile <- args[1]
cvmfile <- args[2]
histfname <- args[3]
histmname <- args[4]

cvf = read.table(cvffile, header=TRUE)$CV
cvm = read.table(cvmfile, header=TRUE)$CV


#countsub = countsf
#dfcountsub = data.frame(sapply(countsub, as.numeric))
#png('test3.png')
#ggplot(dfcountsub, aes(x=countsub)) + 
    #geom_histogram(binwidth=1, fill="gray", colour="black") +
    #theme(axis.text.x = element_text(size=14, colour='black'),
        #axis.text.y = element_text(size=14, colour='black'),
        #axis.title.x = element_text(size=16),
        #axis.title.y = element_text(size=16),
        #legend.text = element_text(size=14),
        #legend.title = element_text(size=16)
        #) +
    #xlim(1, 7)
#dev.off()
#print(getwd())

plotcounthist <- function(countsub, pngname) {
    dfcountsub = data.frame(cv = sapply(countsub, as.numeric))
    #print(head(dfcountsub))
    png(pngname)
    #print(pngname)
    plotobj = ggplot(dfcountsub, aes(x=cv)) + 
        geom_histogram(binwidth=0.03, fill="gray", colour="black") +
        theme(axis.text.x = element_text(size=14, colour='black'),
            axis.text.y = element_text(size=14, colour='black'),
            axis.title.x = element_text(size=16),
            axis.title.y = element_text(size=16),
            legend.text = element_text(size=14),
            legend.title = element_text(size=16)
            ) +
        xlim(0, 1)
    print(plotobj)
    dev.off()
    print(getwd())
}

plotcounthist(cvf, histfname)
plotcounthist(cvm, histmname)

plot(cvf)
#plotcounthist(countsm, name)

