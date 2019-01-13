#
# Cookbook:: netkeiba
# Recipe:: default
#
# Copyright:: 2019, hankehly, All Rights Reserved.

include_recipe 'apt'
include_recipe 'build-essential'
include_recipe 'nodejs'

package 'jq'

locale 'set locale' do
  lang 'en_US.utf8'
  lc_all 'en_US.utf8'
end

include_recipe 'netkeiba::pyenv'
include_recipe 'netkeiba::elk'
include_recipe 'netkeiba::gcloud-sdk'
