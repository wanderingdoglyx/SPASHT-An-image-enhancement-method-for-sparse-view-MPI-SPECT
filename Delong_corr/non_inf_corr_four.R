source("./Delong_test_corr.R")

args <- commandArgs(trailingOnly=TRUE)
csv_fname <- args[1]
result_csv_fname <- args[2]

# read csv filename
cat("reading csv file:", csv_fname,"\n")
data <- read.csv(csv_fname,  header = TRUE)

cat("Loading CTAC\n")
roc_CTAC <- get_auc(response = data$LABEL, var = data$CTAC)
cat("Loading CTLESS_CZT\n")
roc_CTLESS_CZT <- get_auc(response = data$LABEL, var = data$CTLESS_CZT)
cat("Loading CTLESS_NaI\n")
roc_CTLESS_NaI <- get_auc(response = data$LABEL, var = data$CTLESS_NaI)
cat("Loading NAC\n")
roc_NAC <- get_auc(response = data$LABEL, var = data$NAC)

num_cluster <- as.numeric(args[3])
margin <- 0.05*roc_CTAC$auc

auc_test_ctac_ctless_CZT <- auc.test.corr(roc_CTAC, roc_CTLESS_NaI, num_cluster, margin, alpha = 0.05)
auc_test_ctac_ctless_NaI <- auc.test.corr(roc_CTAC, roc_CTLESS_CZT, num_cluster, margin, alpha = 0.05)
auc_test_ctless_CZT_nac <- auc.test.corr(roc_CTLESS_NaI, roc_NAC, num_cluster, margin, alpha = 0.05)
auc_test_ctless_NaI_nac <- auc.test.corr(roc_CTLESS_CZT, roc_NAC, num_cluster, margin, alpha = 0.05)
auc_test_ctac_nac <- auc.test.corr(roc_CTAC, roc_NAC, num_cluster, margin, alpha = 0.05)

cat("CTAC AUC = ",roc_CTAC$auc,", [",auc_test_ctac_ctless_CZT$`Lower 1 CI`,",",auc_test_ctac_ctless_CZT$`Upper 1 CI`,"]\n")
cat("CTLESS_CZT AUC = ",roc_CTLESS_CZT$auc,", [",auc_test_ctac_ctless_CZT$`Lower 2 CI`,",",auc_test_ctac_ctless_CZT$`Upper 2 CI`,"]\n")
cat("CTLESS_NaI AUC = ",roc_CTLESS_NaI$auc,", [",auc_test_ctac_ctless_NaI$`Lower 2 CI`,",",auc_test_ctac_ctless_NaI$`Upper 2 CI`,"]\n")
cat("NAC AUC = ",roc_NAC$auc,", [",auc_test_ctac_nac$`Lower 2 CI`,",",auc_test_ctac_nac$`Upper 2 CI`,"]\n")

cat("CTAC vs NAC p = ",auc_test_ctac_nac$`Difference Pvalue`,"\n")
cat("CTLESS_CZT vs NAC p = ",auc_test_ctless_CZT_nac$`Difference Pvalue`,"\n")
cat("CTLESS_NaI vs NAC p = ",auc_test_ctless_NaI_nac$`Difference Pvalue`,"\n")

# save all relevent data to a csv file

header_names <- c(
    "AUC_CTLESS_CZT", "AUC_CI_UP_CTLESS_CZT", "AUC_CI_LOW_CTLESS_CZT",
    "AUC_CTLESS_NaI", "AUC_CI_UP_CTLESS_NaI", "AUC_CI_LOW_CTLESS_NaI",
    "AUC_NAC", "AUC_CI_UP_NAC", "AUC_CI_LOW_NAC",
    "AUC_CTAC", "AUC_CI_UP_CTAC", "AUC_CI_LOW_CTAC"
    )

fienac_values <- c(
    roc_CTLESS_CZT$auc, auc_test_ctac_ctless_CZT$`Upper 2 CI`, auc_test_ctac_ctless_CZT$`Lower 2 CI`,
    roc_CTLESS_NaI$auc, auc_test_ctac_ctless_NaI$`Upper 2 CI`, auc_test_ctac_ctless_NaI$`Lower 2 CI`,
    roc_NAC$auc, auc_test_ctac_nac$`Upper 2 CI`, auc_test_ctac_nac$`Lower 2 CI`,
    roc_CTAC$auc, auc_test_ctac_ctless_CZT$`Upper 1 CI`, auc_test_ctac_ctless_CZT$`Lower 1 CI`
)


res <- data.frame(header_names, fienac_values)
write.csv(res, result_csv_fname, row.names = FALSE)