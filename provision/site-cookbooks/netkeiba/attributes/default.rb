default['netkeiba']['python_version'] = '3.6.7'

default['td_agent']['includes'] = true
default['td_agent']['version'] = '3.2.1'

default['nodejs']['install_method'] = 'binary'
default['nodejs']['version'] = '10.14.2'
default['nodejs']['binary']['checksum'] = '0552b0f6fc9c0cd078bbb794c876e2546ba63a1dfcf8e3c206387936696ca128'

default['java']['jdk_version'] = '8'
default['java']['install_flavor'] = 'oracle'
default['java']['oracle']['accept_oracle_download_terms'] = true

default['kibana']['version'] = 6
default['kibana']['kibana6_version'] = '6.5.4'

default['rsyslog']['server_ip'] = '127.0.0.1'
default['rsyslog']['protocol'] = 'tcp'
# ports below 1024 require root access to bind
# so add a 0 to the end of the default port
default['rsyslog']['port'] = '5140'
default['rsyslog']['logs_to_forward'] = '*.*'
