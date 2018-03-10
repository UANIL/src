import csv
import sys

#Author: Austin Rife
#Date: 1-23-2018
#Description: 
# This program parses a csv file exported from wireshark
# to output all URLs in the file.

#Running the program:
#python URLParser.py (filename.csv)

#Create a dictionary with the value being a count and the key being a URL
#url_Dictionary = {} #created a new dictionary named "url+Dictionary"

with open(sys.argv[1], 'rb') as csvfile:
	wordparser = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in wordparser:
		y=0

		for x in range(0, len(row)):
			word = row[x]

			if(y == 0):
				if(word == "query"):
					y+=1
				else:
					y=0
			elif(y == 1):
				if(word == "response"):
					#proceed with response code here
					#response style:
					#Example: 
					#"Standard query response 0x9980 A 5291166.fLs.DouBLeCLICK.neT CNAME 
					#dart.l.doubleclick.net A 172.217.6.6"

					hex = row[x+1]
					type = row[x+2] #A/AAAA
					url = row[x+3] #url
					#url.replace('"', '')
					print(url).replace('"', '')


					#cover multiple addresses in a single line
					for i in range(x+3, len(row)-2,2):
						type = row[i+1]
						url = row[i+2]
						print(url).replace('"', '')
						#url.replace('"', '')
					y=0

					#FIXME -- address what happens when "No such name" occurs
				else:
					y=0
					#proceed with query code here
					#query style: 
					#"Standard query 0x4375 A aD.ATDMT.c0m"
					hex = row[x]
					type = row[x+1] #A/AAAA
					url = row[x+2] #url
					print(url).replace('"', '')
					#url.replace('"', '')

#NEW GOALS:
#1. Print each url/IP addresses only once - print a count of how many times it appeared next to it
#2. Instead of printing to stdio format into a readable csv file