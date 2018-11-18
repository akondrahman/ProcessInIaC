'''
Akond Rahman
April 10, 2017
main file for prediction model
'''

from sklearn.ensemble import ExtraTreesClassifier
from sklearn import decomposition
import process_metric_utility , numpy as np , pandas as pd, sklearn_utility
glimpseIndex=10

def getPCAInsights(pcaParamObj, no_of_pca_comp_to_see):
    print '+'*25
    print 'PCA metric importance zone  ...'
    print '+'*25
    for comp_index in xrange(no_of_pca_comp_to_see):
        all_metric_value_in_one_component =  np.abs(pcaParamObj.components_[comp_index])
        non_zero_metric_cnt = len([x_ for x_ in all_metric_value_in_one_component if x_ > 0])
        print 'Number of non-zero metrics:{}, of {}'.format(non_zero_metric_cnt, len(all_metric_value_in_one_component))
        print '$'*15
        sorted_all_metric_index_in_one_component = all_metric_value_in_one_component.argsort()[::-1]
        for met_index in sorted_all_metric_index_in_one_component:
            print 'Metric index:{}, metric score:{}'.format(met_index, all_metric_value_in_one_component[met_index])
            print '~'*10
        print '$'*15
    print "+"*25


print "Started at:", process_metric_utility.giveTimeStamp()
print "-"*50
'''
  first is mozilla then openstack then wiki
'''
# BEST-FIRST FEATURE SUBSET: MUCH BETTER THAN PCA::: V1
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MOZILLA_ONLY_COMM_DEV_SUMCHNG.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OPENSTACK_ONLY_COMM_DELPERLOC_MINOR.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/WIKIMEDIA_ONLYL_COMMIT_AGE.csv"

# LR FOR MOZILLA DROPS A TINY BIT, RF FOR OST IMPORVES A LOT!!!: MUCH BETTER THAN PCA ::: V2
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MOZILLA_ONLY_AGE_DELPERLOC_SUMCHNG_MINOR.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OPENSTACK_ONLY_COMM_ADDPERLOC_SUMCHNG_AVGCHNG.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/WIKIMEDIA_ONLY_COMM_DELPERLOC.csv"

# WITH MULTI TAKING DATA:  PCA TO BE APPLIED
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MultiTasking_MOZ_FULL_PROCESS_DATASET.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MultiTasking_OPENSTACK_PROCESS_DATASET.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MultiTasking_WIKI_FULL_PROCESS_DATASET.csv"


# WITH MULTI TAKING DATA: BFS APPLIED
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/BFS_MT_MOZ_PROCESS_DATASET.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/BFS_MT_OST_PROCESS_DATASET.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/BFS_MT_WIKI_PROCESS_DATASET.csv"


# NEW DATA NO BFS
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_MIRANTIS_FULL_PROCESS_DATASET.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_REDHAT_FULL_PROCESS_DATASET.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_CISCO_FULL_PROCESS_DATASET.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_CERN_FULL_PROCESS_DATASET.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_BASTION_FULL_PROCESS_DATASET.csv'

# FINA DATASETS : PCA: NO BFS
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_BASTION_FULL_PROCESS_DATASET.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_CISCO_FULL_PROCESS_DATASET.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_MIRANTIS_FULL_PROCESS_DATASET.csv'
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MultiTasking_MOZ_FULL_PROCESS_DATASET.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MultiTasking_OPENSTACK_PROCESS_DATASET.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MultiTasking_WIKI_FULL_PROCESS_DATASET.csv"

# dataset_file = "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/COMMIT_WIKIMEDIA_DS.csv"


# ACTINABLE ANTI_PATTERN DATASETS : PCA: NO BFS
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/nosize/BAS.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/NO-COMM-AGE/CIS.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/NO-COMM-AGE/MIR.csv'
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/NO-COMM-AGE/MOZ.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/NO-COMM-AGE/OST.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/NO-COMM-AGE/WIK.csv"

'''
ICSE 2019 , TSE
'''
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/MIR_FUL_PRO.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/MOZ_FUL_PRO.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/OST_FUL_PRO.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/WIK_FUL_PRO.csv'

