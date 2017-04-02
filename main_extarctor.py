'''
April 01, 2017
Extracting process metrics
Akond Rahman
'''
import hg_process_extractor, git_process_extractor
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
print "Started at:", process_metric_utility.gigiveTimeStamp()
fullPuppMap   = process_metric_utility.getPuppetFileDetails()
print "Loaded the mapping of files ... "
print "-"*100
getAllStaticMatricForAllFiles(fullPuppMap)
print "We analyzed {} Puppet files".format(len(fullPuppMap))
print "-"*100
print "Ended at:", process_metric_utility.gigiveTimeStamp()
print "-"*100
