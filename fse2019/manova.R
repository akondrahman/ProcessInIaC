cat("\014") 
options(max.print=1000000)
t1 <- Sys.time()

## log reff: https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/log
## normal transformation: https://www.datanovia.com/en/lessons/transform-data-to-normal-distribution-in-r/ 
## MANOVA: http://www.sthda.com/english/wiki/manova-test-in-r-multivariate-analysis-of-variance


# DS_FILE   <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/MIR_EMSE2020.csv"
# DS_FILE   <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/MOZ_EMSE2020.csv"
# DS_FILE   <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/OST_EMSE2020.csv"
# DS_FILE   <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/WIK_EMSE2020.csv"

DATAFRAME <- read.csv(DS_FILE)
DATAFRAME <- DATAFRAME[ -c(1) ]
# print(head(DATAFRAME))




print("======================================================================")
print(DS_FILE)
print("MULTI WAY ANOVA START ... ")

DATAFRAME$defect_status <- as.factor(DATAFRAME$defect_status)
DATAFRAME$LOC           <- log1p(DATAFRAME$LOC)
DATAFRAME$AGE           <- log1p(DATAFRAME$AGE)
DATAFRAME$MINORS        <- log1p(DATAFRAME$MINORS)
DATAFRAME$OWNER_LINES   <- log1p(DATAFRAME$OWNER_LINES)
DATAFRAME$DEV_MET       <- log1p(DATAFRAME$DEV_MET)
DATAFRAME$COLA_MET      <- log1p(DATAFRAME$COLA_MET)
DATAFRAME$TOT_PER_COM   <- log1p(DATAFRAME$TOT_PER_COM)
DATAFRAME$SCATERNESS    <- log1p(DATAFRAME$SCATERNESS)
DATAFRAME$DEVS          <- log1p(DATAFRAME$DEVS)

print("**********TRANSFORMATION START********")
print(head(DATAFRAME))
print("**********TRANSFORMATION END**********")

print("**********")
result_anova <- manova( cbind(LOC, AGE, DEVS) ~ defect_status , data = DATAFRAME)
# summary(result_anova) 
summary.aov(result_anova)
print("**********")


print("**********")
result_anova <- manova( cbind(LOC, AGE, MINORS) ~ defect_status , data = DATAFRAME)
# summary(result_anova) 
summary.aov(result_anova)
print("**********")

print("**********")
result_anova <- manova( cbind(LOC, AGE, OWNER_LINES) ~ defect_status , data = DATAFRAME)
# summary(result_anova) 
summary.aov(result_anova)
print("**********")
print("**********")
result_anova <- manova( cbind(LOC, AGE, DEV_MET) ~ defect_status , data = DATAFRAME)
# summary(result_anova) 
summary.aov(result_anova)
print("**********")

print("**********")
result_anova <- manova( cbind(LOC, AGE, COLA_MET) ~ defect_status , data = DATAFRAME)
# summary(result_anova) 
summary.aov(result_anova)
print("**********")

print("**********")
result_anova <- manova( cbind(LOC, AGE, TOT_PER_COM) ~ defect_status , data = DATAFRAME)
# summary(result_anova) 
summary.aov(result_anova)
print("**********")

print("**********")
result_anova <- manova( cbind(LOC, AGE, SCATERNESS) ~ defect_status , data = DATAFRAME)
# summary(result_anova) 
summary.aov(result_anova)
print("**********")

print("MULTI WAY ANOVA END ... ")
print("======================================================================")


t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))