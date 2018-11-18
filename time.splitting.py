'''
time series splitting
Akond Rahman
Sep 13, 2017 ...
Wednesday
'''
import csv, pandas as pd
import os, process_metric_utility
import matplotlib.pyplot as plt
'''
time series plotting
'''
def makeTimeSeriesPlotting(x_axis, y_axis, output_file_name):
    del x_axis[0]
    del y_axis[0]
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    x_axis_pos = list(range(len(x_axis)))
    plt.plot(x_axis_pos, y_axis, 'b-', linewidth = 1.0)
    ax.set_xticklabels(x_axis, rotation=45, fontsize=8)
    fig.savefig(output_file_name + '.png')
    plt.clf()
    plt.close()

def getTimeInfo(id_param, repo_param):
    dict2see = {}
    if repo_param.endswith('/'):
       repo_param = repo_param
    else:
       repo_param = repo_param + '/'
    file2read = repo_param + 'fullThrottle_msg_file_map.csv'
    with open(file2read, 'rU') as f:
         reader_ = csv.reader(f)
         for row in reader_:
             id_       = row[0]
             ts_    = row[2]
             dict2see[id_] = ts_
    return dict2see[id_param]

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP)
    fileToWrite.close()
    return str(os.stat(fileP).st_size)


def getYear(single_date):
    dt2ret = single_date.split('-')[0]
    return dt2ret

def getMonth(single_date):
    dt2ret =  single_date.split('-')[0] + '-' + single_date.split('-')[1]
    return dt2ret

def runAnalysis(df_param, mf, yf):
    _df = pd.DataFrame(df_param, columns=['ID', 'REPO', 'FILE', 'TIME', 'DEFECTSTATUS'])
    _df['YEAR']  = _df['TIME'].apply(getYear)
    _df['MONTH'] = _df['TIME'].apply(getMonth)
    #print _df.head()
    _df         = _df.sort(['MONTH'])
    _df_mon_cnt = _df.groupby(['MONTH'])[['FILE']].count()
    print _df_mon_cnt
    print '-'*50
    _df_y_cnt = _df.groupby(['YEAR'])[['FILE']].count()
    print _df_y_cnt
    print '-'*50
    '''
    get Y and X axis
    '''
    y_list     = _df_y_cnt.index.get_level_values('YEAR').tolist()
    y_c_list   = _df_y_cnt['FILE'].tolist()
    #print y_list, y_c_list
    makeTimeSeriesPlotting(y_list, y_c_list, yf)
    '''
    get Y and X axis
    '''
    m_list     = _df_mon_cnt.index.get_level_values('MONTH').tolist()
    m_c_list       = _df_mon_cnt['FILE'].tolist()
    makeTimeSeriesPlotting(m_list, m_c_list, mf)
 
def getCategFromDataset(categ_file_param, file2dump, mf, yf):
       str2write = ''
       df_list = []
       with open(categ_file_param, 'rU') as f:
         reader_ = csv.reader(f)
         next(reader_, None)
         for row in reader_:
             id_       = row[0]
             repo_     = row[1]
             categ_    = row[3]
             if categ_=='N':
                 defect_status = '1'
             else:
                 defect_status = '0'
             filepath_ = row[4]
             time_ = getTimeInfo(id_, repo_)
             time2write = time_.split(' ')[0]
             #print filepath_, time2write
             str2write = str2write + id_ + ',' + repo_ + ',' + filepath_ + ',' + time2write + ',' + defect_status + '\n'
             # for further anlysis
             df_list.append((id_, repo_, filepath_, time2write, defect_status))
       dumpContentIntoFile(str2write, file2dump)
       runAnalysis(df_list, mf, yf)


if __name__=='__main__':
    print 'Started at:', process_metric_utility.giveTimeStamp()
    print '='*100
    # dataset_file   = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
    # file2dump      = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/MOZ_TIMENDEFECT.csv'
    # plot_file_year = 'MOZ.Y.SCRIPTCOUNT.png'
    # plot_file_mont = 'MOZ.M.SCRIPTCOUNT.png'

    # dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.Final.Categ.csv'
    # file2dump    = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/OST_TIMENDEFECT.csv'
    # plot_file_year = 'OST.Y.SCRIPTCOUNT.png'
    # plot_file_mont = 'OST.M.SCRIPTCOUNT.png'
    #
    # dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'
    # file2dump    = '/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/WIK_TIMENDEFECT.csv'
    # plot_file_year = 'WIK.Y.SCRIPTCOUNT.png'
    # plot_file_mont = 'WIK.M.SCRIPTCOUNT.png'

    print 'The dataset is:', dataset_file
    getCategFromDataset(dataset_file, file2dump, plot_file_mont, plot_file_year)
    print '='*100
    print 'Ended at:', process_metric_utility.giveTimeStamp()
