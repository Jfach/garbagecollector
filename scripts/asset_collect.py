#!/usr/bin/env python
# vim: set ts=2 sw=2 ai et:
import nmapTools
import dnsTools
import csv
import os

# Read a file of networks in the format
# net_block(n),n.n.n.n/n
# example: net_block1,192.168.1.0/24
# Store in networks.txt (local directory) 
# Use the file to create a dictionary of desired networks to scan

net_dict = {}

with open('networks.txt') as f:
  for line in f:
    network = line.rstrip('\n').split(',') 
    net_dict[network[0]] = (network[1])
# logging (test) 
# print net_dict
results = []
# iterate through each K,V in net_dict then scan
for k,v in net_dict.iteritems():
  for x in v:
    results.append(nmapTools.ping_sweep(v))
# logging (test)
# print results

dns_list = []
lookups = []
for result in results:
  ips = result['scan'].keys()
  for ip in ips:
    if ip not in lookups:
      lookups.append(ip)
      print ip
      dns_rec = dnsTools.lookup(ip)
      if dns_rec[2] is not None:
        dns_dict = {'ip':dns_rec[2], 'fqdn': dns_rec[0], 'alias': dns_rec[1]}
        dns_list.append(dns_dict)
   

"""
# iterate through each discovered ip in results
# performing a dns lookcup using local DNS
for x in results:
  for y in results[x]:
    dns_rec = dnsTools.lookup(y) 
    # logging (test)
    # print (y,dns_rec[0],dns_rec[1],dns_rec[2])
    if dns_rec[2] is not None:
	# logging (test)
	# print (dns_rec[2])
	dns_dict = {'ip':dns_rec[2], 'fqdn': dns_rec[0], 'alias': dns_rec[1]}
        # logging (test)
        # print dns_dict
"""