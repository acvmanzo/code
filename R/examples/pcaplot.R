# Script for demonstrating PCA using singular value decomposition.

# Data
g1 = c(1, 2, 3)
g2 = c(4, 5, 6)
exa = data.frame(g1, g2)
rownames(exa) <- c('m1', 'm2', 'm3')
g1m = g1-mean(g1)
g2m = g2-mean(g2)
mexa = data.frame(g1m, g2m) # Mean-subtracted data.

# SVD
sr = svd(exa, 2, 2)
pc1 = sr$v[,1]

srm = svd(mexa, 2, 2)
pc1m = srm$v[,1]

# Graph results
par(mfrow=c(1,2))

# Graphs the mean-centered data with a line representing the first PCA.
mexar = rbind(mexa, pc1m)
plot(mexar, xlim=c(-2,2), ylim=c(-2, 2), main="First PCA of mean-centered data")
x <- c(mexar[4, 1], 0)
y <- c(mexar[4, 2], 0)
reg1 <- lm(y~x)
abline(reg1)

# Graphs the raw data with a line through the 1st PCA, which points to the mean.
nexa = rbind(exa, pc1)
plot(nexa, xlim=c(-1, 4), ylim=c(-1, 8), main="First PCA of non-mean-centered data")
x <- c(nexa[4, 1], 0)
y <- c(nexa[4, 2], 0)
reg1 <- lm(y~x)
abline(reg1)
dev.copy(jpeg, 'PCAplot.jpg')
dev.off()
