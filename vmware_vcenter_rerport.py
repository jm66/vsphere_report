#!/usr/bin/python
import sys, re, getpass, argparse, subprocess, logging
from time import sleep
from pysphere import MORTypes, VIServer, VITask, VIProperty, VIMor, VIException
from pysphere.vi_virtual_machine import VIVirtualMachine

def find_vm(name):
	try:
		vm = con.get_vm_by_name(name)
		return vm
	except VIException:
		return None

def print_dc(datacenters):
    print ' '
    print 'Datacenter(s):'
    for dc in sorted(datacenters):
        print '-%s' %dc

def print_cl(datacenters):
    print ' '
    print 'Cluster(s)'
    for cl in sorted(clusters):
        print '-%s' %cl

def print_hs(datacenters):
    print ' '
    print 'Host(s)'
    for hs in sorted(hosts):
        print '-%s' %hs

def print_ds(datacenters):
    print ' '
    print 'Datastore(s)'
    for ds in sorted(datastores):
        print '-%s' %ds   
         
def print_vms():
    print ' '
    print 'Virtual Machine(s)'
    print '.' * 50
    for vm in sorted(vms):
        print '-%s' %vm

def print_main(datacenters, clusters, hosts, datastores, vms):
    print 'Current installation has:'
    if datacenters is not None:
        print ' %d datacenter(s)' % len(datacenters)
    else:
        logger.error('No datacenters data could be gotten')
    
    if clusters is not None:
        print ' %d cluster(s)' % len(clusters)
    else:
        logger.error('No clusters data could be gotten')
    
    if hosts is not None:
        print ' %d host(s)' % len(hosts)
    else:
        logger.error('No hosts data could be gotten')
    
    if datastores is not None:
        print ' %d datastore(s)' % len(datastores)
    else:
        logger.error('No datastores data could be gotten')
    
    if vms is not None:
        print ' %d vm(s)' % len(vms)
    else:
        logger.error('No VMs data could be gotten')
    print ' '
        
def get_args():
	# Creating the argument parser		
    parser = argparse.ArgumentParser(description="Print report of the current vCenter environment")
    parser.add_argument('-s', '--server', nargs=1, required=True, help='The vCenter or ESXi server to connect to', dest='server', type=str)
    parser.add_argument('-u', '--user', nargs=1, required=True, help='The username with which to connect to the server', dest='username', type=str)
    parser.add_argument('-p', '--password', nargs=1, required=False, help='The password with which to connect to the host. If not specified, the user is prompted at runtime for a password', dest='password', type=str)
    parser.add_argument('-hs', '--hosts', required=False, help='Restrict report to hosts info', dest='hosts_i', action='store_true')
    parser.add_argument('-dc', '--datacenters', required=False, help='Restrict report to datacenters info', dest='datacenters_i', action='store_true')
    parser.add_argument('-cs', '--clusters', required=False, help='Restrict report to clusters info', dest='clusters_i', action='store_true')
    parser.add_argument('-ds', '--datastores', required=False, help='Restrict report to datastores info', dest='datastores_i', action='store_true')
    parser.add_argument('-vm', '--virtualmachines', required=False, help='Restrict report to VMs info', dest='vms_i', action='store_true')
    parser.add_argument('-v', '--verbose', required=False, help='Enable verbose output', dest='verbose', action='store_true')
    parser.add_argument('-d', '--debug', required=False, help='Enable debug output', dest='debug', action='store_true')
    parser.add_argument('-l', '--log-file', nargs=1, required=False, help='File to log to (default = stdout)', dest='logfile', type=str)
    parser.add_argument('-V', '--version', action='version', version="%(prog)s (version 0.2)")
	
    args = parser.parse_args()
    return args
    
# Parsing values
args = get_args()
argsdict = vars(args)
server 		= args.server[0]
username 	= args.username[0]
verbose		= args.verbose
debug		= args.debug
log_file	= None
password 	= None
dc_i        = args.datacenters_i
ds_i        = args.datastores_i
h_i         = args.hosts_i
vms_i       = args.vms_i
c_i         = args.clusters_i

if args.password:
	password = args.password[0]

if args.logfile:
        log_file = args.logfile[0]
# Logging settings
if debug:
	log_level = logging.DEBUG
elif verbose:
	log_level = logging.INFO
else:
	log_level = logging.WARNING
    
# Initializing logger
if log_file:
	logging.basicConfig(filename=log_file,format='%(asctime)s %(levelname)s %(message)s',level=log_level)
else:
	logging.basicConfig(filename=log_file,format='%(asctime)s %(levelname)s %(message)s',level=log_level)
	logger = logging.getLogger(__name__)
logger.debug('logger initialized')

# Asking Users password for server
if password is None:
	logger.debug('No command line password received, requesting password from user')
        password = getpass.getpass(prompt='Enter password for vCenter %s for user %s: ' % (server,username))

# Connecting to server
logger.info('Connecting to server %s with username %s' % (server,username))

con = VIServer()
try:
	logger.debug('Trying to connect with provided credentials')
	con.connect(server,username,password)
	logger.info('Connected to server %s' % server)
	logger.debug('Server type: %s' % con.get_server_type())
	logger.debug('API version: %s' % con.get_api_version())
except VIException as ins:
	logger.error(ins)
	logger.debug('Loggin error. Program will exit now.')
	sys.exit()

# Setting up vars
datacenters = None
clusters = None
hosts = None
datastores = None
vms = None

try:
    # Getting datacenters
    logger.debug('Getting datastores')
    datacenters = con.get_datacenters().values()

    # Getting clusters
    logger.debug('Getting clusters')
    clusters = con.get_clusters().values()

    # Getting Hosts
    logger.debug('Getting Hosts')
    hosts = con.get_hosts().values()

    # Getting Datastores 
    logger.debug('Getting Datastores')
    datastores = con.get_datastores().values()

    # Getting Registered VMs
    logger.debug('Getting VMs')
    vms = con.get_registered_vms()
    
    # Disconnecting from server
    con.disconnect()
except VIException as ins:
	logger.error(ins)
	logger.debug('An error ocurred getting vSphere data.')
        con.disconnect()
	sys.exit()

# printing main report    
print_main(datacenters, clusters, hosts, datastores, vms)

# printing DC report
if dc_i:
    logger.debug('Printing datacentres')
    print_dc(datacenters)

# printing clusters report
if c_i:
    logger.debug('Printing clusters')
    print_cl(clusters)

# printing hosts report
if h_i:
    logger.debug('Printing hosts')
    print_hs(hosts)

# printing datastores report
if ds_i:
    logger.debug('Printing datastores')
    print_ds(datastores)

# printing vms report    
if vms_i:
    logger.debug('Printing VMs')
    if len(vms) > 500:
        logger.info('This may take several seconds depending of the number of VMs in the environment.')
    print_vms(vms)
