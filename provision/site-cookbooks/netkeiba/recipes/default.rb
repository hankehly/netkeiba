#
# Cookbook:: netkeiba
# Recipe:: default
#
# Copyright:: 2018, hankehly, All Rights Reserved.

include_recipe 'apt'
include_recipe 'build-essential'
include_recipe 'nodejs'

python_version = '3.6.7'

locale 'set locale' do
	lang 'en_US.utf8'
	lc_all 'en_US.utf8'
end

pyenv_system_install 'system'

pyenv_python python_version
pyenv_global python_version

pyenv_plugin 'virtualenv' do
	git_url 'https://github.com/pyenv/pyenv-virtualenv'
end

pyenv_pip 'awscli'

include_recipe 'java'
include_recipe 'elasticsearch'
include_recipe 'td-agent'

aws_access_key_id = data_bag_item('aws', 'credentials')['aws_access_key_id']
aws_secret_access_key = data_bag_item('aws', 'credentials')['aws_secret_access_key']

td_agent_match 'netkeiba_s3' do
  	type 's3'
  	tag 'netkeiba.**'
  	parameters({
  		aws_key_id: aws_access_key_id,
  		aws_sec_key: aws_secret_access_key,
  		s3_bucket: 'octo-waffle',
  		s3_region: 'us-east-1',
  		path: 'netkeiba/log/',
  		buffer: [{
  			'@type': 'file',
  			path: '/var/log/td-agent/buffer/netkeiba',
  			timekey_use_utc: true
  		}]
  	})
  	action :create
end

td_agent_match 'netkeiba_elasticsearch' do
  	type 'elasticsearch'
  	tag 'netkeiba.**'
  	parameters({
  		host: 'localhost',
  		port: 9200,
  		logstash_format: true,
  		logstash_prefix: 'netkeiba'
  	})
  	action :create
end

include_recipe 'kibana::kibana6'
