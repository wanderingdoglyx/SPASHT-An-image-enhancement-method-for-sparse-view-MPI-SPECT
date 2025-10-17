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
cat("Loading NAC\n")
roc_NAC <- get_auc(response = data$LABEL, var = data$NAC)

num_cluster <- 27
margin <- 0.05*roc_CTAC$auc

auc_test_ctac_ctless <- auc.test.corr(roc_CTAC, roc_CTLESS, num_cluster, margin, alpha = 0.05)
auc_test_ctac_nac <- auc.test.corr(roc_CTAC, roc_NAC, num_cluster, margin, alpha = 0.05)
auc_test_ctless_nac <- auc.test.corr(roc_CTLESS, roc_NAC, num_cluster, margin, alpha = 0.05)

cat("CTAC AUC = ",roc_CTAC$auc,", [",auc_test_ctac_ctless$`Lower 1 CI`,",",auc_test_ctac_ctless$`Upper 1 CI`,"]\n")
cat("CTLESS AUC = ",roc_CTLESS$auc,", [",auc_test_ctac_ctless$`Lower 2 CI`,",",auc_test_ctac_ctless$`Upper 2 CI`,"]\n")
cat("NAC AUC = ",roc_NAC$auc,", [",auc_test_ctac_nac$`Lower 2 CI`,",",auc_test_ctac_nac$`Upper 2 CI`,"]\n")

cat("CTAC v.s. CTLESS:\n")
cat("Difference = ",auc_test_ctac_ctless$Difference,", [",auc_test_ctac_ctless$`One-Sided 95% Lower Limit`,",",auc_test_ctac_ctless$`One-Sided 95% upper Limit`,"]\n")
cat("p = ",auc_test_ctac_ctless$`Difference Pvalue`,"\n")
cat("noninf p = ",auc_test_ctac_ctless$`Non-Inferiority Pvalue`,"\n")

cat("CTAC v.s. NAC:\n")
cat("Difference = ",auc_test_ctac_nac$Difference,", [",auc_test_ctac_nac$`One-Sided 95% Lower Limit`,",",auc_test_ctac_nac$`One-Sided 95% upper Limit`,"]\n")
cat("p = ",auc_test_ctac_nac$`Difference Pvalue`,"\n")
cat("noninf p = ",auc_test_ctac_nac$`Non-Inferiority Pvalue`,"\n")

cat("CTLESS v.s. NAC:\n")
cat("Difference = ",auc_test_ctless_nac$Difference,", [",auc_test_ctless_nac$`One-Sided 95% Lower Limit`,",",auc_test_ctless_nac$`One-Sided 95% upper Limit`,"]\n")
cat("p = ",auc_test_ctless_nac$`Difference Pvalue`,"\n")

# save all relevent data to a csv file

header_names <- c(
    "AUC_CTLESS", "AUC_CI_UP_CTLESS", "AUC_CI_LOW_CTLESS",
    "AUC_CTAC", "AUC_CI_UP_CTAC", "AUC_CI_LOW_CTAC",
    "AUC_NAC", "AUC_CI_UP_NAC", "AUC_CI_LOW_NAC",
    "CTLESS_VS_CTAC_DIFF","CTLESS_VS_CTAC_P_VAL","CTLESS_VS_CTAC_noninf_P_VAL", "CTLESS_VS_CTAC_CI_UP", "CTLESS_VS_CTAC_CI_LOW",
    "CTAC_VS_NAC_DIFF","CTAC_VS_NAC_P_VAL","CTAC_VS_NAC_noninf_P_VAL", "CTAC_VS_NAC_CI_UP", "CTAC_VS_NAC_CI_LOW"
)

fienac_values <- c(
    roc_CTLESS$auc, auc_test_ctac_ctless$`Upper 2 CI`, auc_test_ctac_ctless$`Lower 2 CI`,
    roc_CTAC$auc, auc_test_ctac_ctless$`Upper 1 CI`, auc_test_ctac_ctless$`Lower 1 CI`,
    roc_NAC$auc, auc_test_ctac_nac$`Upper 2 CI`, auc_test_ctac_nac$`Lower 2 CI`,
    auc_test_ctac_ctless$Difference, auc_test_ctac_ctless$`Difference Pvalue`, auc_test_ctac_ctless$`Non-Inferiority Pvalue`, auc_test_ctac_ctless$`One-Sided 95% Lower Limit`, auc_test_ctac_ctless$`One-Sided 95% upper Limit`,
    auc_test_ctac_nac$Difference, auc_test_ctac_nac$`Difference Pvalue`, auc_test_ctac_nac$`Non-Inferiority Pvalue`, auc_test_ctac_nac$`One-Sided 95% Lower Limit`, auc_test_ctac_nac$`One-Sided 95% upper Limit`
)


res <- data.frame(header_names, fienac_values)
write.csv(res, result_csv_fname, row.names = FALSE)