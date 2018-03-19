#!/usr/bin/python

#
# Spencer F's CSV parser for Wireshark file
# Gives all sites visited, number of visits for each site, and the sites access at each time stamp since collection
#
#                                   # # Instructions # #
# Use display filter "udp.port == 53 && !(ip.src == 192.168.2.1) && !(ipv6.src == 2602:306:c456:d580::1)"
# displays URLs queries and ignores responses (at least for my file)
# Export that file as a CSV file
# Run program with one argument: the path to the exported CSV file
# Output is stored in its own directory
#


import csv
import sys
import os
import re

csv_file = csv.reader(open(sys.argv[1], "rb"), delimiter = ",")     # opening CSV file

title = str(sys.argv[1]).split('/')[-1]
if not os.path.exists(title):               #creating directory
    os.makedirs(title)
os.chdir(title)

s = open(title + '_sites.txt', 'w')
c = open(title + '_count.txt', 'w')
d = open(title + '_time.txt', 'w')

current_time = 0
firstline = True

for row in csv_file:

    if firstline:                  #skip the first line
        firstline = False
        continue
    info = row[6]
    time = row[1]
    sig_fig = time.split('.', 1)[0]
    sections = info.split()     # Currently pulls data that isnt a website
    site = sections[-1]
    site = site.lower()                # Make the site name uniform lowercase
    if (site.startswith('www.')):
        site = site.replace('www.', '')
    s.write(site)                       # Printing every site visited
    s.write('\n')
    if (current_time != sig_fig):      # Printing access time of websites
        current_time = sig_fig
        d.write(current_time)
        d.write(':')
        d.write('\n')
    d.write("   ")
    d.write(site)
    d.write('\n')

s.close()
d.close()
print '\nTime printed\n'

c = open(str(sys.argv[1]) + '_count.txt', 'w')
f = open(str(sys.argv[1]) + '_sites.txt', 'r')
count = {}


for DNS in f.read().split():
    if DNS not in count:
        count[DNS] = 1
    else:
        count[DNS] += 1

for k, v in sorted(count.iteritems(), key = lambda (k,v): (v,k), reverse = True):       # Printing occurences of websites
    c.write(k + " " + str(v))
    c.write('\n')

c.close()
print 'Site count printed\n'
f.close()
