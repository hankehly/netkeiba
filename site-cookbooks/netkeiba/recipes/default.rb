#
# Cookbook:: netkeiba
# Recipe:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.

python_version = '3.6.7'

locale 'set locale' do
	lang 'en_US.utf8'
	lc_all 'en_US.utf8'
end

apt_repository 'name' do
	components ['contrib']
	distribution 'bionic'
	key 'https://packages.treasuredata.com/GPG-KEY-td-agent'
	uri 'http://packages.treasuredata.com/2.5/ubuntu/bionic/'
	action :add
end

pyenv_system_install 'system'

pyenv_python python_version
pyenv_global python_version

pyenv_plugin 'virtualenv' do
	git_url 'https://github.com/pyenv/pyenv-virtualenv'
end

pyenv_pip 'awscli'

directory '/var/log/fluentd' do
  	owner 'td-agent'
  	group 'td-agent'
  	mode '0755'
  	action :create
end

aws_access_key_id = data_bag_item('aws', 'credentials')['aws_access_key_id']
aws_secret_access_key = data_bag_item('aws', 'credentials')['aws_secret_access_key']

td_agent_match 'netkeiba' do
  	type 's3'
  	tag 'netkeiba.**'
  	action :create
  	parameters({
  		aws_key_id: aws_access_key_id,
  		aws_sec_key: aws_secret_access_key,
  		s3_bucket: 'octo-waffle',
  		path: 'netkeiba/log/',
  		buffer_path: '/var/log/fluentd/buffer/td',
  		time_slice_format: '%Y%m%d%H'
  	})
end

