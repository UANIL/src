import sqlite3
import io
import csv
import os.path

#Author: Austin Rife
#Email: Arife1@crimson.ua.edu
#Date: 9 April 2018
#Description: This program is dedicated to parsing tables within a specified .sql file. The program can
			  #search for a specific keyword, list all Tables in the file, display a menu of options,
			  #and run complete file parsing on the given file. The complete file parsing searches for
			  #tables that are in the list hard-coded in and parses the information from those tables
			  #into a csv file with that table name. All quotes and parenthesis are trimmed away. The
			  #table should resemble an SQL table but in CSV form, this should enable simpler
			  #access to the data for program automation.

#max number of lines per file (max rows for an excel sheet is 1,048,576)
#KEY GLOBAL PARAMETERS
max_rows_in_file = 1000000 
split_into_separate_files = True

#Reads in the given keyword to search the .sql file for a given keyword
print('This program searches a given .sql file for a given keyword and outputs all matches.')

#DETERMINING WHAT COMPONENTS/COLUMNS TO INCLUDE IN THE OUTPUT FILES
columns_include = {} #define a new dictionary
descriptions = {} #define a new dictionary
columns_include['bitcoin_address'] = {'id' : 'y',
									'address' : 'y'} 

#bitcoin_address_cols_include = {}

#bitcoin_address_link_cols_include 
columns_include['bitcoin_address_link'] = {'page' : 'y',
									 'bitcoin_address' : 'y'}

#category_cols_include 
columns_include['category'] = {'ID' : 'y',
							'name' : 'y',
							'is_auto' : 'y',
							'created_at' : 'y'}

#category_link_cols_include 
columns_include['category_link'] = {'domain' : 'y',
							'category' : 'y',
							 'is_confirmed' : 'y', 
							 'is_valid' : 'y', 
							 'created_at' : 'y'}

#categorylink_cols_include 
columns_include['categorylink'] = {'ID' : 'y',
							'domain' : 'y',
							'category' : 'y',
							'is_valid' : 'y',
							'is_confirmed' : 'y',
							'created_at' : 'y'}

#clone_group_cols_include 
columns_include['clone_group'] = {'ID' : 'y'}

#daily_stat_cols_include 
columns_include['daily_stat'] = {'ID' : 'y',
							'Created_At' : 'y',
							'Unique_Visitors' : 'y',
							'Total_Onions' : 'y',
							'New_Onions' : 'y',
							'Total_Clones' : 'y',
							'Total_Onions_All' : 'y',
							'New_Onions_All' : 'y',
							'Banned' : 'y',
							'Up_Right_Now' : 'y',
							'Up_Right_Now_All' : 'y',
							'Banned_Up_Last_24' : 'y'}

#domain_cols_include 
columns_include['domain'] = {'id' : 'y',
						'host' : 'y',
						'port' : 'y',
						'ssl' : 'y',
						'is_up' : 'y',
						'created_at' : 'y',
						'visited_at' : 'y',
						'title' : 'y',
						'last_alive' : 'y',
						'is_crap' : 'y',
						'is_genuine' : 'y',
						'is_fake' : 'y',
						'ssh_fingerprint' : 'y',
						'is_subdomain' : 'y',
						'server' : 'y',
						'powered_by' : 'y',
						'dead_in_a_row' : 'y',
						'next_scheduled_check' : 'y',
						'is_banned' : 'y',
						'portscanned_at' : 'y',
						'path_scanned_at' : 'y',
						'useful_404_scanned_at' : 'y',
						'useful_404' : 'y',
						'useful_404_php' : 'y',
						'useful_404_dir' : 'y',
						'clone_group' : 'y',
						'new_clone_group' : 'y',
						'ban_exempt' : 'y',
						'manual_genuine' : 'y',
						'language' : 'y',
						'description_json' : 'y',
						'description_json_at' : 'y',
						'whatweb_at' : 'y'}

#email_cols_include 
columns_include['email'] = {'ID' : 'y',
						'Address' : 'y'}

#email_link_cols_include = {}
columns_include['email_link'] = {'email' : 'y',
								'page' : 'y'} 

#headless_bot
columns_include['headless_bot'] = {'uuid' : 'y',
									'kind' : 'y',
									'created_at' : 'y'}

#headlessbot_cols_include 
columns_include['headlessbot'] = {'ID' : 'y',
							'uuid' : 'y',
							'kind' : 'y',
							'created_at' : 'y'}

#open_port_cols_include
columns_include['open_port'] = {'id' : 'y',
							'port' : 'y',
							'domain' : 'y'}
#page_cols_include
columns_include['page'] = {'id' : 'y',
						'url' : 'y',
						'title' : 'y',
						'code' : 'y',
						'domain' : 'y',
						'created_at' : 'y',
						'visited_at' : 'y',
						'is_frontpage' : 'y',
						'size' : 'y',
						'path' : 'y'}

#page_link_cols_include
columns_include['page_link'] = {'link_from' : 'y',
							'link_to' : 'y'}

#request_log_cols_include
columns_include['request_log'] = {'id' : 'y',
							'uuid' : 'y',
							'uuid_is_fresh' : 'y',
							'created_at' : 'y',
							'agent' : 'y',
							'path' : 'y',
							'full_path' : 'y',
							'referrer' : 'y'}

#search_log_cols_include
columns_include['search_log'] = {'id' : 'y',
							'request_log' : 'y',
							'created_at' : 'y',
							'has_searchterms' : 'y',
							'searchterms' : 'y',
							'has_searchterms' : 'y',
							'has_raw_searchterms' : 'y',
							'raw_searchterms' : 'y',
							'is_firstpage' : 'y',
							'is_json' : 'y',
							'context' :'y',
							'results' : 'y'}

#ssh_fingerprint_cols_include
columns_include['ssh_fingerprint'] = {'id' : 'y',
								'fingerprint' : 'y'}

#web_component_cols_include
columns_include['web_component'] = {'id' : 'y',
								'name' : 'y',
								'version' : 'y',
								'account' : 'y',
								'string' : 'y'}

#web_component_link_cols_include
columns_include['web_component_link'] = {'web_component' : 'y',
									'domain' : 'y'}

