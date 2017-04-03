'''
April 01, 2017
Extracting process metrics
Akond Rahman
'''
import hg_process_extractor, git_process_extractor, process_metric_utility
MOZFLAG='moz'
WIKIFLAG='wikimedia'

def getAllProcessMetricsForSingleFile(full_path_param, repo_path_param):
  org_of_file                     = ''

  if(MOZFLAG in full_path_param):
   process_metrics         =  hg_process_extractor.getProcessMetrics(full_path_param, repo_path_param)
   org_of_file             =  'MOZILLA'
  elif(WIKIFLAG in full_path_param):
   process_metrics         =  git_process_extractor.getProcessMetrics(full_path_param, repo_path_param)
   org_of_file             =  'WIKIMEDIA'
  else:
   process_metrics         =  git_process_extractor.getProcessMetrics(full_path_param, repo_path_param)
   org_of_file             =  'OPENSTACK'
  print process_metrics
  print "Generated the process metrics ... "
  print "-"*50
  all_metric_as_str_for_file      = org_of_file + ',' + full_path_param + ',' + process_metrics
  return all_metric_as_str_for_file



def getAllProcessMetricForAllFiles(pupp_map_dict_param):
   datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/dataset/MOZ_WIKI_FULL_PROCESS_DATASET.csv'
   str2ret=''
   fileCount = 0
   for file_, details_ in pupp_map_dict_param.items():
     fileCount = fileCount + 1
     repo_                    = details_[1]
     defect_status            = details_[0]
     print "Analyzing ... \nfile#{}\ndefect status:{}\nfile:{}\nrepo:{}".format(fileCount, defect_status, file_, repo_)
     all_metric_for_this_file = getAllProcessMetricsForSingleFile(file_, repo_)
     str2ret = str2ret + all_metric_for_this_file + defect_status + '\n'
     print "="*75
   dump_stats = process_metric_utility.createDataset(str2ret, datasetFile2Save)
   print "Dumped a file of {} bytes".format(dump_stats)
   return str2ret

'''
testing purpose
'''
test_hg_file  = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/relabs-puppet/manifests/site.pp'
test_git_file = '/Users/akond/PUPP_REPOS/wikimedia-downloads/mariadb/manifests/heartbeat.pp'
git_repo_path = '/Users/akond/PUPP_REPOS/wikimedia-downloads/mariadb'
hg_repo_path  = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/relabs-puppet/'

# getAllProcessMetricsForSingleFile(test_hg_file, hg_repo_path)
# getAllProcessMetricsForSingleFile(test_git_file, git_repo_path)

'''
for dataset geenration
'''
print "Started at:", process_metric_utility.giveTimeStamp()
fullPuppMap   = process_metric_utility.getPuppetFileDetails()
print "Loaded the mapping of files ... "
print "-"*100
str_ = getAllProcessMetricForAllFiles(fullPuppMap)
print "-"*100
print "We analyzed {} Puppet files".format(len(fullPuppMap))
print "-"*100
print "Ended at:", process_metric_utility.giveTimeStamp()
print "-"*100
