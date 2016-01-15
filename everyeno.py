#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import time
import discogs_client
import tweepy
import urllib
import mmap
import pytumblr
from everyeno_keys import *

client = pytumblr.TumblrRestClient(tumblr_consumer_key, tumblr_consumer_secret, tumblr_token_key, tumblr_token_secret)
auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_token_key, twitter_token_secret)
api = tweepy.API(auth)
discogs = discogs_client.Client('EveryEno/0.3', user_token=discogs_user_token)

results = discogs.search('Brian Eno',type='master') # This search will return all master releases 

basedir = '/home/vgan/everyeno/' # set this to the working directory for the script
releasesfilepath = basedir + 'releases.csv'
thumbfile = basedir + 'thumb.jpg'
thumbobj = 'nope'
tweetedfilepath = basedir + 'tweeted.txt'
video_url = 'nope'
now = time.strftime("%c")
emoji_discogs = unicode('\xF0\x9F\x93\x96', 'utf-8')
emoji_video = unicode('\xF0\x9F\x93\xBA', 'utf-8')
emoji_year =  unicode('\xF0\x9F\x93\x86', 'utf-8')
emoji_title = unicode('\xF0\x9F\x8E\xB6', 'utf-8')

if not os.path.isfile(tweetedfilepath): # create the tweeted.txt file if it doesnt exist  
	tweetedfile = open(tweetedfilepath,"w")
	tweetedfile.write('MASTER_URLS\n') # write a header and close file
        tweetedfile.close()

def doTweet():
	if thumbobj == 'nope':
		try: # no thumbnail just tweet info and link
                        tweetbody = + emoji_title + ": " + title + "\n" + emoji_year + ": " + year + "\n" + emoji_discogs + ": " + discogs_url + "\n"   
                        status = api.update_status(status=tweetbody)
                        print now + ' tweeted without tumbnail: ' + title
        	except:
                 	print now + ' no thumbnail tweet failed: ' + title
	else:
                try:    # yes thumbnail
                	tweetbody = emoji_title + ": " + short_title + "\n" + emoji_year + ": " + year + "\n" + emoji_discogs + ": " + discogs_url + "\n" + emoji_video + ": " + video_url   
                	status = api.update_with_media(thumbfile,status=tweetbody,file=thumbobj)
                	print now + ' tweeted: ' + title
                except: 
                        print now + ' tweet with thumbnail failed: ' + title + "\n"

def doTumblr():  # check if we should do vdeo post or just picture
        if video_url == 'nope':
		try:
			client.create_photo('everyeno', state="published", tags=["Every Eno", "Brian Eno", year, "Discogs API", "Music Geek"], caption=title + "\n" + year + "\n"+ discogs_url + "\n" , link=discogs_url, data=thumbfile)
			print now + ' tumblrd photo post: ' + title
		except:
			print now + " tumblr photo post failed: " + title
	else:
		try:
        		client.create_video('everyeno', state="published", tags=["Every Eno", "Brian Eno", year , "Discogs","Discogs API","Music Geek"], caption=title + "\n" + year + "\n" + discogs_url + "\n", embed=video_url)
			print now + ' tumblrd video post: ' + title
        	except:
        		print now + ' tumblr video post failed: ' + title

if os.path.isfile(releasesfilepath): # releases.csv file exists - do some stuff
	with open(releasesfilepath) as releasesfile:
		tweetedfile = open(tweetedfilepath,"a+") # open tweetlog for appending
		m = mmap.mmap(tweetedfile.fileno(), 0, access=mmap.ACCESS_READ) # memory map the tweetlog
		for line in releasesfile: # start release loop
			release = line.split(",")
			year = str(release[0])
			title = str(release[1])
			discogs_url = release[2]
			video_url = release[4]
			if m.find(discogs_url) == -1: # master url has not been tweeted yet
				try: # download thumbnail
                                	thumb = release[3]
                                	urllib.urlretrieve(thumb, thumbfile)
                                	thumbobj = open(thumbfile)
                       		except:
                                	thumbobj = 'nope'
                                	
				except:
					print now + ' google search failed.'
					video_url = 'nope'

				if len(title) >= 48:  # truncate title to first 48 characters + elipses (this is the space leftover from image + 2 URLs, emoji, etc..)
					short_title = title[:48] + "..." 
				else:
					short_title = title

				doTweet()
				doTumblr()
				tweetedfile.write(release[2] + '\n') # write master url to tweeted file
				print now + ' cleaning up and exiting script...'
                                tweetedfile.close() # close tweeted.txt file
				os.remove(thumbfile)# delete thumbnail file
				quit() 
			#else:
				# print 'already tweeted this one, skipping ' + title 

else: # no releases.csv file - lets make one
	totalreleases = len(results) # might be able to use this later for comparing with local file and downloading updates?
	print('total releases: ' + str(totalreleases))
	releasesfile = open(releasesfilepath,"w") # create the file since it doesnt exist	
        releasesfile.close()
	releasesfile = open(releasesfilepath,"a+") # open for appending
	for result in results:
		#print result.data.keys()
		title = result.title.encode('ascii',errors='ignore') # encode to ascii to clean up weird characters in title, will still require some cleanup 
		title = title.replace(',', '-') # better replace commas since we are using as delimeter 
		try: 
			URL = result.data['uri']
			URL = 'http://www.discogs.com' + URL
		except:
			print now + ' error grabbing release.master.id'
		try:
 			year = str(result.data['year'])
		
		except:
			print now + ' error getting year'
			year = "0"
		thumb = result.data['thumb']
                try:
                        video_url = result.videos[0].data['uri']
                except:
                        video_url = 'nope'		
		releasesfile.write(year + ',' + title + ',' + URL + ',' + thumb + ',' + video_url + '\n')
	 	time.sleep(1)	
	releasesfile.close()
	print now + ' releases.csv has been created. you should manually clean it up / sort it before running again - i was missing lots of years for releases in my case...'
