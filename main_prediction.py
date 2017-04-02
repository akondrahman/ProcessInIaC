'''
main file for prediction model
'''

from sklearn.ensemble import ExtraTreesClassifier
from sklearn import decomposition
import process_metric_utility , numpy as np , pandas as pd, sklearn_utility
glimpseIndex=10

def getPCAInsights(pcaParamObj, which_component_to_see):
    '''
    reff-1: http://stackoverflow.com/questions/22348668/pca-decomposition-with-python-features-relevances
    reff-2: http://stackoverflow.com/questions/22984335/recovering-features-names-of-explained-variance-ratio-in-pca-with-sklearn
    '''
    top_three_components_index = np.abs(pcaParamObj.components_[which_component_to_see]).argsort()[::-1][:3]
    print top_three_components_index
    print "-"*50


print "Started at:", process_metric_utility.giveTimeStamp()
print "-"*50
'''
  first is mozilla then wiki
'''
dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/PRELIM_MOZILLA.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/PRELIM_WIKIMEDIA.csv"

print "The dataset is:", dataset_file
print "-"*50
full_dataset_from_csv = process_metric_utility.getDatasetFromCSV(dataset_file)
full_rows, full_cols = np.shape(full_dataset_from_csv)
print "Total number of columns", full_cols
## we will skip the first column, as it has file names
feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip
all_features = full_dataset_from_csv[:, 2:feature_cols]
print "Glimpse at features (11th entry in dataset): \n", all_features[glimpseIndex]
print "-"*50

dataset_for_labels = process_metric_utility.getDatasetFromCSV(dataset_file)  ## unlike phase-1, the labels are '1' and '0', so need to take input as str
label_cols = full_cols - 1
all_labels  =  dataset_for_labels[:, label_cols]
print "Glimpse at  labels (11th entry in dataset):", all_labels[glimpseIndex]
print "-"*50

defected_file_count     = len([x_ for x_ in all_labels if x_==1.0])
non_defected_file_count = len([x_ for x_ in all_labels if x_==0.0])
print "No of. defects={}, non-defects={}".format(defected_file_count, non_defected_file_count)
print "-"*50
'''
PCA ZONE
'''
pca_comp = 10 ###  must be less than or equal to no of features
'''
PCA reff:
1. http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html#sklearn.decomposition.PCA.fit
2. http://scikit-learn.org/dev/tutorial/statistical_inference/unsupervised_learning.html#principal-component-analysis-pca
'''
pcaObj = decomposition.PCA(n_components=pca_comp)
pcaObj.fit(all_features)
# variance of features
variance_of_features = pcaObj.explained_variance_
# how much variance is explained each component
variance_ratio_of_features = pcaObj.explained_variance_ratio_
print "Explained varaince ratio"
for index_ in xrange(len(variance_ratio_of_features)):
    print "Principal component#{}, explained variance:{}".format(index_+1, variance_ratio_of_features[index_])
print "-"*50
# see how much explained variance is covered by the number of compoenents , and set the number
no_features_to_use = 10 #using one PCA you get lesser accuracy, so we'll use 10, always check how much variance is explained
print "Of all the features, we will use:", no_features_to_use
print "-"*50
pcaObj.n_components=no_features_to_use
selected_features = pcaObj.fit_transform(all_features)
print "Selected feature dataset size:", np.shape(selected_features)
print "-"*50
pca_insight = getPCAInsights(pcaObj, 1)
print  pca_insight
print "-"*50
#####print "Shape of transformed data:", selected_features.shape
print "Transformed features: \n", selected_features
print "-"*50
sklearn_utility.performModeling(selected_features, all_labels, 10)
print "-"*50
# sklearn_models.performIterativeModeling(selected_features, all_labels, 10, 100)
print "-"*50
print "Ended at:", process_metric_utility.giveTimeStamp()
