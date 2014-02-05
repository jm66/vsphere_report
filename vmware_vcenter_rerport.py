#!/usr/bin/python
# Requires Pysphere: pip install pysphere
import sys, re, getpass, argparse, subprocess
from time import sleep
from pysphere import MORTypes, VIServer, VITask, VIProperty, VIMor, VIException
from pysphere.vi_virtual_machine import VIVirtualMachine

def print_verbose(message):
	if verbose:
		print message
def find_vm(name):
	try:
		vm = con.get_vm_by_name(name)
		return vm
	except VIException:
		return None
		
		
parser = argparse.ArgumentParser(description="Print report of the current vCenter environment")
parser.add_argument('-s', '--server', nargs=1, required=True, help='The vCenter or ESXi server to connect to', dest='server', type=str)
parser.add_argument('-u', '--user', nargs=1, required=True, help='The username with which to connect to the server', dest='username', type=str)
parser.add_argument('-hs', '--hosts', required=False, help='Restrict report to hosts info', dest='hosts_i', action='store_true')
parser.add_argument('-dc', '--datacenters', required=False, help='Restrict report to datacenters info', dest='datacenters_i', action='store_true')
parser.add_argument('-cs', '--clusters', required=False, help='Restrict report to clusters info', dest='clusters_i', action='store_true')
parser.add_argument('-ds', '--datastores', required=False, help='Restrict report to datastores info', dest='datastores_i', action='store_true')
parser.add_argument('-vm', '--virtualmachines', required=False, help='Restrict report to VMs info', dest='vms_i', action='store_true')
parser.add_argument('-v', '--verbose', required=False, help='Enable verbose output', dest='verbose', action='store_true')

args = parser.parse_args()
server 		= args.server[0]
username 	= args.username[0]
verbose		= args.verbose
dc_i        = args.datacenters_i
ds_i        = args.datastores_i
h_i         = args.hosts_i
vms_i       = args.vms_i
c_i         = args.clusters_i

# Asking Users password for server
password=getpass.getpass(prompt='Enter password for vCenter %s for user %s: ' % (server,username))

statuses = ['poweredOn','poweredOff','suspended']

# Connecting to server
print_verbose('Connecting to server %s with username %s' % (server,username))
con = VIServer()
con.connect(server,username,password)
print '-' * 50
print_verbose('Connected to server %s' % server)
print_verbose('Server type: %s' % con.get_server_type())
print_verbose('API version: %s' % con.get_api_version())
print '-' * 50

# Getting datacenters
datacenters = con.get_datacenters().values()

# Getting clusters
clusters = con.get_clusters().values()

# Getting Hosts
hosts = con.get_hosts().values()

# Getting Datastores 
datastores = con.get_datastores().values()

# Getting Registered VMs
vms = con.get_registered_vms()

print 'Current installation has:'
print ' %d datacenter(s)' % len(datacenters)
print ' %d cluster(s)' % len(clusters)
print ' %d host(s)' % len(hosts)
print ' %d datastore(s)' % len(datastores)
print ' %d vm(s)' % len(vms)
print '.' * 50

if dc_i:
    print 'Datacenter(s)'
    print '.' * 50
    for dc in sorted(datacenters):
        print '-%s' %dc
    print '.' * 50

if c_i:
    print 'Cluster(s)'
    print '.' * 50
    for cl in sorted(clusters):
        print '-%s' %cl
    print '.' * 50

if h_i:
    print 'Host(s)'
    print '.' * 50
    for hs in sorted(hosts):
        print '-%s' %hs
    print '.' * 50

if ds_i:
    print 'Datastore(s)'
    print '.' * 50
    for ds in sorted(datastores):
        print '-%s' %ds
    print '.' * 50
    
if vms_i:
    print 'Virtual Machine(s)'
    print '.' * 50
    for vm in sorted(vms):
        print '-%s' %vm
    print '.' * 50
        
# Disconnecting from server
con.disconnect()
