vmware_vctr_report
==================

Reporting VMware vCenter inventory

Simple pysphere implementation script for reporting VMware vCenter inventory. Outputs a summary
of vCenter clusters, datacenters, hosts, datastores and virtual machines or lists each element.

``` bash
  ./vctr_report.py  -s vctr5-1 -h
  usage: vctr_report.py [-h] -s SERVER -u USERNAME [-hs] [-dc] [-cs] [-ds] [-vm]
                      [-v]

  Print report of the current vCenter environment

  optional arguments:
    -h, --help            show this help message and exit
    -s SERVER, --server SERVER
                        The vCenter or ESXi server to connect to
    -u USERNAME, --user USERNAME
                        The username with which to connect to the server
    -hs, --hosts          Restrict report to hosts info
    -dc, --datacenters    Restrict report to datacenters info
    -cs, --clusters       Restrict report to clusters info
    -ds, --datastores     Restrict report to datastores info
    -vm, --virtualmachines
                        Restrict report to VMs info
    -v, --verbose         Enable verbose output
```    

For example, getting an inventory summary:

``` bash
  ./vctr_report.py-s 198.100.234.200 -u stats -v 
  Enter password for vCenter 198.100.234.200 for user stats: 
  Connecting to server 198.100.234.200 with username stats
  --------------------------------------------------
  Connected to server 198.100.234.200
  Server type: VMware vCenter Server
  API version: 5.1
  --------------------------------------------------
  Current installation has:
   1 datacenter(s)
   2 cluster(s)
   3 host(s)
   5 datastore(s)
   8 vm(s)
  ..................................................
``` 
Listing hosts and datastores available in current installation:

``` bash
  ./vctr_report.py-s 198.100.234.200 -u stats -v -hs -ds
  Enter password for vCenter 198.100.234.200 for user stats: 
  Connecting to server 198.100.234.200 with username stats
  --------------------------------------------------
  Connected to server 198.100.234.200
  Server type: VMware vCenter Server
  API version: 5.1
  --------------------------------------------------
  Current installation has:
   1 datacenter(s)
   2 cluster(s)
   3 host(s)
   5 datastore(s)
   8 vm(s)
  ..................................................
  Host(s)
  ..................................................
  198.100.234.10
  198.100.234.15
  198.100.234.20
  ..................................................
  Datastore(s)
  ..................................................
  datastore1
  datastore2
  datastore3
  datastore4
  datastore5
  ..................................................
```
