'''
Akond Rahman
Oct 31, 2017
Tuesday
PCA Mining for all datasets
'''


from sklearn import decomposition
import process_metric_utility , numpy as np , pandas as pd
glimpseIndex=10

def doPCAMining(pcaParamObj, no_of_pca_comp_to_see, correlation_cutoff=0.0):
    headers = ['COMM', 'AGE', 'DEV', 'ADDPERLOC', 'DELPERLOC', 'SUMCHNG', 'TOTCHNGPERLOC', 'AVGCHNG', 'MINOR', 'SCTR', 'MT_PP', 'MT_NON_PP']
    print '+'*25
    print 'PCA metric importance zone  ...'
    print '+'*25
    for comp_index in xrange(no_of_pca_comp_to_see):
        # pcaParamObj.components_ contians correlation of each variable with each principal compoennt, in R we get this using $var$cor
        # string correlation between the vairables and eahc principal compeonnt is an important vairable ... reff: https://onlinecourses.science.psu.edu/stat505/node/54
        all_metric_value_in_one_component =  np.abs(pcaParamObj.components_[comp_index])
        sorted_all_metric_index_in_one_component = all_metric_value_in_one_component.argsort()[::-1]
        imp_met_cnt  = 0
        # print len(pcaParamObj.components_)
        for met_index in sorted_all_metric_index_in_one_component:
            met_corr_val = abs(all_metric_value_in_one_component[met_index])
            if (met_corr_val >= correlation_cutoff):
               met_name = headers[met_index]
               print 'Metric index:{}, correlation (with component) score:{}, name;{}'.format(met_index, met_corr_val, met_name)
               print '~'*5
               imp_met_cnt +=  1
        print '$'*15
        print 'Component index: {}, Important metric count:{}'.format(comp_index+ 1,  imp_met_cnt)
        print '$'*15
    print "+"*25


print "Started at:", process_metric_utility.giveTimeStamp()
print "-"*50
# FINA DATASETS : PCA: NO BFS
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_BASTION_FULL_PROCESS_DATASET.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_CISCO_FULL_PROCESS_DATASET.csv'
# dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/OCT17_MIRANTIS_FULL_PROCESS_DATASET.csv'
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MultiTasking_MOZ_FULL_PROCESS_DATASET.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MultiTasking_OPENSTACK_PROCESS_DATASET.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MultiTasking_WIKI_FULL_PROCESS_DATASET.csv"

print "The dataset is:", dataset_file
print "-"*50
full_dataset_from_csv = process_metric_utility.getDatasetFromCSV(dataset_file)
full_rows, full_cols = np.shape(full_dataset_from_csv)

## we will skip the first column, as it has file names
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
feature_input_for_pca = log_transformed_features
# selected_features = log_transformed_features
'''
PCA ZONE
'''
pca_comp = 10 ###  must be less than or equal to no of features
pcaObj = decomposition.PCA(n_components=pca_comp)
pcaObj.fit(feature_input_for_pca)
# variance of features
variance_of_features = pcaObj.explained_variance_
# how much variance is explained each component
variance_ratio_of_features = pcaObj.explained_variance_ratio_
# see how much explained variance is covered by the number of compoenents , and set the number
no_features_to_use = 5 #using one PCA you get lesser accuracy

pcaObj.n_components=no_features_to_use
selected_features = pcaObj.fit_transform(feature_input_for_pca)

'''
need to specifi correlation cutoff , to idnetify which variables correlate strinhly
with the individual compoennts
reff: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3576830/
any correlation cutoff >= 0.5 is moderatly strong and strong
'''
corr_cutoff = 0.5
print 'Correlation cutoff is:', corr_cutoff
doPCAMining(pcaObj, no_features_to_use, corr_cutoff)
print "Ended at:", process_metric_utility.giveTimeStamp()
print "-"*50
