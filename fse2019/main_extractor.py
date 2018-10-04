'''
Apri 01, 2017
Extracting process metrics
Akond Rahman
'''
import hg_process_extractor
import git_process_extractor 
import process_metric_utility

MOZFLAG='moz'
WIKIFLAG='wikimedia'
OPENSTACKFLAG='openstack'

def getAllProcessMetricsForSingleFile(full_path_param, repo_path_param, org_of_file):
  if(MOZFLAG in full_path_param):
     process_metrics         =  hg_process_extractor.getProcessMetrics(full_path_param, repo_path_param)
  elif(WIKIFLAG in full_path_param):
      process_metrics         =  git_process_extractor.getProcessMetrics(full_path_param, repo_path_param)
  else:
      process_metrics         =  git_process_extractor.getProcessMetrics(full_path_param, repo_path_param)
  print process_metrics
  print "Generated the process metrics ... "
  print "-"*50
  all_metric_as_str_for_file      = org_of_file + ',' + full_path_param + ',' + process_metrics
  return all_metric_as_str_for_file



def getAllProcessMetricForAllFiles(pupp_map_dict_param, datasetFile2Save, org_name, meenely_dict):
   str2ret=''
   fileCount = 0

   for file_, details_ in pupp_map_dict_param.items():
     if (file_!= 'WTF') and (file_ in meenely_dict):
        fileCount = fileCount + 1
        repo_                    = details_[1]
        defect_status            = details_[0]
        print "Analyzing ... \nfile#{}\ndefect status:{}\nfile:{}\nrepo:{}".format(fileCount, defect_status, file_, repo_)
        all_metric_for_this_file = getAllProcessMetricsForSingleFile(file_, repo_, org_name)
        dev_met_, col_met_ = meenely_dict[file_]
        all_metric_for_this_file = all_metric_for_this_file + str(dev_met_) + ',' + str(col_met_) + ','
        str2ret = str2ret + all_metric_for_this_file + defect_status + '\n'
        print "="*75
   dump_stats = process_metric_utility.createDataset(str2ret, datasetFile2Save)
   print "Dumped a file of {} bytes".format(dump_stats)
   return str2ret

'''
for dataset generation 
'''

### INPUT

# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mirantis_Categ_For_DB.csv'
# init_dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/MIR_FUL_PRO.csv'
# ORG = 'MIRANTIS'


# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
# init_dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/MOZ_FUL_PRO.csv'
# ORG = 'MOZILLA'

# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.WithoutBadBoys.Final.Categ.csv'
# init_dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/OST_FUL_PRO.csv'
# ORG = 'OPENSTACK'

# theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'
# init_dataset_file='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/ICSE19_TSE/WIK_FUL_PRO.csv'
# ORG = 'WIKIMEDIA'


### OUTPUT

# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/MIR_FULL_DATASET.csv'
# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/MOZ_FULL_DATASET.csv'
# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/OST_FULL_DATASET.csv'
# datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/FSE2019/WIK_FULL_DATASET.csv'




print "Started at:", process_metric_utility.giveTimeStamp()
fullPuppMap   = process_metric_utility.getPuppetFileDetails(theCompleteCategFile)
meenely_dict  = process_metric_utility.getMeenelyDetails(init_dataset_file)
print "Loaded the defect mapping of files ... "
print "-"*100


str_ = getAllProcessMetricForAllFiles(fullPuppMap, datasetFile2Save, ORG, meenely_dict)
print "-"*100
print "We analyzed {} Puppet files".format(len(fullPuppMap))
print "-"*100
print "Ended at:", process_metric_utility.giveTimeStamp()
print "-"*100
