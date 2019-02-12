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
    if metric_name == 'OWNER_LINES':
       metric_vals = [round(x_, 1) for x_ in metric_vals]

    tot_cnt = len(metric_vals)
    
    metric_dist = dict(Counter(metric_vals)) 
    for k_, v_ in metric_dist.iteritems():
        perc_valu = (float(v_)/float(tot_cnt))*100
        file_name =  ds_name.split('/')[-1] 
        print '[DATASET:::{}:::]{}  for {}% defective scripts'.format(file_name, k_, perc_valu )
        strToWrite = strToWrite + str(k_) + ',' + str(perc_valu) + ',' + '\n'
    
    dumpContentIntoFile(strToWrite, '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/' + file_name + '_' + metric_name + '.csv')

def dumpCount(the_fil, metric_name, output_file,  ds_name):
    strToWrite = ''
    the_df_ = pd.read_csv(the_fil)

    defect_df = the_df_[the_df_['defect_status']==1]
    defect_metric_vals = defect_df[metric_name].tolist()

    non_defect_df = the_df_[the_df_['defect_status']==0]
    non_defect_metric_vals = non_defect_df[metric_name].tolist()

    for x_ in defect_metric_vals: 
        strToWrite = strToWrite + ds_name + ',' + str(x_) + ',' + 'Defective' + ',' + '\n'

    for y_ in non_defect_metric_vals: 
        strToWrite = strToWrite + ds_name + ',' + str(y_) + ',' + 'Neutral' + ',' + '\n'

    file_name = output_file.split('/')[-1] 
    dumpContentIntoFile(strToWrite, '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/' + file_name + '_' + metric_name + '.csv')

if __name__=='__main__':
    '''
    get percentages 
    '''

    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_MIR_FULL_DATASET.csv'
    # showMetricDist(the_fil, 'COLA_MET', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/MIRA_COLA_MET_DIST.csv')
    
    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_MOZ_FULL_DATASET.csv'
    # showMetricDist(the_fil, 'COLA_MET', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/MOZI_COLA_MET_DIST.csv')

    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_OST_FULL_DATASET.csv'
    # showMetricDist(the_fil, 'COLA_MET', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/OSTK_COLA_MET_DIST.csv')    

    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_WIK_FULL_DATASET.csv'
    # showMetricDist(the_fil, 'COLA_MET', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/WIKI_COLA_MET_DIST.csv')        

    '''
    dump raw coutnt 
    '''

    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_MIR_FULL_DATASET.csv'
    # dumpCount(the_fil, 'OWNER_LINES', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/MIRA_OWNER_LINES_RAW_CNT.csv', 'MIR')    

    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_MOZ_FULL_DATASET.csv'
    # dumpCount(the_fil, 'OWNER_LINES', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/MOZ_OWNER_LINES_RAW_CNT.csv', 'MOZ')    

    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_OST_FULL_DATASET.csv'
    # dumpCount(the_fil, 'OWNER_LINES', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/OSTK_OWNER_LINES_RAW_CNT.csv', 'OST')    

    # the_fil = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/FIGSHARE/REDUCED_WIK_FULL_DATASET.csv'
    # dumpCount(the_fil, 'OWNER_LINES', '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/WIK_OWNER_LINES_RAW_CNT.csv', 'WIK')    