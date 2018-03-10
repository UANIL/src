import io
import os.path

#Author: Austin Rife
#Date: 26 February 2018

#can find a table format
#can also find an example of the output
#can work for a specific table or all table names

#Parse line by line a .txt file
def data_finder(filename, tableName, delimiter, exampleType):
    with io.open(filename, 'rtU', encoding='utf-8') as file:
        while True:
            chunk = file.read(4096)
            if chunk == '':
                return

            if(delimiter != ""):
            	lines = chunk.split(delimiter)
            else:
            	lines = chunk

            for word in lines:
                if(tableName == ''):
                    if(exampleType == "Table Format"):
                       searchString = "CREATE TABLE `"
                       if(searchString in word):
                            startIndex = word.find(searchString)
                            tableFormat = parse_text(startIndex, word)
                            print(tableFormat)
                    elif(exampleType == "Example Output"):
                        searchString = "INSERT INTO `"
                        if(searchString in word):
                            startIndex = word.find(searchString)
                            outputExample = parse_text(startIndex, word)
                            print(outputExample)

                elif tableName in word:

                    #discover given table format
                    if(exampleType == "Table Format"):
                        searchString = "CREATE TABLE `" + tableName + "`"

                        if(searchString in word):
                            startIndex = word.find(searchString)
                            tableFormat = parse_text(startIndex, word)
                            print(tableFormat)

                    #discover given table example
                    elif (exampleType == "Example Output"):
                        searchString = "INSERT INTO `" + tableName + "` VALUES"
                        if(searchString in word):
                            startIndex = word.find(searchString)
                            outputExample = parse_text(startIndex, word)
                            print(outputExample)


def parse_text(startIndex, word):
    #from the given index, find the contents of the next parenthesis
    index = startIndex
    parenthesisLayer = 0
    trackChar = False
    completeText = False
    text = ""
    maxIndex = len(word)

    while True:
        #print("Index : ",index)
        if(index == maxIndex):
            print("ERROR: Unexpected data format")
            return
        char = word[index]
        text += char

        if(char == '('):
            parenthesisLayer += 1
            trackChar = True

        if(char == ")"):
            parenthesisLayer -= 1
            if(parenthesisLayer == 0):
                trackChar = False
                completeText = True

        if parenthesisLayer == 0 and completeText == True:
            return text

        index +=1          
                        

filename = input("Filename: ")
if not(os.path.isfile(filename)):
    print("Error: File does not exist")
    exit(0)

tableName = input("Table Name (leave blank if unknown): ")

exampleType = input("'Table Format' or 'Example Output': ")

if(exampleType != "Table Format" and exampleType != "Example Output"):
    print("Error: unknown search type")
    exit(0)

delimiter = ""#input("Delimiter (type 'newline' to split by line): ")
if(exampleType == "Table Format"):
    delimiter = ';'

elif (exampleType == "Example Output"):
    delimiter = '\n'

data_finder(filename,tableName,delimiter, exampleType)