Tables = {"bitcoin_address", "bitcoin_address_link", "category", "category_link",
			"categorylink", "clone_group", "daily_stat", "domain", "email", "email_link",
			"headless_bot", "headlessbot", "open_port", "page_link", "page",
			"request_log", "search_log", "ssh_fingerprint", "web_component", 
			"web_component_link"}

#write the correct column titles to the csv files
for key in columns_include:
	descriptions[key] = ()
	temp = []
	for innerkey in columns_include[key]:
		if(columns_include[key][innerkey] == 'y'):
			temp.append(innerkey)
	descriptions[key] = (temp)

file_exists = {} #create a new dictionary
file_exists['bitcoin_address'] = False
file_exists['bitcoin_address_link'] = False
file_exists['category'] = False
file_exists['category_link'] = False
file_exists['categorylink'] = False
file_exists['clone_group'] = False
file_exists['daily_stat'] = False
file_exists['domain'] = False
file_exists['email'] = False
file_exists['email_link'] = False
file_exists['headless_bot'] = False
file_exists['headlessbot'] = False
file_exists['open_port'] = False
file_exists['page'] = False
file_exists['page_link'] = False
file_exists['request_log'] = False
file_exists['search_log'] = False
file_exists['ssh_fingerprint'] = False
file_exists['web_component'] = False
file_exists['web_component_link'] = False

bitcoin_address_file = None
bitcoin_address_link_file = None
category_file = None
category_link_file = None
categorylink_file = None
clone_group_file = None
daily_stat_file = None
domain_file = None
email_file = None
email_link_file = None
headless_bot_file = None
headlessbot_file = None
open_port_file = None
page_file = None
page_link_file = None
request_log_file = None
search_log_file = None
ssh_fingerprint_file = None
web_component_file = None
web_component_link_file = None


#initilize files to store each of the tables
bitcoin_addressWriter = None
bitcoin_address_linkWriter = None
categoryWriter = None
category_linkWriter = None
categorylinkWriter = None
clone_groupWriter = None
daily_statWriter = None
domainWriter = None
emailWriter = None
email_linkWriter = None
headless_botWriter = None
headlessbotWriter = None
open_portWriter = None
pageWriter = None
page_linkWriter = None
request_logWriter = None
search_logWriter = None
ssh_fingerprintWriter = None
web_componentWriter = None
web_component_linkWriter = None

def open_files(Tables):
	global file_exists
	for name in Tables:
		filename = name + '.csv'
		if (os.path.isfile(filename)):
			file_exists[name] = True
			#print("file %s exists" % filename)
		else:
			#print("file %s DOES NOT EXIST" % name)
			file_exists[name] = False

