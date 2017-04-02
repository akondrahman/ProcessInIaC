'''
main file for prediction model
'''

from sklearn.ensemble import ExtraTreesClassifier
from sklearn import decomposition
import Utility , numpy as np , sklearn_models, pandas as pd
glimpseIndex=10

def getPCAInsights(pcaParamObj, no_feat_param):
    '''
    reff-1: http://stackoverflow.com/questions/22348668/pca-decomposition-with-python-features-relevances
    reff-2: http://stackoverflow.com/questions/22984335/recovering-features-names-of-explained-variance-ratio-in-pca-with-sklearn
    '''
    top_three_components_index = np.abs(pcaParamObj.components_[no_feat_param]).argsort()[::-1][:3]
    print top_three_components_index



print "Started at:", Utility.giveTimeStamp()
'''
  first is mozilla then wiki
'''
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"
dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv"

print "The dataset is:", dataset_file
print "-"*50
full_dataset_from_csv = Utility.getDatasetFromCSV(dataset_file)
full_rows, full_cols = np.shape(full_dataset_from_csv)
print "Total number of columns", full_cols
## we will skip the first column, as it has file names
feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip
all_features = full_dataset_from_csv[:, 2:feature_cols]
print "Glimpse at features (11th entry in dataset): \n", all_features[glimpseIndex]
print "-"*50
