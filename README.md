vsphere_report
==================

Get a quick summary of the vSphere inventory.

Simple pysphere implementation script for reporting VMware vCenter inventory. Outputs a summary
of vCenter clusters, datacenters, hosts, datastores and virtual machines or lists each element.

``` bash
 ./vmware_vcenter_report.py -h
usage: vmware_vcenter_report.py [-h] -s SERVER -u USERNAME [-p PASSWORD] [-hs]
                                [-dc] [-cs] [-ds] [-vm] [-v] [-d] [-l LOGFILE]
                                [-V]

Print report of the current vCenter environment

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        The vCenter or ESXi server to connect to
  -u USERNAME, --user USERNAME
                        The username with which to connect to the server
  -p PASSWORD, --password PASSWORD
                        The password with which to connect to the host. If not
                        specified, the user is prompted at runtime for a
                        password
  -hs, --hosts          Restrict report to hosts info
  -dc, --datacenters    Restrict report to datacenters info
  -cs, --clusters       Restrict report to clusters info
  -ds, --datastores     Restrict report to datastores info
  -vm, --virtualmachines
                        Restrict report to VMs info
  -v, --verbose         Enable verbose output
  -d, --debug           Enable debug output
  -l LOGFILE, --log-file LOGFILE
                        File to log to (default = stdout)
  -V, --version         show program's version number and exit
```    

For example, getting an inventory summary:

``` bash
./vmware_vcenter_report.py -s 198.100.234.200 -u vma 
Enter password for vCenter 198.100.234.200 for user vma: 
Current installation has:
 1 datacenter(s)
 1 cluster(s)
 5 host(s)
 6 datastore(s)
 122 vm(s)
``` 
