# Helper functions
h_get_u_statistic <- function(x, y) {
  if (x < y) {
    return(1)
  }
  if (x == y) {
    return(0.5)
  }
  if (x > y) {
    return(0)
  }
}

h_auc_v10_v01 <- function(n1, n0, v1, v0) {
  v10 <- NULL
  v01 <- NULL

  # Mann-Whitney U statistic
  auc <- sum(sapply(v1, function(x) {
    sapply(v0, function(y) {h_get_u_statistic(x, y)})
  })) / (n1 * n0)

  for (i in 1:n1) {
    v10 <- c(v10, sum(
      sapply(v0, function(y) {h_get_u_statistic(v1[i], y)})
    ) / n0)
  }

  for (i in 1:n0) {
    v01 <- c(v01, sum(
      sapply(v1, function(x) {h_get_u_statistic(x, v0[i])})
    ) / n1)
  }

  return(list(auc = auc, v10 = v10, v01 = v01))
}

# To get the auc and corresponding intermediate parameters `v10` and `v01`
get_auc <- function(response, var) {
  dat <- cbind(response, var)
  n0 <- sum(response == 0, na.rm = TRUE)
  n1 <- sum(response == 1, na.rm = TRUE)
  var0 <- var[response == 0]
  var1 <- var[response == 1]

  c(
    list(n1 = n1, n0 = n0, var1 = var1, var0 = var0),
    h_auc_v10_v01(n1 = n1, n0 = n0, v1 = var1, v0 = var0)
  )
}

# The main program.
auc.test <- function(mroc1, mroc2, margin, alpha = 0.05) {
  mod1 <- mroc1
  mod2 <- mroc2

  n1 <- mod1$n1
  n0 <- mod1$n0
  auc1 <- mod1$auc
  auc2 <- mod2$auc

  s10_11 <- sum((mod1$v10 - auc1)^2) / (n1 - 1)
  s10_22 <- sum((mod2$v10 - auc2)^2) / (n1 - 1)
  s10_12 <- sum((mod1$v10 - auc1) * (mod2$v10 - auc2)) / (n1 - 1)

  s01_11 <- sum((mod1$v01 - auc1)^2) / (n0 - 1)
  s01_22 <- sum((mod2$v01 - auc2)^2) / (n0 - 1)
  s01_12 <- sum((mod1$v01 - auc1) * (mod2$v01 - auc2)) / (n0 - 1)

  mod1_var <- s10_11/n1 + s01_11/n0
  mod2_var <- s10_22/n1 + s01_22/n0

  cov <- s10_12 / n1 + s01_12 / n0
  

  variance <- (s10_11 + s10_22 - 2 * s10_12) / n1 + (s01_11 + s01_22 - 2 * s01_12) / n0
  
  auc_diff <- auc1 - auc2
  z <- (auc_diff - margin) / sqrt(variance)
  p <- 1 - pnorm(z)
  lower_limit <- auc_diff - (qnorm(1 - alpha) * sqrt(variance))
  list(Difference = auc_diff, `Non-Inferiority Pvalue` = p, `One-Sided 95% Lower Limit` = lower_limit)
}

