x = read.csv("decountf+m_fdr10_fbgns.txt")

hist(x$sum_counts)

library("ggplot2")
x = degenes
degenes = data.frame(sapply(degenes, as.numeric))

png('hist_decountf+m_fdr10_fbgns.png')

ggplot(degenes, aes(x=x.sum_counts)) + geom_histogram(binwidth=1, fill="gray", colour="black")
dev.off()

