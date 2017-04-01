'''
April 01, 2017
Extracting process metrics
Akond Rahman
'''




'''
testing purpose
'''
test_hg_file  = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/relabs-puppet/manifests/site.pp'
test_git_file = '/Users/akond/PUPP_REPOS/wikimedia-downloads/mariadb/manifests/heartbeat.pp'
git_repo_path = '/Users/akond/PUPP_REPOS/wikimedia-downloads/mariadb'
hg_repo_path = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/relabs-puppet/'
getAllStaticMetricForSingleFile(test_hg_file, hg_repo_path)