def test_if_files_exist():
	global file_exists
	global bitcoin_address_file, bitcoin_addressWriter
	global bitcoin_address_link_file, bitcoin_address_linkWriter
	global category_file, categoryWriter
	global category_link_file, category_linkWriter
	global categorylink_file, categorylinkWriter
	global clone_group_file, clone_groupWriter
	global daily_stat_file, daily_statWriter
	global domain_file, domainWriter
	global email_file, emailWriter
	global email_link_file, email_linkWriter
	global headless_bot_file, headless_botWriter
	global headlessbot_file, headlessbotWriter
	global open_port_file, open_portWriter
	global page_file, pageWriter
	global page_link_file, page_linkWriter
	global request_log_file, request_logWriter
	global search_log_file, search_logWriter
	global ssh_fingerprint_file, ssh_fingerprintWriter
	global web_component_file, web_componentWriter
	global web_component_link_file, web_component_linkWriter
	if(file_exists['bitcoin_address'] == False):
		bitcoin_address_file = io.open('bitcoin_address.csv', 'w', newline='', encoding='utf-8')
		bitcoin_addressWriter = csv.writer(bitcoin_address_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		bitcoin_addressWriter.writerow(descriptions['bitcoin_address'])

	if(file_exists['bitcoin_address_link'] == False):
		bitcoin_address_link_file = io.open('bitcoin_address_link.csv', 'w', newline='', encoding='utf-8')
		bitcoin_address_linkWriter = csv.writer(bitcoin_address_link_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		bitcoin_address_linkWriter.writerow(descriptions['bitcoin_address_link'])

	if(file_exists['category'] == False):
		category_file = io.open('category.csv', 'w', newline='', encoding='utf-8')
		categoryWriter = csv.writer(category_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		categoryWriter.writerow(descriptions['category'])

	if(file_exists['category_link'] == False):
		category_link_file = io.open('category_link.csv', 'w', newline='', encoding='utf-8')
		category_linkWriter = csv.writer(category_link_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		category_linkWriter.writerow(descriptions['category_link'])

	if(file_exists['categorylink'] == False):
		categorylink_file = io.open('categorylink.csv', 'w', newline='', encoding='utf-8')
		categorylinkWriter = csv.writer(categorylink_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		categorylinkWriter.writerow(descriptions['categorylink'])

	if(file_exists['clone_group'] == False):
		clone_group_file = io.open('clone_group.csv', 'w', newline='', encoding='utf-8')
		clone_groupWriter = csv.writer(clone_group_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		clone_groupWriter.writerow(descriptions['clone_group'])

	if(file_exists['daily_stat'] == False):
		daily_stat_file = io.open('daily_stat.csv', 'w', newline='', encoding='utf-8')
		daily_statWriter = csv.writer(daily_stat_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		daily_statWriter.writerow(descriptions['daily_stat'])

	if(file_exists['domain'] == False):
		domain_file = io.open('domain.csv', 'w', newline='', encoding='utf-8')
		domainWriter = csv.writer(domain_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		domainWriter.writerow(descriptions['domain'])

	if(file_exists['email'] == False):
		email_file = io.open('email.csv', 'w', newline='', encoding='utf-8')
		emailWriter = csv.writer(email_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		emailWriter.writerow(descriptions['email'])

	if(file_exists['email_link'] == False):
		email_link_file = io.open('email_link.csv', 'w', newline='', encoding='utf-8')
		email_linkWriter = csv.writer(email_link_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		email_linkWriter.writerow(descriptions['email_link'])

	if(file_exists['headless_bot'] == False):
		headless_bot_file = io.open('headless_bot.csv', 'w', newline='', encoding='utf-8')
		headless_botWriter = csv.writer(headless_bot_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		headless_botWriter.writerow(descriptions['headless_bot'])

	if(file_exists['headlessbot'] == False):
		headlessbot_file = io.open('headlessbot.csv', 'w', newline='', encoding='utf-8')
		headlessbotWriter = csv.writer(headlessbot_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		headlessbotWriter.writerow(descriptions['headlessbot'])

	if(file_exists['open_port'] == False):
		open_port_file = io.open('open_port.csv', 'w', newline='', encoding='utf-8')
		open_portWriter = csv.writer(open_port_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		open_portWriter.writerow(descriptions['open_port'])

	if(file_exists['page'] == False):
		page_file = io.open('page.csv', 'w', newline='', encoding='utf-8')
		pageWriter = csv.writer(page_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		pageWriter.writerow(descriptions['page'])

	if(file_exists['page_link'] == False):
		page_link_file = io.open('page_link.csv', 'w', newline='', encoding='utf-8')
		page_linkWriter = csv.writer(page_link_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		page_linkWriter.writerow(descriptions['page_link'])

	if(file_exists['request_log'] == False):
		request_log_file = io.open('request_log.csv', 'w', newline='', encoding='utf-8')
		request_logWriter = csv.writer(request_log_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		request_logWriter.writerow(descriptions['request_log'])

	if(file_exists['search_log'] == False):
		search_log_file = io.open('search_log.csv', 'w', newline='', encoding='utf-8')
		search_logWriter = csv.writer(search_log_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		search_logWriter.writerow(descriptions['search_log'])

	if(file_exists['ssh_fingerprint'] == False):
		ssh_fingerprint_file = io.open('ssh_fingerprint.csv', 'w', newline='', encoding='utf-8')
		ssh_fingerprintWriter = csv.writer(ssh_fingerprint_file, delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		ssh_fingerprintWriter.writerow(descriptions['ssh_fingerprint'])

	if(file_exists['web_component'] == False):
		web_component_file = io.open('web_component.csv', 'w', newline='', encoding='utf-8')
		web_componentWriter = csv.writer(web_component_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		web_componentWriter.writerow(descriptions['web_component'])

	if(file_exists['web_component_link'] == False):
		web_component_link_file = io.open('web_component_link.csv', 'w', newline='', encoding='utf-8')
		web_component_linkWriter = csv.writer(web_component_link_file,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		web_component_linkWriter.writerow(descriptions['web_component_link'])

	

#flush files
def flush_files():
	if(file_exists['bitcoin_address'] == False):
		bitcoin_address_file.flush()
	if(file_exists['bitcoin_address_link'] == False):
		bitcoin_address_link_file.flush()
	if(file_exists['category'] == False):
		category_file.flush()
	if(file_exists['category_link'] == False):
		category_link_file.flush()
	if(file_exists['categorylink'] == False):
		categorylink_file.flush()
	if(file_exists['clone_group'] == False):
		clone_group_file.flush()
	if(file_exists['daily_stat'] == False):
		daily_stat_file.flush()
	if(file_exists['domain'] == False):
		domain_file.flush()
	if(file_exists['email'] == False):
		email_file.flush()
	if(file_exists['email_link'] == False):
		email_link_file.flush()
	if(file_exists['headless_bot'] == False):
		headless_bot_file.flush()
	if(file_exists['headlessbot'] == False):
		headlessbot_file.flush()
	if(file_exists['open_port'] == False):
		open_port_file.flush()
	if(file_exists['page'] == False):
		page_file.flush()
	if(file_exists['page_link'] == False):
		page_link_file.flush()
	if(file_exists['request_log'] == False):
		request_log_file.flush()
	if(file_exists['search_log'] == False):
		search_log_file.flush()
	if(file_exists['ssh_fingerprint'] == False):
		ssh_fingerprint_file.flush()
	if(file_exists['web_component'] == False):
		web_component_file.flush()
	if(file_exists['web_component_link'] == False):
		web_component_link_file.flush()

#line counts for each file
bitcoin_address_lineCount = 1
bitcoin_address_link_lineCount = 1
category_lineCount = 1
category_link_lineCount = 1 
categorylink_lineCount = 1
clone_group_lineCount = 1
daily_stat_lineCount = 1
domain_lineCount = 1
email_lineCount = 1
email_link_lineCount = 1 
headless_bot_lineCount = 1
headlessbot_lineCount = 1
open_port_lineCount = 1
page_lineCount = 1
page_link_lineCount = 1 
request_log_lineCount = 1
search_log_lineCount = 1
ssh_fingerprint_lineCount = 1 
web_component_lineCount = 1
web_component_link_lineCount = 1

def close_files():
	if(file_exists['bitcoin_address'] == False):
		bitcoin_address_file.close()
	if(file_exists['bitcoin_address_link'] == False):
		bitcoin_address_link_file.close()
	if(file_exists['category'] == False):
		category_file.close()
	if(file_exists['category_link'] == False):
		category_link_file.close()
	if(file_exists['categorylink'] == False):
		categorylink_file.close()
	if(file_exists['clone_group'] == False):
		clone_group_file.close()
	if(file_exists['daily_stat'] == False):
		daily_stat_file.close()
	if(file_exists['domain'] == False):
		domain_file.close()
	if(file_exists['email'] == False):
		email_file.close()
	if(file_exists['email_link'] == False):
		email_link_file.close()
	if(file_exists['headless_bot'] == False):
		headless_bot_file.close()
	if(file_exists['headlessbot'] == False):
		headlessbot_file.close()
	if(file_exists['open_port'] == False):
		open_port_file.close()
	if(file_exists['page'] == False):
		page_file.close()
	if(file_exists['page_link'] == False):
		page_link_file.close()
	if(file_exists['request_log'] == False):
		request_log_file.close()
	if(file_exists['search_log'] == False):
		search_log_file.close()
	if(file_exists['ssh_fingerprint'] == False):
		ssh_fingerprint_file.close()
	if(file_exists['web_component'] == False):
		web_component_file.close()
	if(file_exists['web_component_link'] == False):
		web_component_link_file.close()

#pass in the item from beginning parenthesis to end parenthesis
def parse_string(listItem):
	#loop through each character in the string
	#keep track of single quotes (')
		#don't count escaped quotes ("\'")
	#print item when single quotes are at 0 and a comma is found

	#store the sorted items in a list
	#return the list

	strings = []
	singleQuoteCount = 0
	prevChar = ''
	bufferString = ""
	containsCommas = False

	for character in listItem:
		if character == "'" and prevChar != "\\":
			singleQuoteCount += 1

		elif (character == ',' and (singleQuoteCount % 2) == 0):
			if containsCommas == True:
				#bufferString = '"' + bufferString + '"'

				tempString = '"'
				for char in bufferString:
					if char == ",":
						strings.append(tempString)
						tempString = ""
					else:
						tempString += char
				tempString += '"'
				strings.append(tempString)

			else:
				strings.append(bufferString)
			bufferString = ""
			containsCommas = False
			singleQuoteCount = 0

		elif character == ',' and prevChar:
			if singleQuoteCount %2 != 0:
				containsCommas = True
			bufferString += character
		else:
			bufferString += character
			

		if bufferString == "":
			prevChar = ''
		else:
			prevChar = character

	#print last word
	if containsCommas == True:
		bufferString = '"' + bufferString + '"'
	strings.append(bufferString)

	return strings

#Parse line by line a .txt file
def txt_parser(filename, keyword, delimiter):
    with io.open(filename, 'rtU', encoding='utf-8') as file:
        while True:
            chunk = file.read(1000)
            if chunk == '':
                return

            #lines = chunk.split("\n") #used for text
            #lines = chunk.split(")") #used for SQL dump
            if(delimiter != ""):
            	lines = chunk.split(delimiter)
            else:
            	lines = chunk

            for word in lines:
                if keyword in word:
                   print(word)


# The following are table names from the SQL dump we received
# Each function parses all input that relates to that table,
# and stores it in a manageable format

#AVAILABLE TABLES
#Bitcoin_address_link()
#category()
#category_link()
#categorylink()
#clone_group()
#daily_stat()
#domain()
#email()
#email_link()
#headless_bot()
#headlessbot()
#open_port()
#page()
#page_link()
#request_log()
#search_log()
#ssh_fingerprint()
#web_component()
#web_component_link()

def list_tables():
	print("TABLE LIST")
	print("bitcoin_address")
	print("Bitcoin_address_link")
	print("category")
	print("category_link")
	print("categorylink")
	print("clone_group")
	print("daily_stat")
	print("domain")
	print("email")
	print("email_link")
	print("headless_bot")
	print("headlessbot")
	print("open_port")
	print("page")
	print("page_link")
	print("request_log")
	print("search_log")
	print("ssh_fingerprint")
	print("web_component")
	print("web_component_link")

def bitcoin_address(listItem):
	global bitcoin_addressWriter
	global bitcoin_address_lineCount
	global descriptions
	global columns_include

	if (split_into_separate_files and (bitcoin_address_lineCount % max_rows_in_file) == 0):
		i = bitcoin_address_lineCount / max_rows_in_file
		bitcoin_addressWriter = csv.writer(open('bitcoin_address%s.csv' % int(i),'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL) 
		bitcoin_addressWriter.writerow(descriptions['bitcoin_address'])

	#print("FIXME bitcoin_address")
	strings = parse_string(listItem)

	#write the correct column titles to the csv files
	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	bitcoin_addressWriter.writerow(row)
	bitcoin_address_file.flush()

	bitcoin_address_lineCount += 1


def Bitcoin_address_link(listItem):
	#(
	#page - int(11),
	#bitcoin_address - int(11),
	#)
	#print("FIXME Bitcoin_address_link")

	global bitcoin_address_link_lineCount
	global bitcoin_address_linkWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (bitcoin_address_link_lineCount % max_rows_in_file) == 0):
		i = bitcoin_address_link_lineCount / max_rows_in_file
		bitcoin_address_linkWriter = csv.writer(open('bitcoin_address_link%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		bitcoin_address_linkWriter.writerow(descriptions['bitcoin_address_link'])

	strings = parse_string(listItem)
	page = strings[0]
	bitcoin_address = strings[1].strip("'")

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	bitcoin_address_linkWriter.writerow(row)
	bitcoin_address_link_file.flush()

	bitcoin_address_link_lineCount += 1

def category(listItem): # - low priority
	#(
	#id - int(11)
	#name - string
	#is_auto - tinyint(1)
	#created_at - datetime
	#)
	#print("FIXME category")

	global category_lineCount
	global categoryWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (category_lineCount % max_rows_in_file) == 0):
		i = category_lineCount / max_rows_in_file
		categoryWriter = csv.writer(open('category%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		categoryWriter.writerow(descriptions['category'])

	strings = parse_string(listItem)
	id = strings[0]
	name = strings[1]
	is_auto = strings[2]
	created_at = strings[3]

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	categoryWriter.writerow(row)
	category_file.flush()

	category_lineCount += 1

def category_link(listItem): # - low priority
	#(
	#domain - int(11),
	#category - int(11),
	#is_confirmed - tinyint(1),
	#is_valid - tinyint(1),
	#created_at - datetime
	#)
	#print("FIXME category_link")

	global category_link_lineCount
	global category_linkWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (category_link_lineCount % max_rows_in_file) == 0):
		i = category_link_lineCount / max_rows_in_file
		category_link_linkWriter = csv.writer(open('category_link%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		category_linkWriter.writerow(descriptions['category_link'])

	strings = parse_string(listItem)
	domain = strings[0]
	category = strings[1]
	is_confirmed = strings[2]
	is_valid = strings[3]
	created_at = strings[4]

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	category_linkWriter.writerow(row)
	category_link_file.flush()

	category_link_lineCount += 1

def categorylink(listItem):
	#(
	#id - int(11),
	#domain - int(11),
	#category - int(11),
	#is_valid - tinyint(1),
	#is_confirmed - tinyint(1),
	#created_at - datetime
	#)
	#print("FIXME categorylink")


	global categorylink_lineCount
	global categorylinkWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (categorylink_lineCount % max_rows_in_file) == 0):
		i = categorylink_lineCount / max_rows_in_file
		categorylink_linkWriter = csv.writer(open('categorylink%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		categorylinkWriter.writerow(descriptions['categorylink'])

	strings = parse_string(listItem)
	id = strings[0]
	domain = strings[1]
	category = strings[2]
	is_valid = strings[3]
	is_confirmed = strings[4]
	created_at = strings[5].strip("'")

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	categorylinkWriter.writerow(row)
	categorylink_file.flush()

	categorylink_lineCount += 1

def clone_group(listItem):
	#(
	#id - int(11)
	#)
	#print("FIXME clone_group")

	global clone_group_lineCount
	global clone_groupWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (clone_group_lineCount % max_rows_in_file) == 0):
		i = clone_group_lineCount / max_rows_in_file
		clone_group_linkWriter = csv.writer(open('clone_group%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		clone_groupWriter.writerow(descriptions['clone_group'])

	strings = parse_string(listItem)
	id = strings[0]

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	clone_groupWriter.writerow(row)
	clone_group_file.flush()

	clone_group_lineCount += 1

def daily_stat(listItem):
	#(
	#id - int(11),
	#created_at - datetime,
	#unique_visitors - int(11),
	#total_onions - int(11),
	#new_onions - int(11),
	#total_onions_all - int(11),
	#new_onions_all - int(11),
	#banned - int(11),
	#up_right_now - int(11),
	#up_right_now_all - int(11),
	#banned_up_last_24 - int(11)
	#)
	#print("FIXME daily_stat")

	global daily_stat_lineCount
	global daily_statWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (daily_stat_lineCount % max_rows_in_file) == 0):
		i = daily_stat_lineCount / max_rows_in_file
		daily_statWriter = csv.writer(open('daily_stat%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		daily_statWriter.writerow(descriptions['daily_stat'])

	strings = parse_string(listItem)
	id = strings[0]
	created_at = strings[1].strip("'")
	unique_visitors = strings[2]
	total_onions = strings[3]
	new_onions = strings[4]
	total_onions_all = strings[5]
	new_onions_all = strings[6]
	banned = strings[7]
	up_right_now = strings[8]
	up_right_now_all = strings[9]
	banned_up_last_24 = strings[10]

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	daily_statWriter.writerow(row)
	daily_stat_file.flush()

	daily_stat_lineCount += 1

def domain(listItem):
	#(
	#id - int(11),
	#host - string,
	#port - int(11),
	#ssl - tinyint(1),
	#is_up - tinyint(1),
	#created_at - datetime,
	#visited_at - datetime,
	#title - ,
	#last_alive - datetime,
	#is_crap - tinyint(1),
	#is_genuine - tinyint(1),
	#is_fake - tinyint(1),
	#ssh_fingerprint - int(11),
	#is_subdomain - tinyint(1),
	#server - string,
	#powered_by - string,
	#dead_in_a_row - int(11),
	#next_scheduled_check - datetime,
	#is_banned - tinyint(1),
	#portsscanned_at - datetime,
	#path_scanned_at - datetime,
	#useful_404_scanned_at - datetime,
	#useful_404 - tinyint(1),
	#useful_404_php - tinyint(1),
	#useful_404_dir - tinyint(1),
	#clone_group - int(11),
	#new_clone_group - int(11),
	#ban_exempt - tinyint(1),
	#manual_genuine - tinyint(1),
	#language - 2 letter string,
	#description_json - string,
	#description_json_at - datetime,
	#whatweb_at - datetime
	#)
	#print("FIXME domain")

	global domain_lineCount
	global domainWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (domain_lineCount % max_rows_in_file) == 0):
		i = domain_lineCount / max_rows_in_file
		domainWriter = csv.writer(open('domain%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		domainWriter.writerow(descriptions['domain'])

	strings = parse_string(listItem)#current line that is up for debate -- needs fixing somehow
	#how to deal with a title that contains commas? 
	#split by commas(,) unless a single quote is seen, then read until single quote followed by a comma
	#single quote must be escaped (\') if it is to be used other than to end the string
	for string in strings:
		string.strip("'")


	#id = strings[0]
	#host = strings[1].strip("'")
	#port = strings[2]
	#ssl = strings[3]
	#is_up = strings[4]
	# created_at = strings[5].strip("'")
	# visited_at = strings[6].strip("'")
	# title = strings[7].strip("'")
	# last_alive = strings[8].strip("'")
	# is_crap = strings[9]
	# is_genuine = strings[10]
	# is_fake = strings[11]
	# ssh_fingerprint = strings[12]
	# is_subdomain = strings[13]
	# server = strings[14].strip("'")
	# powered_by = strings[15].strip("'")
	# dead_in_a_row = strings[16]
	# next_scheduled_check = strings[17].strip("'")
	# is_banned = strings[18]
	# portsscanned_at = strings[19].strip("'")
	# path_scanned_at = strings[20].strip("'")
	# useful_404_scanned_at = strings[21].strip("'")
	# useful_404 = strings[22]
	# useful_404_php = strings[23]
	# useful_404_dir = strings[24]
	# clone_group = strings[25]
	# new_clone_group = strings[26]
	# ban_exempt = strings[27]
	# manual_genuine = strings[28]
	# language = strings[29].strip("'")
	# description_json = strings[30]
	# description_json_at = strings[31].strip("'")
	# whatweb_at = strings[32].strip("'")


	row = ()
	temp = []

	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)

	row = (temp)

	domainWriter.writerow(row)
	domain_file.flush()

	domain_lineCount += 1

def email(listItem): # - low priority
	#(
	#ID - int(11),
	#address - string
	#)
	#print("FIXME email")

	global email_lineCount
	global emailWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (email_lineCount % max_rows_in_file) == 0):
		i = email_lineCount / max_rows_in_file
		emailWriter = csv.writer(open('email%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		emailWriter.writerow(descriptions['email'])

	strings = parse_string(listItem)
	id = strings[0]
	address = strings[1]

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	emailWriter.writerow(row)
	email_file.flush()

	email_lineCount += 1

def email_link(listItem):
	#(
	# ID - int(11),
	#address - string
	#)
	#print("FIXME email_link")

	global email_link_lineCount
	global email_linkWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (email_link_lineCount % max_rows_in_file) == 0):
		i = email_link_lineCount / max_rows_in_file
		email_linkWriter = csv.writer(open('email_link%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		email_linkWriter.writerow(descriptions['email_link'])

	strings = parse_string(listItem)
	#id = strings[0]
	#address = strings[1].strip("'")

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)
	email_linkWriter.writerow(row)
	email_link_file.flush()

	email_link_lineCount += 1

def headless_bot(listItem):
	#(
	#uuid - string,
	#kind - string,
	#created_at - datetime
	#)
	#print("FIXME headless_bot")

	global headless_bot_lineCount
	global headless_botWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (headless_bot_lineCount % max_rows_in_file) == 0):
		i = headless_bot_lineCount / max_rows_in_file
		headless_botWriter = csv.writer(open('headless_bot%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		headless_botWriter.writerow(descriptions['headless_bot'])

	strings = parse_string(listItem)

	uuid = strings[0].strip("'")
	kind = strings[1].strip("'")
	created_at = strings[2].strip("'")

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	headless_botWriter.writerow(row)
	headless_bot_file.flush()

	headless_bot_lineCount += 1

def headlessbot(listItem): # - low priority
	#(
	#ID - int(11),
	#uuid - string,
	#kind - string,
	#created_at - datetime
	#)
	#print("FIXME headlessbot")

	global headlessbot_lineCount
	global headlessbotWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (headlessbot_lineCount % max_rows_in_file) == 0):
		i = headlessbot_lineCount / max_rows_in_file
		headlessbotWriter = csv.writer(open('headlessbot%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		headlessbotWriter.writerow(descriptions['headlessbot'])

	strings = parse_string(listItem)

	id = strings[0]
	uuid = strings[1]
	kind = strings[2]
	created_at = strings[3]

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	headlessbotWriter.writerow(row)
	headlessbot_file.flush()

	headlessbot_lineCount += 1

def open_port(listItem):
	#(
	#ID - int(11),
	#port - int(11),
	#domain - int(11)
	#)
	#print("FIXME open_port")

	global open_port_lineCount
	global open_portWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (open_port_lineCount % max_rows_in_file) == 0):
		i = open_port_lineCount / max_rows_in_file
		open_portWriter = csv.writer(open('open_port%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		open_portWriter.writerow(descriptions['open_port'])

	strings = parse_string(listItem)

	id = strings[0]
	port = strings[1]
	domain = strings[2]

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	open_portWriter.writerow(row)
	open_port_file.flush()

	open_port_lineCount += 1

def page(listItem): # - HIGH PRIORITY
	#rint("FIXME page")
	#TABLE STRUCTURE
	#( 
	#id - int(11), 
	#url - string,  - in single quotes
	#title - string, - in single quotes
	#code - int(11), 
	#domain - int(11), 
	#created_at - datetime, - in single quotes
	#visited_at - datetime, - in single quotes
	#is_frontpage - tinyint(1),
	#size - int(11),
	#path - string, - in single quotes
	#)
	#listItem = listItem[1:-1] #trim the parenthesis off the beginning and end
	global page_lineCount
	global pageWriter
	global split_into_separate_files
	global descriptions
	global columns_include

	if(split_into_separate_files and (page_lineCount % max_rows_in_file) == 0):
		i = page_lineCount / max_rows_in_file
		pageWriter = csv.writer(open('page%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		pageWriter.writerow(descriptions['page'])

	strings = parse_string(listItem) # separate the list items by commas

	id = strings[0]
	url = strings[1].strip("'")
	title = strings[2].strip("'")
	code = strings[3]
	domain = strings[4]
	created_at = strings[5].strip("'")
	visited_at = strings[6].strip("'")
	is_frontpage = strings[7]
	size = strings[8]
	path = strings[9].strip("'")
	#pageWriter.writerow([id,url,title,code,domain,created_at,visited_at,is_frontpage,size,path])
	
	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	pageWriter.writerow(row)
	page_file.flush()

	page_lineCount += 1

def page_link(listItem):
	#(
	#link_from - int(11),
	#link_to - int(11)
	#)
	#print("FIXME page_link")

	global page_link_lineCount
	global page_linkWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (page_link_lineCount % max_rows_in_file) == 0):
		i = page_link_lineCount / max_rows_in_file
		page_linkWriter = csv.writer(open('page_link%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		page_linkWriter.writerow(descriptions['page_link'])

	strings = parse_string(listItem)

	link_from = strings[0]
	link_to = strings[1]

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	page_linkWriter.writerow(row)
	page_link_file.flush()

	page_link_lineCount +=1

def request_log(listItem):
	#LOOK INTO MORE FOR EXAMPLE --- FIXME
	#(
	#id - int(11),
	#uuid - string,
	#uuid_is_fresh - tinyint(1),
	#created_at - datetime,
	#agent - string,
	#path - string,
	#full_path - string,
	#referrer - string
	#)
	#print("FIXME request_log")

	global request_log_lineCount
	global request_logWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (request_log_lineCount % max_rows_in_file) == 0):
		i = request_log_lineCount / max_rows_in_file
		request_logWriter = csv.writer(open('request_log%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		request_logWriter.writerow(descriptions['request_log'])

	strings = parse_string(listItem)

	id = strings[0]
	uuid = strings[1]
	uuid_is_fresh = strings[2]
	created_at = strings[3]
	agent = strings[4]
	path = strings[5]
	full_path = strings[6]
	referrer = strings[7]

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	request_logWriter.writerow(row)
	request_log_file.flush()

	request_log_lineCount += 1

def search_log(listItem):
	#LOOK INTO MORE FOR EXAMPLE -- FIXME
	#(
	#ID - int(11),
	#uuid - string,
	#uuid_is_fresh - tinyint(1),
	#created_at - datetime,
	#agent - string,
	#path - string,
	#full_path - string,
	#referrer - string
	#)
	#print("FIXME search_log")

	global search_log_lineCount
	global search_logWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (search_log_lineCount % max_rows_in_file) == 0):
		i = search_log_lineCount / max_rows_in_file
		search_logWriter = csv.writer(open('search_log%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		search_logWriter.writerow(descriptions['search_log'])

	strings = parse_string(listItem)
	#id = strings[0]
	#uuid = strings[1]
	#uuid_is_fresh = strings[2].strip("'")
	#created_at = strings[3]
	#agent = strings[4].strip("'")
	#path = strings[5].strip("'")
	#full_path = strings[6].strip("'")
	#referrer = strings[7]

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	search_logWriter.writerow(row)
	search_log_file.flush()

	search_log_lineCount += 1

def ssh_fingerprint(listItem):
	#(
	#ID - int(11),
	#fingerprint - string
	#)
	#print("FIXME ssh_fingerprint")

	global ssh_fingerprint_lineCount
	global ssh_fingerprintWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (ssh_fingerprint_lineCount % max_rows_in_file) == 0):
		i = ssh_fingerprint_lineCount / max_rows_in_file
		ssh_fingerprintWriter = csv.writer(open('ssh_fingerprint%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		ssh_fingerprintWriter.writerow(descriptions['ssh_fingerprint'])

	strings = parse_string(listItem)

	id = strings[0]
	fingerprint = strings[1].strip("'")

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	ssh_fingerprintWriter.writerow(row)
	ssh_fingerprint_file.flush()

	ssh_fingerprint_lineCount += 1

def web_component(listItem):
	#(
	#ID - int(11),
	#name - string,
	#version - string,
	#account - string
	#string - string
	#)
	#print("FIXME web_component")

	global web_component_lineCount
	global web_componentWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (web_component_lineCount % max_rows_in_file) == 0):
		i = web_component_lineCount / max_rows_in_file
		web_componentWriter = csv.writer(open('web_component%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		web_componentWriter.writerow(descriptions['web_component'])

	strings = parse_string(listItem)

	id = strings[0]
	name = strings[1].strip("'")
	version = strings[2].strip("'")
	account = strings[3].strip("'")
	string = strings[4].strip("'")

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	web_componentWriter.writerow(row)
	web_component_file.flush()

	web_component_lineCount += 1

def web_component_link(listItem):
	#(
	#web_component - int(11),
	#domain - int(11)
	#)
	#print("FIXME web_component_link")

	global web_component_link_lineCount
	global web_component_linkWriter
	global descriptions
	global columns_include

	if(split_into_separate_files and (web_component_link_lineCount % max_rows_in_file) == 0):
		i = web_component_link_lineCount / max_rows_in_file
		web_component_linkWriter = csv.writer(open('web_component_link%s.csv' % int(i), 'w', newline='', encoding='utf-8'),delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		web_component_linkWriter.writerow(descriptions['web_component_link'])

	strings = parse_string(listItem)
	
	web_component = strings[0]
	domain = strings[1]

	row = ()
	temp = []
	for string in strings:
		if(string.startswith("'") and string.endswith("'")):
			string = string[1:-1]
		temp.append(string)
	row = (temp)

	web_component_linkWriter.writerow(row)
	web_component_link_file.flush()

	web_component_link_lineCount += 1


#function for text processing
def read_text(Tables): # - HIGH PRIORITY

	filename = input("FileName: ")
	if not(os.path.isfile(filename)):
		print("Error: File does not exist")
		return

	notifyNumber = input("Update user every (# words): ")

	try:
		int(notifyNumber)
	except:
		print("Error: Not a number.")
		return
	
	notifyNumber = int(notifyNumber)

	#variable to track how many lines each file has
	#max for an excel sheet is 1,048,576 rows or 16,384 columns
	global bitcoin_address_lineCount
	global Bitcoin_address_link_lineCount
	global category_lineCount 
	global category_link_lineCount 
	global categorylink_lineCount 
	global clone_group_lineCount 
	global daily_stat_lineCount
	global domain_lineCount 
	global email_lineCount 
	global email_link_lineCount 
	global headless_bot_lineCount 
	global headlessbot_lineCount
	global open_port_lineCount 
	global page_lineCount 
	global page_link_lineCount 
	global request_log_lineCount
	global search_log_lineCount 
	global ssh_fingerprint_lineCount 
	global web_component_lineCount 
	global web_component_link_lineCount

	if bitcoin_address_lineCount is None:
		bitcoin_address_lineCount = 1 #wrote column titles already

	if Bitcoin_address_link is None:
		Bitcoin_address_link_lineCount = 1

	if category_lineCount is None:
		category_lineCount = 1

	if category_link_lineCount is None:
		category_link_lineCount = 1

	if categorylink_lineCount is None:
		categorylink_lineCount = 1

	if clone_group_lineCount is None:
		clone_group_lineCount = 1

	if daily_stat_lineCount is None:
		daily_stat_lineCount = 1

	if domain_lineCount is None:
		domain_lineCount = 1

	if email_lineCount is None:
		email_lineCount = 1

	if email_link_lineCount is None:
		email_link_lineCount = 1

	if headless_bot_lineCount is None:
		headless_bot_lineCount = 1

	if headlessbot_lineCount is None:
		headlessbot_lineCount = 1

	if open_port_lineCount is None:
		open_port_lineCount = 1

	if page_lineCount is None:
		page_lineCount = 1

	if page_link_lineCount is None:
		page_link_lineCount = 1

	if request_log_lineCount is None:
		request_log_lineCount = 1

	if search_log_lineCount is None:
		search_log_lineCount = 1

	if ssh_fingerprint_lineCount is None:
		ssh_fingerprint_lineCount = 1

	if web_component_lineCount is None:
		web_component_lineCount = 1

	if web_component_link_lineCount is None:
		web_component_link_lineCount = 1

	with io.open(filename, 'rtU', encoding='utf-8') as file:

		#variables for determining when a new table has started
		tableName = ''
		bufferText = ""

		#variables for processing a table item
		balanced = True # - parenthesis layer == 0 is balanced
		parenthesisLayer = 0 # how many open ( seen
		text = "" # line to be used
		trackChar = False # - keep characters in buffer
		tableRead = False

	#	variable for telling the user how progress is going
		wordCount = 0;
		tableWordCount = 0;

		insertSeen = False
		valuesSeen = False
		ignoreInput = False

		singleQuoteBalanced = True 
		doubleQuoteBalanced = True

		prevChar = ""

		while True:
			char = file.read(1)
			if not char:
				if tableName != "":
					print("Final Table Entries Count: ", "{:,}".format(tableWordCount))	
				return

			bufferText += char

			if("VALUES" in bufferText):
				valuesSeen = True

			if(tableRead == True and char == '`' and parenthesisLayer == 0):
				#print('should change table name?')
				temp = bufferText.replace(' ', '')
				temp = temp[1:-1]
				temp = temp.lower()
				if temp in Tables:
					if temp != tableName:
						#print('yes.')
						if tableName != "":
							print("Final Table Entries Count: ", "{:,}".format(tableWordCount))	
						tableName = temp
						print("Current Table = " + tableName)
						tableWordCount = 0
			elif char == '`':
				tableRead = True

			#clear the buffer
			if (char == ' ' or char == '\n'):
				bufferText = ""
			#END FUNCTION FOR FINDING THE CURRENT TABLES

			#find a list item in the table
			if(char == '(' and parenthesisLayer == 0 and valuesSeen == False and prevChar != ','):
				ignoreInput = True
			elif(char == '(' and parenthesisLayer == 0 and valuesSeen == True):
				ignoreInput = False
				text = ""

			if (char == '(' and doubleQuoteBalanced == True and singleQuoteBalanced == True):
				balanced = False
				parenthesisLayer += 1
				trackChar = True
				
			if trackChar == True:
				text += char

			if (char == '"' and trackChar):
				#print("Char : %c " % char + " BufferText: %s" % bufferText)
				if(doubleQuoteBalanced == True):
					doubleQuoteBalanced = False
				else:
					doubleQuoteBalanced = True

			if (char == "'" and trackChar):
				#print("Char : %c " % char + " BufferText: %s" % bufferText)
				if(singleQuoteBalanced == True):
					singleQuoteBalanced = False
				else:
					singleQuoteBalanced = True


			if (char == ')' and doubleQuoteBalanced == True and singleQuoteBalanced == True):
				parenthesisLayer -= 1
				if(parenthesisLayer == 0):
					balanced = True
					trackChar = False

			if(char != ' ' and char != '(' and char != ')' and char !=',' and parenthesisLayer == 0 and ignoreInput == False):
				valuesSeen = False
				ignoreInput = True
				#print("2nd IGNORE INPUT SET TO TRUE")
			
			if(parenthesisLayer == 0):
				temp = text[1:-1]
				if(temp is ""):
					text = ""

			if (balanced == True) and (text is not "") and (singleQuoteBalanced == True) and (doubleQuoteBalanced == True):# and (ignoreInput == False):
				text = text[1:-1] #trim the parenthesis off the beginning and end

				wordCount += 1;
				tableWordCount += 1
				if((notifyNumber > 0) and (wordCount % notifyNumber == 0)):
					print("Total Words Parsed: ", "{:,}".format(wordCount),"...", "\tCurrent Table Entries: ", "{:,}".format(tableWordCount), "...")
				# process text
				#print text

				#actually process text according to its pattern/current table pattern
				if (tableName == "bitcoin_address" and file_exists[tableName] == False):	
					bitcoin_address(text)
				elif (tableName == "bitcoin_address_link" and file_exists[tableName] == False):
					Bitcoin_address_link(text)
				elif (tableName == "category" and file_exists[tableName] == False):
					category(text)
				elif (tableName == "category_link" and file_exists[tableName] == False):
					category_link(text)
				elif (tableName == "categorylink" and file_exists[tableName] == False):
					categorylink(text)
				elif (tableName == "clone_group" and file_exists[tableName] == False):
					clone_group(text)
				elif (tableName == "daily_stat" and file_exists[tableName] == False):
					daily_stat(text)
				elif (tableName == "domain" and file_exists[tableName] == False):
					domain(text)
				elif (tableName == "email" and file_exists[tableName] == False):
					email(text)
				elif (tableName == "email_link" and file_exists[tableName] == False):
					email_link(text)
				elif (tableName == "headless_bot" and file_exists[tableName] == False):
					headless_bot(text)
				elif (tableName == "headlessbot" and file_exists[tableName] == False):
					headlessbot(text)
				elif (tableName == "open_port" and file_exists[tableName] == False):
					open_port(text)
				elif (tableName == "page" and file_exists[tableName] == False):
					page(text)
				elif (tableName == "page_link" and file_exists[tableName] == False):
					page_link(text)
				elif (tableName == "request_log" and file_exists[tableName] == False):
					request_log(text)
				elif (tableName == "search_log" and file_exists[tableName] == False):
					search_log(text)
				elif (tableName == "ssh_fingerprint" and file_exists[tableName] == False):
					ssh_fingerprint(text)
				elif (tableName == "web_component" and file_exists[tableName] == False):
					web_component(text)
				elif (tableName == "web_component_link" and file_exists[tableName] == False):
					web_component_link(text)

				text = "" #clear text
				prevChar = char


#command prompt + setup?
#Possible commands
#s - search for a keyword
#l - list tables
#m - display menu
#r - run complete file parsing
#q - quit
#table name - parses the information stored in that table
commands = {"s","l","m", "r", "q"}

#Tables = {"bitcoin_address", "bitcoin_address_link", "category", "category_link",
#			"categorylink", "clone_group", "daily_stat", "domain", "email", "email_link",
#			"headless_bot", "headlessbot", "open_port", "page_link", "page",
#			"request_log", "search_log", "ssh_fingerprint", "web_component", 
#			"web_component_link"}

def get_command(commands):
	print("Enter a command.")
	print("s - search for a keyword")
	print("l - list Tables")
	print("m - display Menu")
	print("r - run complete file parsing")
	print("q - quit")
	command = input("Command: ")

	while (command not in commands):# and command not in Tables):
		print("invalid command")
		print("Enter a command.")
		command = input("Command: ")
	return command

def process_command(command):
	#command doesn't repeat
	if command is "s":
		filename = input("FileName: ")
		if not(os.path.isfile(filename)):
			print("Error: File does not exist")
			return

		keyword = input("Keyword: ")
		delimiter = input("Delimiter (type 'newline' to split by line): ")

		if(delimiter == "newline"):
			delimiter = "\n"

		txt_parser(filename, keyword, delimiter)
	elif command is "l":
		list_tables()
	elif command is "m":
		print("MENU")
		print("s - search for a keyword")
		print("l - list Tables")
		print("m - display Menu")
		print("r - run complete file parsing")
		print("q - quit")
	elif command is "r":
		read_text(Tables)
	elif command is "q":
		return
	elif (command in Tables):
		read_text(Tables)
	else:
		print("unknown command")

def run():
	open_files(Tables)
	test_if_files_exist()
	flush_files()
	command = get_command(commands)
	while(command is not "q"):
		process_command(command)
		command = get_command(commands)
		print()
		break
	close_files()

run()