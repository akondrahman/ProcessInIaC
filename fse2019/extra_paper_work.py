'''
Akond Rahman 
Feb 05, 2019 
Extra paper work 
'''
import pandas as pd 
from collections import Counter

def showMetricDist(the_fil, metric_name, ds_name):
    the_df_ = pd.read_csv(the_fil)
    defect_df = the_df_[the_df_['defect_status']==1]

    metric_vals = defect_df[metric_name].tolist()
    tot_cnt = len(metric_vals)
    
    metric_dist = dict(Counter(metric_vals)) 
    for k_, v_ in metric_dist.iteritems():
        print '[DATSET:::{}:::]{} developers for {}% defective scripts'.format(ds_name, k_, (float(v_)/float(tot_cnt))*100)


if __name__=='__main__':
    the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_MIR_FULL_DATASET.csv'
    showMetricDist(the_fil, 'DEVS', 'MIR')
    
    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_MOZ_FULL_DATASET.csv'
    # showMetricDist(the_fil, 'DEVS', 'MOZ')
    

