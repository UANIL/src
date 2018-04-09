'''
Author: Jake Wachs
Authority: The University of Alabama, Network Intrusion Lab
Function: This script will ping the url's from a provided
csv. If those url's exist, it will grab the header information
and write that to a csv file entitled header_info.csv.

Manual:
	To use script, simply run with cmd line arg [1] as the csv
	For instance:
		~$ python parser.py test.csv

'''

import csv
import sys
import urllib2

print "Starting..."
current_url = None

with open(sys.argv[1], 'rb') as file:
	reader = csv.reader(file)
	for row in reader:
		current_url = row[1]				# grabs url from csv

		response = urllib2.urlopen(current_url)
		response.getcode()

		if response.getcode() == 200:		# if site exists
			headers = response.info().headers
			write_file = open('header_info.csv', 'wb')
			
			headers_len = len(headers)

			i = 0							# keeps track of commas
			for info in headers:
				info = info.rstrip('\n')
				info = info.rstrip('\r')
				write_file.write(info)

				if i < headers_len - 1:
					write_file.write(', ')
				i += 1

			write_file.write('\n')


print "Done. Check header_info.csv for header information from dump."