auc.test.corr <- function(mroc1, mroc2, num_cluster, margin, alpha = 0.05) {
  # mroc has test statistics in the shape of [cluster1{1,2,3,...,N_patient}, cluster2{1,2,3,...,N_patient}, ...]
  mod1 <- mroc1
  mod2 <- mroc2

  n1 <- mod1$n1
  n0 <- mod1$n0
  auc1 <- mod1$auc
  auc2 <- mod2$auc

  mod1_v10 <- as.numeric(unlist(lapply(split(mod1$v10, rep(1:ceiling(length(mod1$v10)*num_cluster/n1), each = n1/num_cluster, length.out = length(mod1$v10))),sum)))
  mod1_v01 <- as.numeric(unlist(lapply(split(mod1$v01, rep(1:ceiling(length(mod1$v01)*num_cluster/n0), each = n0/num_cluster, length.out = length(mod1$v01))),sum)))
  mod2_v10 <- as.numeric(unlist(lapply(split(mod2$v10, rep(1:ceiling(length(mod2$v10)*num_cluster/n1), each = n1/num_cluster, length.out = length(mod2$v10))),sum)))
  mod2_v01 <- as.numeric(unlist(lapply(split(mod2$v01, rep(1:ceiling(length(mod2$v01)*num_cluster/n0), each = n0/num_cluster, length.out = length(mod2$v01))),sum)))
  
  I01 <- length(mod1_v01)
  I10 <- length(mod1_v10)

  I <- num_cluster

  s10_11 <- sum((mod1_v10-mean(mod1_v10))^2) * I10 /(I10-1) / n1
  s01_11 <- sum((mod1_v01-mean(mod1_v01))^2) * I01 /(I01-1) / n0
  s11_11 <- sum((mod1_v01-mean(mod1_v01)) * (mod1_v10-mean(mod1_v10))) * I /(I-1)
  
  s10_22 <- sum((mod2_v10-mean(mod2_v10))^2) * I10 /(I10-1) / n1
  s01_22 <- sum((mod2_v01-mean(mod2_v01))^2) * I01 /(I01-1) / n0
  s11_22 <- sum((mod2_v01-mean(mod2_v01)) * (mod2_v10-mean(mod2_v10))) * I /(I-1)

  mod1_var <- s10_11/n1 + s01_11/n0 + s11_11*2/n1/n0
  mod2_var <- s10_22/n1 + s01_22/n0 + s11_22*2/n1/n0

  s10_12 <- sum((mod1_v10-mean(mod1_v10)) * (mod2_v10-mean(mod2_v10))) * I10 /(I10-1) / n1
  s01_12 <- sum((mod1_v01-mean(mod1_v01)) * (mod2_v01-mean(mod2_v01))) * I01 /(I01-1) / n0

  s11_12 <- sum((mod1_v10-mean(mod1_v10)) * (mod2_v01-mean(mod2_v01))) * I /(I-1)
  s11_21 <- sum((mod2_v10-mean(mod2_v10)) * (mod1_v01-mean(mod1_v01))) * I /(I-1)

  cov <- s10_12/n1 + s01_12/n0 + s11_12/n1/n0 + s11_21/n1/n0

  variance <- mod1_var + mod2_var - 2 * cov
  
  auc_diff <- auc2 - auc1
  z <- (auc_diff+margin) / sqrt(variance)
  p <- 1 - pnorm(z)
  z_diff <- abs(auc_diff) / sqrt(variance)
  p_diff <- 1 - pnorm(abs(z_diff))
  lower_limit <- auc_diff - (qnorm(1 - alpha) * sqrt(variance))
  upper_limit <- auc_diff + (qnorm(1 - alpha) * sqrt(variance))
  

  mod1_lower_CI <- mod1$auc - (qnorm(1 - alpha) * sqrt(mod1_var))
  mod1_upper_CI <- mod1$auc + (qnorm(1 - alpha) * sqrt(mod1_var))

  mod2_lower_CI <- mod2$auc - (qnorm(1 - alpha) * sqrt(mod2_var))
  mod2_upper_CI <- mod2$auc + (qnorm(1 - alpha) * sqrt(mod2_var))

  list(Difference = auc_diff, `Difference Pvalue` = p_diff,`Non-Inferiority Pvalue` = p, `One-Sided 95% Lower Limit` = lower_limit, `One-Sided 95% upper Limit` = upper_limit, AUC1=mod1$auc, `Lower 1 CI` = mod1_lower_CI, `Upper 1 CI` = mod1_upper_CI, AUC2=mod2$auc, `Lower 2 CI` = mod2_lower_CI, `Upper 2 CI` = mod2_upper_CI)
}