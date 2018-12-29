#
# Cookbook:: netkeiba
# Recipe:: default
#
# Copyright:: 2018, hankehly, All Rights Reserved.

include_recipe 'apt'
include_recipe 'build-essential'

package 'jq'

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

include_recipe 'rsyslog::client'
include_recipe 'java'
include_recipe 'elasticsearch'
include_recipe 'td-agent'

aws_access_key_id = data_bag_item('aws', 'credentials')['aws_access_key_id']
aws_secret_access_key = data_bag_item('aws', 'credentials')['aws_secret_access_key']

td_agent_source 'in_syslog' do
	type 'syslog'
	tag 'system'
	parameters({
		port: node['rsyslog']['port'],
		bind: '0.0.0.0',
		protocol_type: 'tcp'
	})
end

td_agent_match 'netkeiba_out_s3' do
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

td_agent_match 'out_elasticsearch' do
  	type 'elasticsearch'
  	tag '{netkeiba.**,system.**,unattended-upgrades}'
  	parameters({
  		host: 'localhost',
  		port: 9200,
  		logstash_format: true,
  		logstash_prefix: '${tag}'
  	})
  	action :create
end

include_recipe 'kibana::kibana6'

apt_repository 'google-cloud-sdk' do
    uri 'http://packages.cloud.google.com/apt'
    distribution 'cloud-sdk-xenial'
    components ['main']
    key 'https://packages.cloud.google.com/apt/doc/apt-key.gpg'
    notifies :run, 'execute[apt-get update]', :immediately
end

apt_package 'google-cloud-sdk'

# Perform manually
# execute 'gcloud init'
