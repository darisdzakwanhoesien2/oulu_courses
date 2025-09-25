# NOISY DATA

# 1
noisy <- read.csv("iris_noisy.csv", header = TRUE, sep = ";", dec = ",")

# 2
# load the package e1071, install it if necessary
if (!require(e1071)) {
    install.packages("e1071")
    require(e1071)
}

# 3
fit_noisy <- naiveBayes(as.factor(Species ) ~., data = noisy)
pred_noisy <- predict(fit_noisy, noisy)
# confusion matrix
table(pred_noisy, noisy$Species)

# 4
# load iris_complete from iris_complete.csv
iris_complete <- read.csv("iris_complete.csv", header = TRUE, sep = ";", dec = ",")

# fit the model, predict, and compare the confusion matrix with the one above 


# 5 check the summary() of both noisy and iris_complete


# 6
# e.g.:
# you can plot two figures in the same plot, side by side (one row, two columns)
op <- par(mfrow = c(1,2))
# try boxplot for the subsets for both data sets
# for setosa it looks like this:
boxplot(subset(noisy, Species == "setosa", select = c("Petal.Length", "Petal.Width")), ylim = c(0,5))
boxplot(subset(iris_complete, Species == "setosa", select = c("Petal.Length", "Petal.Width")), ylim = c(0,5))
# reset the plot parameters when done
par(op)

# OUTLIERS 

# 7
outlier <- subset(noisy, Species == "setosa")

# 8
if (!require(mclust)) {
    install.packages("mclust")
    require(mclust)
}
dens <- densityMclust(outlier[,c(1,2)], G = 2)
# here are the cluster means
dens$parameters$mean

# 9
# calculate the distances
dists <- rep(NA, nrow(outlier))

for (i in 1:nrow(outlier)) {
    dists[i] <- sqrt((outlier$Petal.Length[i] - dens$parameters$mean[[1,1]])^2 + (outlier$Petal.Width[i] - dens$parameters$mean[[2,1]])^2)
}

# calculate and report the mean distance of normal data points
# and the distance of the one outlier


# SATURATED SIGNAL

# 10
saturated <- read.table("saturated.csv", sep = ";", dec = ",", header = TRUE)

# 11
plot(saturated$Time, saturated$Acc, type = "l")

# 12
# what are the minimum and maximum values of the signal (Acc)?

# 13
# min values
nrow(subset(saturated, Acc == min(saturated$Acc))) / nrow(saturated)

# do the same math for max values

# 14
r <- rle(saturated$Acc)

# value repeated in the longest run
r$values[which.max(r$lengths)]

# by checking the rle output, we find out that the longest run of value less than the saturation point is three consecutive values
max(unique(r$lengths[r$values < max(r$values)]))
r$values[r$lengths == 3]

# number of runs of length >= 4
