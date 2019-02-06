'''
Akond Rahman 
Feb 05, 2019 
Extra paper work 
'''
import pandas as pd 
from collections import Counter
import os 

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP)
    fileToWrite.close()
    return str(os.stat(fileP).st_size)


def showMetricDist(the_fil, metric_name, ds_name):
    strToWrite = ''
    

    the_df_ = pd.read_csv(the_fil)
    defect_df = the_df_[the_df_['defect_status']==1]

    metric_vals = defect_df[metric_name].tolist()
    tot_cnt = len(metric_vals)
    
    metric_dist = dict(Counter(metric_vals)) 
    for k_, v_ in metric_dist.iteritems():
        perc_valu = (float(v_)/float(tot_cnt))*100
        file_name =  ds_name.split('/')[-1] 
        print '[DATASET:::{}:::]{} developers for {}% defective scripts'.format(file_name, k_, perc_valu )
        strToWrite = strToWrite + str(k_) + ',' + str(perc_valu) + ',' + '\n'
    
    dumpContentIntoFile(strToWrite, '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/' + file_name + '_' + metric_name + '.csv')


if __name__=='__main__':
    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_MIR_FULL_DATASET.csv'
    # showMetricDist(the_fil, 'DEVS', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/MIRA_DEVS_DIST.csv')
    
    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_MOZ_FULL_DATASET.csv'
    # showMetricDist(the_fil, 'DEVS', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/MOZI_DEVS_DIST.csv')

    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_OST_FULL_DATASET.csv'
    # showMetricDist(the_fil, 'DEVS', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/OSTK_DEVS_DIST.csv')    

    the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_WIK_FULL_DATASET.csv'
    showMetricDist(the_fil, 'DEVS', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/WIKI_DEVS_DIST.csv')        

