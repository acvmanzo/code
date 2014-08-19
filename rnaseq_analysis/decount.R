#x = read.csv("decountf+m_fdr10_fbgns.txt")

#hist(x$sum_counts)

#library("ggplot2")
#x = degenes
#degenes = data.frame(sapply(degenes, as.numeric))

#png('hist_decountf+m_fdr10_fbgns.png')

#ggplot(degenes, aes(x=x.sum_counts)) + geom_histogram(binwidth=1, fill="gray", colour="black")
#dev.off()

library("ggplot2")
args <- commandArgs(trailingOnly = TRUE)
print(args)

countfile <- args[1]
histfname <- args[2]
histmname <- args[3]

counts = read.csv(countfile)
countsf = counts$avg_f[counts$avg_f != 0]
countsm = counts$avg_m[counts$avg_m != 0]

addmeanstd <- function(df, inmean, instd) {
    df$mean <- toString(inmean)
    df$sd <- toString(instd)
    return(df)
}

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
    dfcountsub = data.frame(num_genotypes = sapply(countsub, as.numeric))
    #print(head(dfcountsub))
    png(pngname)
    #print(pngname)
    plotobj = ggplot(dfcountsub, aes(x=num_genotypes)) + 
        geom_histogram(binwidth=1, fill="gray", colour="black") +
        theme(axis.text.x = element_text(size=14, colour='black'),
            axis.text.y = element_text(size=14, colour='black'),
            axis.title.x = element_text(size=16),
            axis.title.y = element_text(size=16),
            legend.text = element_text(size=14),
            legend.title = element_text(size=16)
            ) +
        xlim(1, 7)
    print(plotobj)
    dev.off()
    print(getwd())
}

plotcounthist(countsf, histfname)
plotcounthist(countsm, histmname)

