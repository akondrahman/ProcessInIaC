'''
Akond Rahman
April 10, 2017
main file for prediction model
'''

from sklearn.ensemble import ExtraTreesClassifier
from sklearn import decomposition
import process_metric_utility , numpy as np , pandas as pd, sklearn_utility


print "Started at:", process_metric_utility.giveTimeStamp()
print "-"*50


'''
FSE 2019 
'''
dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/V1_WIK_FULL_DATASET.csv'

print "The dataset is:", dataset_file
print "-"*50
full_dataset_from_csv = process_metric_utility.getDatasetFromCSV(dataset_file)
full_rows, full_cols = np.shape(full_dataset_from_csv)
print "Total number of columns", full_cols

feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip

all_features = full_dataset_from_csv[:, 2:feature_cols]

dataset_for_labels = process_metric_utility.getDatasetFromCSV(dataset_file)  ## unlike phase-1, the labels are '1' and '0', so need to take input as str
label_cols = full_cols - 1 

all_labels  =  dataset_for_labels[:, label_cols]

defected_file_count     = len([x_ for x_ in all_labels if x_==1.0])
non_defected_file_count = len([x_ for x_ in all_labels if x_==0.0])
print "No of. defects={}, non-defects={}".format(defected_file_count, non_defected_file_count)
print "-"*50

'''
lets transform all the features via log transformation
'''
log_transformed_features = process_metric_utility.createLogTransformedFeatures(all_features)
print "Selected (log-transformed) feature dataset size:", np.shape(log_transformed_features)
feature_input_for_pca = log_transformed_features
'''
PCA ZONE
'''
# pca_comp = 10 ###  must be less than or equal to no of features
pca_comp = 1 ###  for size
pcaObj = decomposition.PCA(n_components=pca_comp)
pcaObj.fit(feature_input_for_pca)

variance_of_features = pcaObj.explained_variance_

variance_ratio_of_features = pcaObj.explained_variance_ratio_
print "Explained varaince ratio"
for index_ in xrange(len(variance_ratio_of_features)):
    print "Principal component#{}, explained variance:{}".format(index_+1, variance_ratio_of_features[index_])
print "-"*50

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

outputDir = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/ICSE19_TSE/SIZE-NODE-' +   dataset_file.split('/')[-1] + '/'
process_metric_utility.createOutputDirectory(outputDir)
print 'Output directory created ...'
sklearn_utility.performIterativeModeling(selected_features, all_labels, 10, 10, outputDir)
print "-"*50
print "The dataset was:", dataset_file
print "-"*50
print "Ended at:", process_metric_utility.giveTimeStamp()
