cat("\014") 
options(max.print=1000000)
library(Hmisc)
t1 <- Sys.time()

THE_FILE  <- '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/WIK_FULL_DATASET.csv'
THE_DATA  <- read.csv(THE_FILE)

NEEDED_DATA    <- THE_DATA[, -c(1, 2)]
NEEDED_DATA$defect_status <- as.factor(NEEDED_DATA$defect_status)

#print(head(NEEDED_DATA))

logiReg_combined_model <-  glm(defect_status ~ ., family=binomial(link='logit'), data=NEEDED_DATA)
print(summary(logiReg_combined_model))
anova_ful_model <- anova(logiReg_combined_model, test="Chisq")
print(anova_ful_model)

t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))