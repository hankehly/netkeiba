#
# Cookbook:: netkeiba
# Recipe:: pyenv
#
# Copyright:: 2019, hankehly, All Rights Reserved.

pyenv_system_install 'system'

pyenv_python node['netkeiba']['python_version']
pyenv_global node['netkeiba']['python_version']

pyenv_plugin 'virtualenv' do
  git_url 'https://github.com/pyenv/pyenv-virtualenv'
end

pyenv_pip 'awscli'

package 'python3.6-dev'
package 'libmysqlclient-dev'
