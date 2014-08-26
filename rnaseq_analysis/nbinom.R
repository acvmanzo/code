#Plots histograms and probability densities of negative binomial and poisson distributions with different parameters.

library("ggplot2")

mu1 = 100
disp1 = 0.1

mu2 = 500
disp2 = 0.01

mean1 = 50
sd1 = 10

mean2 = 160
sd2 = 10

mean3 = 100
sd3 = 25

xmin = 0
xmax = 200
#lamda1 = 100

n1df <- data.frame(values = rnbinom(n = 100000, mu=mu1, size=(1/disp1)))
n2df <- data.frame(values = rnbinom(n = 100000, mu=mu2, size=(1/disp2)))
p1df <- data.frame(values = rpois(n = 100000, lambda=mu1))
g1df <- data.frame(values = rnorm(n = 100000, mean=mean1, sd=sd1))
g2df <- data.frame(values = rnorm(n = 100000, mean=mean2, sd=sd2))
g3df <- data.frame(values = rnorm(n = 100000, mean=mean3, sd=sd3))
#n1df$mu <- toString(mu1)
#n1df$size <- toString(size1)


addmeanstd <- function(df, inmean, instd) {
    df$mean <- toString(inmean)
    df$sd <- toString(instd)
    return(df)
}

addmusize <- function(df, inmu, insize) {
    df$mu <- toString(inmu)
    df$disp <- toString(insize)
    return(df)
}

n1df = addmusize(n1df, mu1, disp1)
n2df = addmusize(n2df, mu2, disp2)
p1df = addmusize(p1df, mu1, 0)
g1df = addmeanstd(g1df, mean1, sd1)
g2df = addmeanstd(g2df, mean2, sd2)
g3df = addmeanstd(g3df, mean3, sd3)

ndf <- rbind(n1df, n2df)
pdf <- rbind(n1df, p1df)
gdf <- rbind(g1df, g2df)

png(paste('norm_density_mean3_', mean3, '_sd3_', sd3, '.png', sep=''))
#point = data.frame(x=750, y=0.001)
#p <- ggplot(point, aes(x, y))

ggplot(g3df, aes(x=values, fill=mean)) + 
    geom_density(alpha=0.3) + 
    theme(axis.text.x = element_text(size=14, colour='black'),
          axis.text.y = element_text(size=14, colour='black'),
          axis.title.x = element_text(size=16),
          axis.title.y = element_text(size=16),
          legend.text = element_text(size=14),
          legend.title = element_text(size=16)
          ) +
    xlim(xmin, xmax)

dev.off()

png(paste('norm_density_mean1_', mean1, '_sd1_', sd1, '_mean2_', mean2, '_sd2_', sd2, '.png', sep=''))
ggplot(gdf, aes(x=values, fill=mean)) + 
    geom_density(alpha=0.3) + 
    theme(axis.text.x = element_text(size=14, colour='black'),
          axis.text.y = element_text(size=14, colour='black'),
          axis.title.x = element_text(size=16),
          axis.title.y = element_text(size=16),
          legend.text = element_text(size=14),
          legend.title = element_text(size=16)
          ) +
    xlim(xmin, xmax)
dev.off()

#png(paste('poiss_vs_nbinom_density_mu1_', mu1, '_disp1_', disp1, '.png', sep=''))
#ggplot(pdf, aes(x=values, fill=disp)) + 
    #geom_density(alpha=0.3) + 
    #theme(axis.text.x = element_text(size=14, colour='black'),
          #axis.text.y = element_text(size=14, colour='black'),
          #axis.title.x = element_text(size=16),
          #axis.title.y = element_text(size=16),
          #legend.text = element_text(size=14),
          #legend.title = element_text(size=16)
          #)

#dev.off()

#png(paste('nbinom_density_mu1_', mu1, '_d1_', disp1, '_mu2_', mu2, '_d2_', disp2, '.png',sep=''))
#ggplot(ndf, aes(x=values, fill=mu)) + 
    #geom_density(alpha=0.3) +
    #theme(axis.text.x = element_text(size=14, colour='black'),
          #axis.text.y = element_text(size=14, colour='black'),
          #axis.title.x = element_text(size=16),
          #axis.title.y = element_text(size=16),
          #legend.text = element_text(size=14),
          #legend.title = element_text(size=16)
          #)
#dev.off()
#png('poiss_vs_nbinom_hist.png')
#ggplot(pdf, aes(x=x, fill=disp)) + geom_histogram(binwidth=0.5, position='identity')
##ggplot(xdf, aes(x=x, fill=size)) + geom_density(alpha=0.3)
