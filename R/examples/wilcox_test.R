library(coin)
library(exactRankTests)


x <- seq(1, 10)
y <- seq(11, 21)
z <- seq(5, 15)

a <- seq(1, 21)
f <- factor(c(rep("x", 10), rep("y", 11)))

b <- c(x, z)
g <- factor(c(rep("x", 10), rep("z", 11)))

#wt_noties = wilcox.test(x, y)
#wtc_noties = wilcox_test(a~f, distribution="exact")

#print(wt_noties)
#print(wtc_noties)

wt_ties = wilcox.test(x, z)
wtc_ties = wilcox.test(b~g, distribution="exact", ties.method="average-scores")
print(wt_ties)
print(wtc_ties)
