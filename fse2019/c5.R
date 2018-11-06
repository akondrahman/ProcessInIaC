cat("\014") 
options(max.print=1000000)
t1 <- Sys.time()


library(ggplot2)

THE_FILE  <- '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_WIK_FULL_DATASET.csv'
THE_DATA  <- read.csv(THE_FILE)

NEEDED_DATA    <- THE_DATA[, -c(1, 2)]
NEEDED_DATA$defect_status <- as.factor(NEEDED_DATA$defect_status)

mdl<- train(x = NEEDED_DATA[, -10], y = NEEDED_DATA$defect_status,  method= 'rfRules', verbose=FALSE)

mdl

t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))