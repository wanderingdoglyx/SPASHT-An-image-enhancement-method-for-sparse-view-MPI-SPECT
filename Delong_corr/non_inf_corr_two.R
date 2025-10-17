source("./Delong_test_corr.R")

args <- commandArgs(trailingOnly=TRUE)
csv_fname <- args[1]
result_csv_fname <- args[2]

# read csv filename
cat("reading csv file:", csv_fname,"\n")
data <- read.csv(csv_fname,  header = TRUE)

cat("Loading CTAC\n")
roc_CTAC <- get_auc(response = data$LABEL, var = data$CTAC)
cat("Loading CTLESS\n")
roc_CTLESS <- get_auc(response = data$LABEL, var = data$CTLESS)

num_cluster <- as.numeric(args[3])
margin <- 0.05*roc_CTAC$auc

auc_test_ctac_ctless <- auc.test.corr(roc_CTAC, roc_CTLESS, num_cluster, margin, alpha = 0.05)

cat("CTAC AUC = ",roc_CTAC$auc,", [",auc_test_ctac_ctless$`Lower 1 CI`,",",auc_test_ctac_ctless$`Upper 1 CI`,"]\n")
cat("CTLESS AUC = ",roc_CTLESS$auc,", [",auc_test_ctac_ctless$`Lower 2 CI`,",",auc_test_ctac_ctless$`Upper 2 CI`,"]\n")

# save all relevent data to a csv file

header_names <- c(
    "AUC_CTLESS", "AUC_CI_UP_CTLESS", "AUC_CI_LOW_CTLESS",
    "AUC_CTAC", "AUC_CI_UP_CTAC", "AUC_CI_LOW_CTAC",
    "CTLESS_VS_CTAC_DIFF","CTLESS_VS_CTAC_P_VAL"
    )

fienac_values <- c(
    roc_CTLESS$auc, auc_test_ctac_ctless$`Upper 2 CI`, auc_test_ctac_ctless$`Lower 2 CI`,
    roc_CTAC$auc, auc_test_ctac_ctless$`Upper 1 CI`, auc_test_ctac_ctless$`Lower 1 CI`,
    auc_test_ctac_ctless$Difference, auc_test_ctac_ctless$`Difference Pvalue`
)


res <- data.frame(header_names, fienac_values)
write.csv(res, result_csv_fname, row.names = FALSE)