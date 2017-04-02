library(ggplot2)
cat("\014") 
options(max.print=1000000)

t1 <- Sys.time()

file_to_read   <- "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/PRELIM_MOZILLA.csv"
pred_dataset   <- read.csv(file_to_read)
defects        <- as.factor(pred_dataset$defect_status)
thePredictors  <- colnames(pred_dataset)

sctr_plot_           <- ggplot(pred_dataset, aes(x=factor(defects), y=SCTR)) + geom_boxplot(aes(fill=defects))
sctr_plot_

t2 <- Sys.time()
print(t2 - t1)  # 
rm(list = setdiff(ls(), lsf.str()))