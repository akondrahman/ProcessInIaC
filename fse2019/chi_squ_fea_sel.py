'''
Oct 24 2018 
Wed 
Chi Square-based feature selection 
'''
import process_metric_utility , numpy as np , pandas as pd, sklearn_utility
import sklearn.feature_selection 


def performChi(feat_, label, feat_names):
    chi_squ, p_val = sklearn.feature_selection.chi2(feat_, label)
    for imp_vec_index in xrange(len(feat_names)):
            chi_squ_val = chi_squ[imp_vec_index]
            indi_p_val  = p_val[imp_vec_index]
            print 'Metric:{}, Chi-Square:{}, p-val:{}'.format(feat_names[imp_vec_index], chi_squ_val, indi_p_val)
            print '-'*25


def getColumnNames(file_name_param, start, end ):
    ds_   = pd.read_csv(file_name_param)
    temp_ = list(ds_.columns.values)
    temp_ = temp_[start:end]
    return temp_

if __name__=='__main__':
    print "Started at:", process_metric_utility.giveTimeStamp()
    print "-"*50

    # dataset_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_MIR_FULL_DATASET.csv'
    # dataset_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_MOZ_FULL_DATASET.csv'
    # dataset_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_OST_FULL_DATASET.csv'
    # dataset_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/REDUCED_WIK_FULL_DATASET.csv'
    # start_cols = 2

    # dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/MIR_VDB.csv'
    # dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/MOZ_VDB.csv'
    # dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/OST_VDB.csv'
    # dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/WIK_VDB.csv'
    # start_cols =  1 



    full_dataset_from_csv = process_metric_utility.getDatasetFromCSV(dataset_file)
    full_rows, full_cols = np.shape(full_dataset_from_csv)


    feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip

    all_features = full_dataset_from_csv[:, start_cols:feature_cols]

    dataset_for_labels = process_metric_utility.getDatasetFromCSV(dataset_file)  ## unlike phase-1, the labels are '1' and '0', so need to take input as str
    label_cols = full_cols - 1 

    all_labels  =  dataset_for_labels[:, label_cols]

    defected_file_count     = len([x_ for x_ in all_labels if x_==1.0])
    non_defected_file_count = len([x_ for x_ in all_labels if x_==0.0])

    feature_names = getColumnNames(dataset_file, start_cols, feature_cols)

    performChi(all_features, all_labels, feature_names )

    print "The dataset was:", dataset_file
    print "-"*50
    print "Ended at:", process_metric_utility.giveTimeStamp()    