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
