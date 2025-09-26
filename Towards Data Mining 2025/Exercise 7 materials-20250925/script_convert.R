# For PCA dataset
load("data_PCA_E7.RData")
write.csv(X, file = "data_PCA_E7.csv", row.names = FALSE)

# For NN/PCANN dataset
load("data_NN_E7.RData")
write.csv(X, file = "data_NN_E7.csv", row.names = FALSE)
write.csv(y, file = "target_NN_E7.csv", row.names = FALSE)
