cat("\014") 
options(max.print=1000000)
t1 <- Sys.time()

# DS_FILE   <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/MIR_EMSE2020.csv"
# DS_FILE   <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/MOZ_EMSE2020.csv"
# DS_FILE   <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/OST_EMSE2020.csv"
# DS_FILE   <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/WIK_EMSE2020.csv"

DATAFRAME <- read.csv(DS_FILE)
DATAFRAME <- DATAFRAME[ -c(1) ]
print(head(DATAFRAME))

print("======================================================================")
print("LINEAR MODEL START ... ")

model_ <- lm(defect_status ~ LOC  + DEVS, data=DATAFRAME)
summary(model_) 
print("**********")
model_ <- lm(defect_status ~ LOC  + MINORS, data=DATAFRAME)
summary(model_) 
print("**********")
print("**********")
model_ <- lm(defect_status ~ LOC  + OWNER_LINES, data=DATAFRAME)
summary(model_) 
print("**********")
print("**********")
model_ <- lm(defect_status ~ LOC  + DEV_MET, data=DATAFRAME)
summary(model_) 
print("**********")
print("**********")
model_ <- lm(defect_status ~ LOC  + COLA_MET, data=DATAFRAME)
summary(model_) 
print("**********")
print("**********")
model_ <- lm(defect_status ~ LOC  + TOT_PER_COM, data=DATAFRAME)
summary(model_) 
print("**********")
print("**********")
model_ <- lm(defect_status ~ LOC  + SCATERNESS, data=DATAFRAME)
summary(model_) 
print("**********")

print("LINEAR MODEL END ... ")
print("======================================================================")


print("======================================================================")
print("LOGISTIC MODEL START ... ")

DATAFRAME$defect_status <- as.factor(DATAFRAME$defect_status) 
logit_model_ <- glm(defect_status ~ LOC  + DEVS, data=DATAFRAME, family = "binomial")
summary(logit_model_) 
print("**********")
logit_model_ <- glm(defect_status ~ LOC  + MINORS, data=DATAFRAME, family = "binomial")
summary(logit_model_) 
print("**********")
print("**********")
logit_model_ <- glm(defect_status ~ LOC  + OWNER_LINES, data=DATAFRAME, family = "binomial")
summary(logit_model_) 
print("**********")
print("**********")
logit_model_ <- glm(defect_status ~ LOC  + DEV_MET, data=DATAFRAME, family = "binomial")
summary(logit_model_) 
print("**********")
print("**********")
logit_model_ <- glm(defect_status ~ LOC  + COLA_MET, data=DATAFRAME, family = "binomial")
summary(logit_model_) 
print("**********")

print("**********")
logit_model_ <- glm(defect_status ~ LOC  + TOT_PER_COM, data=DATAFRAME, family = "binomial")
summary(logit_model_) 
print("**********")

print("**********")
logit_model_ <- glm(defect_status ~ LOC  + SCATERNESS, data=DATAFRAME, family = "binomial")
summary(logit_model_) 
print("**********")

print("LOGISTIC MODEL END ... ")
print("======================================================================")


t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))