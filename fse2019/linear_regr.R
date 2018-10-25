cat("\014") 
options(max.print=1000000)
library(Hmisc)
t1 <- Sys.time()

# THE_FILE  <- '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/WIK_DEFECT_COUNT_DATASET.csv'
# THE_FILE  <- '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/OST_DEFECT_COUNT_DATASET.csv'
# THE_FILE  <- '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/MOZ_DEFECT_COUNT_DATASET.csv'
# THE_FILE  <- '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/MIR_DEFECT_COUNT_DATASET.csv'
THE_DATA  <- read.csv(THE_FILE)

NEEDED_DATA    <- THE_DATA[, -c(1, 2)]

# print(head(NEEDED_DATA))
rcorr(as.matrix(NEEDED_DATA), type = "spearman") 
linearMod    <- lm(defect_status ~ ADD_PER_COM + DEL_PER_COM + TOT_PER_COM + DEVS + MINORS + OWNER_LINES + SCATERNESS + DEV_MET + COLA_MET,
                data=NEEDED_DATA)  # build linear regression model on full data
modelSummary <- summary(linearMod)
print(modelSummary)




t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))