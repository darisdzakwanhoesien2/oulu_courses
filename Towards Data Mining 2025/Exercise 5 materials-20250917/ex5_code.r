# MISSING DATA

# 1
# use the right separator characters
iris_data <- read.table("iris.csv", header = TRUE, sep = ";", dec = ",")

# 2
plot(iris_data$Petal.Length, iris_data$Petal.Width)

# 3
lm_fit <- lm(Petal.Width ~ Petal.Length, data = iris_data)
summary(lm_fit)

# 4
abline(lm_fit)

# 5
mean(iris_data$Petal.Length)
mean(iris_data$Petal.Width)
summary(iris_data)

# 6
getOption("na.action")

# 7
sum(complete.cases(iris_data))

# 8
# this will save the values and print out the result
(mean_pl <- mean(iris_data$Petal.Length, na.rm = TRUE))
(mean_pw <- mean(iris_data$Petal.Width, na.rm = TRUE))

# 9
cov(iris_data$Petal.Length, iris_data$Petal.Width)
cov(iris_data$Petal.Length, iris_data$Petal.Width, use = "complete.obs")
cov(iris_data$Petal.Length, iris_data$Petal.Width, use = "pairwise.complete.obs")

# 10 b.
# first make a copy of the original data frame
mean_imputation <- iris_data
# find the indexes of the missing values
idx_pw_missing <- is.na(mean_imputation$Petal.Width)
# then impute the mean where data is missing
mean_imputation$Petal.Width[idx_pw_missing] <- mean_pw
# now calculate the mean
mean(mean_imputation$Petal.Width)

# do the same for Petal.Length

# 10 c.
# make a copy of the original data frame
strat_mean_imputation <- iris_data
# calculate the mean of Petal.Width for only setosas
mean_pw_setosa <- mean(subset(iris_data, Species == "setosa")$Petal.Width, na.rm = TRUE)
# impute, right indexes are found when both conditions are true
strat_mean_imputation$Petal.Width[is.na(strat_mean_imputation$Petal.Width) & strat_mean_imputation$Species == "setosa"] <- mean_pw_setosa
# do the same for virginica (no missing values in versicolor). Finally:
mean(strat_mean_imputation$Petal.Width)

# do the same for Petal.length

# 10 d.
# make a copy of the original data frame
regr_imputation <- iris_data
# impute the values with regression
regr_imputation$Petal.Width[is.na(regr_imputation$Petal.Width)] <- predict(lm_fit, subset(regr_imputation, is.na(Petal.Width)))
# calculate the mean
mean(regr_imputation$Petal.Width)

# do the same for Petal.length
# note that we need to build another regression model to impute the missing Petal.Length values


# 11
# make a copy of the original data frame
iris_ml <- iris_data

# load the needed package, install if not already installed
if (!require(mclust)) {
    install.packages("mclust")
    require(mclust)
}
# only complete observations for building the density model
trainingdata <- iris_data[complete.cases(iris_data),]
# do not use Species column
dens <- densityMclust(trainingdata[,c(1,2)], G = 3)
summary(dens, parameters = TRUE)
plot(dens, what = "density", data = trainingdata[,c(1,2)])
plot(dens, what = "density", type = "persp")

# ML estimate of width when length is known, in this case for row #18
widths <- seq(0,4,0.1)
lengths <- rep(iris_data$Petal.Length[18], length(widths))
ml_est <- seq(0,4,0.1)[which.max(predict(dens, data.frame(Petal.Length = lengths, Petal.Width = widths)))]
iris_ml$Petal.Width[18] <- ml_est

# repeat for all missing Petal.Width values

# repeat for all missing Petal.Length values (ML estimate of length when width is known)


# 12
# load the needed package, install if not already installed
if (!require(mice)) {
    install.packages("mice")
    require(mice)
}
imp <- mice(iris_data, m = 10, print = FALSE, seed = 121018)

# we can fit the regression model on MI data:
fit_mi <- with(imp, lm(Petal.Width ~ Petal.Length))
est <- pool(fit_mi)
summary(est)
# intercept = est$qbar[[1]], slope = est$qbar[[2]]
# pw <- est$qbar[[1]] + pl * est$qbar[[2]]

# pooled estimates of the means
m <- imp$m
Q <- rep(NA, m)
U <- rep(NA, m)
for (i in 1:m) {
   Q[i] <- mean(complete(imp, i)$Petal.Width)
   U[i] <- var(complete(imp, i)$Petal.Width) / nrow(iris_data)  # (standard error of estimate)^2
}
est_pw <- pool.scalar(Q, U, n = nrow(iris_data), k = 1)  # Barnard-Rubin 1999

est_pw$qbar # this is the pooled estimate for Petal.Width

# do the same for Petal.length
for (i in 1:m) {
    Q[i] <- mean(complete(imp, i)$Petal.Length)
    U[i] <- var(complete(imp, i)$Petal.Length) / nrow(iris_data)  # (standard error of estimate)^2
}
est_pl <- pool.scalar(Q, U, n = nrow(iris_data), k = 1)  # Barnard-Rubin 1999

est_pl$qbar # this is the pooled estimate for Petal.Length