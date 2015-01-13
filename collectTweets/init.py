from twitter import *
from lxml import html
import requests
from time import sleep
import datetime
import fileinput
import json
import os


#save the time at which our program starts
start = datetime.datetime.now().time()

#intitialize OAuth 
auth = OAuth(
    consumer_key = 'F7kxDzbq9In9ZPCMh8LxoQ',
    consumer_secret = 'pdOBdaCK0HfdCyLsgInjrlwAqU2NM44gpL1L4Gg3s',
    token = '47515689-m5aR9v3m0ia9gGUqUfn52I7jmKkUpsDOJtBm3TQim',
    token_secret = '0DKCQE1pGGJ4sEAUP7JZKDBYIxwDeG3SigkjnQZJw86Gs'
)

#setup file we will write to
currFile = 5 #0
fileNameStruc = ['DB/tweetDB_', str(currFile), '.json']
fileName = ''.join(fileNameStruc)
tweetDB = open(fileName, 'a')

#file size must not be larger than 10MB (10485760 Bytes)
maxFileSize = 30000#10485760 #421888 
#number of files we expect to collect for a total of 5GB of data (5GB data/ 10MB per file = 512 files)
maxNumFiles = 6 #520

#initialise Twitter Stream, using FIREHOSE
public_stream = TwitterStream(auth=auth, domain='stream.twitter.com')
"""
while currFile < maxNumFiles:
	#iterator to parse through twitter stream
	iterator = public_stream.statuses.sample()
	for tweet in iterator:
		#check if we've collected enough data!
		if currFile > maxNumFiles:
			tweetDB.close()
			break

		#size of file must be less than 10MB (10485760 Bytes)
		statinfo = os.stat(fileName)

		#if file size is larger, then create a new file
		while statinfo.st_size > maxFileSize:
			tweetDB.close()
			currFile += 1
			fileNameStruc = ['DB/tweetDB_', str(currFile), '.json']
			fileName = ''.join(fileNameStruc)
			tweetDB = open(fileName, 'a')
			statinfo = os.stat(fileName)

		#takes python objects (WrapperTwitterResponse) and serializes it into JSON string
		jdataString = json.dumps(tweet) 
		#takes JSON string and turns it into a python dictionary!
		jdataDict = json.loads(jdataString) 

		#only need to save Text, Timestamp, Geolocation, User of Tweet, and Links
		try:
			if jdataDict['coordinates'] != None:
				link = ''
				for item in jdataDict['entities']['urls']:
					link = item['expanded_url']

				tweetDB.write(json.dumps(
					{
						'text': jdataDict['text'], 
						'timestamp': jdataDict['created_at'],
						'geoJSON': jdataDict['coordinates'],
						'useroftweet': jdataDict['user']['screen_name'],
						'link': link,
						'linktitle': ''
					})+ '\n')
		except KeyError:
			continue

		#stats for development use
		os.system('clear')
		print 'START ' + str(start)
		print 'CURR  ' + str(datetime.datetime.now().time())
		print '\n'
		print 'Current File ' + str(currFile)
		print 'File Size ' + str(statinfo.st_size) + ' bytes'
		print '    <     ' + str(maxFileSize) + ' bytes'

	if currFile < maxNumFiles:
		print 'connection timedout: waiting 5 minutes to restart connection'
		sleep(300)

print 'DONE COLLECTING TWEETS!'
"""

print 'PROCESSING: SECOND PASS TO LOAD LINK TITLES...'

#goinng through the files in tweetDB, get the file name as a string
for x in range(5,currFile):
	fileNameStruc = ['./DB/tweetDB_',str(x),'.json']
	fileName = ''.join(fileNameStruc)

	#open up the file using file.input and traverse every line
	for line in fileinput.input(fileName,inplace=1):
		#make the string a dictionary
		jdataDict = json.loads(line)
		#if 'link' is not empty go to link page and retrieve title using requests
		if jdataDict['link'] != '':
			page = requests.get(jdataDict['link'])
			tree = html.fromstring(page.text)
			#store the title
			title = tree.xpath('//title/text()')
			#update the 'linktitle' field, if it fails leave it blank
			try:
				jdataDict['linktitle'] = title[0]
			except:
				jdataDict['linktitle'] = ''
			#make the dictionary into a string, print back into the file
			updatedstring = json.dumps(jdataDict) 
			print updatedstring
		else:
			print line.replace('\n','')

print 'TWEET COLLECTION DONE'
