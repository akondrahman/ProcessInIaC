'''
Akond Rahman 
Feb 22 
Merge dataframes : process, size, age 
'''
import pandas as pd 
import numpy as np 

if __name__=='__main__':
#    process_dataset_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/MIR_FULL_DATASET.csv'
#    size_dataset_file    = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/SIZE_MIR.csv' 
#    age_dataset_file     = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/AGE_MIR.csv'
#    output_file          = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/MIR_EMSE2020.csv'

#    process_dataset_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/MOZ_FULL_DATASET.csv'
#    size_dataset_file    = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/SIZE_MOZ.csv' 
#    age_dataset_file     = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/AGE_MOZ.csv'
#    output_file          = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/MOZ_EMSE2020.csv'

#    process_dataset_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/OST_FULL_DATASET.csv'
#    size_dataset_file    = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/SIZE_OST.csv' 
#    age_dataset_file     = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/AGE_OST.csv'
#    output_file          = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/OST_EMSE2020.csv'

#    process_dataset_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/WIK_FULL_DATASET.csv'
#    size_dataset_file    = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/SIZE_WIK.csv' 
#    age_dataset_file     = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/AGE_WIK.csv'
#    output_file          = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/iac-ncsu/ProcessInIaC/EMSE_JRNL_WORK_2020/WIK_EMSE2020.csv'

   process_df = pd.read_csv(process_dataset_file)
   size_df    = pd.read_csv(size_dataset_file)
   age_df     = pd.read_csv(age_dataset_file)
   temp_df    = pd.merge(process_df, size_df, on='file_')
   full_df    = pd.merge(temp_df, age_df , on ='file_') 

   full_df    = full_df.drop(columns=['org', 'org_x', 'ADD_PER_COM', 'DEL_PER_COM', 'defect_status_x', 'org_y', 'defect_status_y'])
   print(full_df.shape) 
   print(full_df.head())
   print(full_df.columns) 
   full_df.to_csv(output_file, index=False, encoding='utf-8')       