# dataset_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/JUST_SIZE/MIR.csv'
# dataset_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/JUST_SIZE/MOZ.csv'
# dataset_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/JUST_SIZE/OST.csv'
# dataset_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/JUST_SIZE/WIK.csv'

'''
FSE 2019 
'''
dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/V1_WIK_FULL_DATASET.csv'

print "The dataset is:", dataset_file
print "-"*50
full_dataset_from_csv = process_metric_utility.getDatasetFromCSV(dataset_file)
full_rows, full_cols = np.shape(full_dataset_from_csv)
print "Total number of columns", full_cols
## we will skip the first column, as it has file names
feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip
# ###feature_cols = full_cols - 2  ## the last column is null, second last couln is defect status, so two column to skip
all_features = full_dataset_from_csv[:, 2:feature_cols]
print "Glimpse at features (11th entry in dataset): \n", all_features[glimpseIndex]
print "-"*50

dataset_for_labels = process_metric_utility.getDatasetFromCSV(dataset_file)  ## unlike phase-1, the labels are '1' and '0', so need to take input as str
label_cols = full_cols - 1 ### FOR FIEL LEVEL
# ### label_cols = full_cols - 2  ### FOR COMMTI LEVEL
all_labels  =  dataset_for_labels[:, label_cols]
print "Glimpse at  labels (11th entry in dataset):", all_labels[glimpseIndex]
print "-"*50

defected_file_count     = len([x_ for x_ in all_labels if x_==1.0])
non_defected_file_count = len([x_ for x_ in all_labels if x_==0.0])
print "No of. defects={}, non-defects={}".format(defected_file_count, non_defected_file_count)
print "-"*50

'''
lets transform all the features via log transformation
'''
log_transformed_features = process_metric_utility.createLogTransformedFeatures(all_features)
print "Selected (log-transformed) feature dataset size:", np.shape(log_transformed_features)
print "Glimpse at (log-transformed) selected features(10th entry in label list): \n", log_transformed_features[glimpseIndex]
print "-"*50
feature_input_for_pca = log_transformed_features
# selected_features = log_transformed_features
'''
PCA ZONE
'''
# pca_comp = 10 ###  must be less than or equal to no of features
pca_comp = 1 ###  for size
pcaObj = decomposition.PCA(n_components=pca_comp)
pcaObj.fit(feature_input_for_pca)
# variance of features
variance_of_features = pcaObj.explained_variance_
# how much variance is explained each component
variance_ratio_of_features = pcaObj.explained_variance_ratio_
print "Explained varaince ratio"
for index_ in xrange(len(variance_ratio_of_features)):
    print "Principal component#{}, explained variance:{}".format(index_+1, variance_ratio_of_features[index_])
print "-"*50
# see how much explained variance is covered by the number of compoenents , and set the number
# no_features_to_use = 5 #using one PCA you get lesser accuracy
no_features_to_use = 1 #using one PCA for size only
print "Of all the features, we will use:", no_features_to_use
print "-"*50
pcaObj.n_components=no_features_to_use
selected_features = pcaObj.fit_transform(feature_input_for_pca)
print "Selected feature dataset size:", np.shape(selected_features)
print "-"*50
# pca_insight = getPCAInsights(pcaObj, no_features_to_use)
# print  pca_insight
# print "-"*50
#####print "Shape of transformed data:", selected_features.shape
# print "Transformed features: \n", selected_features
# print "-"*50



# sklearn_utility.performModeling(selected_features, all_labels, 10)
# print "-"*50

outputDir = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/ICSE19_TSE/SIZE-NODE-' +   dataset_file.split('/')[-1] + '/'
process_metric_utility.createOutputDirectory(outputDir)
print 'Output directory created ...'
sklearn_utility.performIterativeModeling(selected_features, all_labels, 10, 10, outputDir)
print "-"*50
print "The dataset was:", dataset_file
print "-"*50
print "Ended at:", process_metric_utility.giveTimeStamp()
