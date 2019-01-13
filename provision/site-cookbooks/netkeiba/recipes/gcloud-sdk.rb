#
# Cookbook:: netkeiba
# Recipe:: gcloud-sdk
#
# Copyright:: 2019, hankehly, All Rights Reserved.

apt_package 'google-cloud-sdk'

apt_repository 'google-cloud-sdk' do
  uri 'http://packages.cloud.google.com/apt'
  distribution 'cloud-sdk-bionic'
  components ['main']
  key 'https://packages.cloud.google.com/apt/doc/apt-key.gpg'
  notifies :run, 'execute[apt-get update]', :immediately
end

# Perform manually
# execute 'gcloud init'