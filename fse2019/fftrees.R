cat("\014") 
options(max.print=1000000)
t1 <- Sys.time()


library("FFTrees")                # Load the package

# heart.fft <- FFTrees(formula = diagnosis ~ ., # Criterion
#                      data = heart.train,      # Training data
#                      main = "Heart Disease",  # Optional labels
#                      decision.labels = c("Low-Risk", "High-Risk"))
# 
# 
# inwords(heart.fft)   # Print a verbal description of the final FFT

THE_FILE  <- '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_WIK_FULL_DATASET.csv'
THE_DATA  <- read.csv(THE_FILE)

NEEDED_DATA    <- THE_DATA[, -c(1, 2)]
NEEDED_DATA$defect_status <- as.factor(NEEDED_DATA$defect_status)

# print(head(NEEDED_DATA))

DEFECTIVE_FFT <- FFTrees(formula = defect_status ~ ., # Criterion
                     data = THE_DATA,      # Training data
                     main = "DefectiveScript")


inwords(DEFECTIVE_FFT)




t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))