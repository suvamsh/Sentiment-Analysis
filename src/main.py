import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy
from dateutil import parser
import Tkinter
import json
import unicodedata
import urllib
import httplib2
import re
import copy
import os
import Image, ImageTk

global goog_line
global aapl_line
global msft_line
goog_line = ()
aapl_line = ()
msft_line = ()
global goog_t
global msft_t
global aapl_t
global goog_sz
global aapl_sz
global msft_sz
goog_t = 0
msft_t = 0
aapl_t = 0


def goog_update(data):
    	goog_line.set_ydata(data)
    	return goog_line,

def aapl_update(data):
    	aapl_line.set_ydata(data)
    	return aapl_line,

def msft_update(data):
    	msft_line.set_ydata(data)
    	return msft_line,

def goog_data_gen():
    while True: 
    	global goog_t
    	goog_cpy = []
    	global goog_movavg
    	for i in range(goog_t):
    		goog_cpy.append(goog_movavg[i])

    	for i in range(goog_t,goog_sz):
    		goog_cpy.append(0)
    	goog_t = goog_t + 1
    	yield goog_cpy

def aapl_data_gen():
    while True: 
    	global aapl_t
    	aapl_cpy = []
    	global aapl_movavg
    	for i in range(aapl_t):
    		aapl_cpy.append(aapl_movavg[i]*10)

    	for i in range(aapl_t,aapl_sz):
    		aapl_cpy.append(0)
    	aapl_t = aapl_t + 1
    	yield aapl_cpy


def msft_data_gen():
    while True: 
    	global msft_t
    	msft_cpy = []
    	global msft_movavg
    	for i in range(msft_t):
    		#print msft_movavg[i]
    		msft_cpy.append(msft_movavg[i]*10)

    	for i in range(msft_t,msft_sz):
    		msft_cpy.append(0)
    	msft_t = msft_t + 1
    	yield msft_cpy

def aaplMoveAvg():
	data2 = numpy.recfromcsv('stock_data/aapl.csv', delimiter=',')
	aapl_clsPrice = []
	aapl_date = []
	global aapl_movavg 
	aapl_movavg = []

	for i in range(len(data2)):
		aapl_clsPrice.append(data2[i][6])
		aapl_date.append(data2[i][0])

	aapl_clsPrice.reverse()
	aapl_date.reverse()
	aapl_movavg = numpy.convolve(aapl_clsPrice, numpy.ones(10)/10)

	for i in range(10):
		if i == 0 :
			continue
		aapl_movavg[len(aapl_movavg) - i] = aapl_movavg[len(aapl_movavg) - 10]

	global aapl_line

	global aapl_sz
	aapl_sz = len(aapl_movavg)
	aapl_fig, aapl_ax = plt.subplots()
	aapl_line, = aapl_ax.plot(aapl_movavg, "bo")
	aapl_ax.set_ylim(10, 500)
	aapl_ax.set_xlim(0, 2000)
	aapl_ani = animation.FuncAnimation(aapl_fig, aapl_update, aapl_data_gen, interval=100)
	plt.ylabel('Price')
	plt.xlabel('Time')
	plt.show()

def msftMoveAvg():
	data1 = numpy.recfromcsv('stock_data/msft.csv', delimiter=',')
	msft_clsPrice = []
	msft_date = []
	global msft_movavg 
	msft_movavg = []
	
	for i in range(len(data1)):
		msft_clsPrice.append(data1[i][6])
		msft_date.append(data1[i][0])

	msft_clsPrice.reverse()
	msft_date.reverse()
	msft_movavg = numpy.convolve(msft_clsPrice, numpy.ones(10)/10)

	for i in range(10):
		if i == 0 :
			continue
		msft_movavg[len(msft_movavg) - i] = msft_movavg[len(msft_movavg) - 10]

	global msft_line
	global msft_sz
	msft_sz = len(msft_movavg)
	msft_fig, msft_ax = plt.subplots()
	msft_line, = msft_ax.plot(msft_movavg, "bo")
	msft_ax.set_ylim(0.3, 20)
	msft_ax.set_xlim(0, 2000)
	msft_ani = animation.FuncAnimation(msft_fig, msft_update, msft_data_gen, interval=100)	
	plt.ylabel('Price')
	plt.xlabel('Time')
	plt.show()

def googMoveAvg():
	data3 = numpy.recfromcsv('stock_data/goog.csv', delimiter=',')
	goog_clsPrice = []
	goog_date = []
	global goog_movavg 
	goog_movavg = []

	for i in range(len(data3)):
		goog_clsPrice.append(data3[i][6])
		goog_date.append(data3[i][0])

	goog_clsPrice.reverse()
	goog_date.reverse()
	goog_movavg = numpy.convolve(goog_clsPrice, numpy.ones(10)/10)

	for i in range(10):
		if i == 0 :
			continue
		goog_movavg[len(goog_movavg) - i] = goog_movavg[len(goog_movavg) - 10]
	
	global goog_line
	global goog_sz
	goog_sz = len(goog_movavg)
	goog_fig, goog_ax = plt.subplots()
	goog_line, = goog_ax.plot(goog_movavg, "bo")
	goog_ax.set_ylim(10, 1000)
	goog_ax.set_xlim(0, 2000)
	goog_ani = animation.FuncAnimation(goog_fig, goog_update, goog_data_gen, interval=100)
	plt.ylabel('Price')
	plt.xlabel('Time')
	plt.show()
	

def twitter():
	print "Computing Sentiment... This may take up to 5 minutes"
	#MICROSOFT
	file_tweets = open('tweet_data/msft.dat', 'r')
	tweets = []
	for i in file_tweets.readlines():
		if (not i.find("***")):
			continue
		tweets.append(i)
	outfile = open("json_files/msft.json", "w")
	outfile.write('{"language": "auto","data": [')
	for i in range(len(tweets)):
		tmp = tweets[i].decode('unicode-escape')
		tmp = unicodedata.normalize('NFKD', tmp).encode('ascii','ignore')
		tmp = tmp.strip('\n')
		json.dump({'text':tmp.encode('utf8'), 'query':'microsoft OR windows OR xboxone OR xbox OR one OR word OR office'}, outfile)
		if(i != (len(tweets) - 1)):
			outfile.write(',')
	outfile.write(']}')
	outfile.close()

	#GOOGLE
	file_tweets = open('tweet_data/goog.dat', 'r')
	tweets = []
	for i in file_tweets.readlines():
		if (not i.find("***")):
			continue
		i.strip('\n')
		tweets.append(i)
	outfile = open("json_files/goog.json", "w")
	outfile.write('{"language": "auto","data": [')
	for i in range(len(tweets)):
		tmp = tweets[i].decode('unicode-escape')
		tmp = unicodedata.normalize('NFKD', tmp).encode('ascii','ignore')
		tmp = tmp.strip('\n')		
		json.dump({'text':tmp.encode('utf8'), 'query':'google OR android OR gmail'}, outfile)
		if(i != (len(tweets) - 1)):
			outfile.write(',')
	outfile.write(']}')
	outfile.close()

	#APPLE
	file_tweets = open('tweet_data/aapl.dat', 'r')
	tweets = []
	for i in file_tweets.readlines():
		if (not i.find("***")):
			continue
		i.strip('\n')
		tweets.append(i)
	outfile = open("json_files/aapl.json", "w")
	outfile.write('{"language": "auto","data": [')
	for i in range(len(tweets)):
		tmp = tweets[i].decode('unicode-escape')
		tmp = unicodedata.normalize('NFKD', tmp).encode('ascii','ignore')
		tmp = tmp.strip('\n')		
		json.dump({'text':tmp.encode('utf8'), 'query':'apple OR ipod OR ipad OR macbook OR air OR pro OR imac'}, outfile)
		if(i != (len(tweets) - 1)):
			outfile.write(',')
	outfile.write(']}')
	outfile.close()



	#post to sentiment analytics tool
	http = httplib2.Http()

	url = 'http://www.sentiment140.com/api/bulkClassifyJson?appid=ssuvamsh@gmail.com'   
	body_msft = open('json_files/msft.json', 'r').read()
	body_aapl = open('json_files/aapl.json', 'r').read()
	body_goog = open('json_files/goog.json', 'r').read()
	sent_msft = []
	sent_aapl = []
	sent_goog = []
	val = 0
	sent_msft_vals = []
	sent_aapl_vals = []
	sent_goog_vals = []

	response_msft, content_msft = http.request(url, 'POST', body=body_msft)
	tmp = re.findall('polarity...', content_msft, re.S)
	for m in tmp:
		if (int(m[len(m)-1]) == 0):
			sent_msft.append(-1)
		elif (int(m[len(m)-1]) == 2):
			sent_msft.append(0)
		elif (int(m[len(m)-1]) == 4):
			sent_msft.append(1)

	for i in sent_msft:
		val = val + i
		sent_msft_vals.append(val)

	plt.plot(sent_msft_vals, color='b')

	response_aapl, content_aapl = http.request(url, 'POST', body=body_aapl)
	tmp = re.findall('polarity...', content_aapl, re.S)
	for m in tmp:
		if (int(m[len(m)-1]) == 0):
			sent_aapl.append(-1)
		elif (int(m[len(m)-1]) == 2):
			sent_aapl.append(0)
		elif (int(m[len(m)-1]) == 4):
			sent_aapl.append(1)	


	val = 0
	for i in sent_aapl:
		val = val + i
		sent_aapl_vals.append(val)

	plt.plot(sent_aapl_vals, color='r')
	
	response_goog, content_goog = http.request(url, 'POST', body=body_goog)
	tmp = re.findall('polarity...', content_goog, re.S)
	for m in tmp:
		if (int(m[len(m)-1]) == 0):
			sent_goog.append(-1)
		elif (int(m[len(m)-1]) == 2):
			sent_goog.append(0)
		elif (int(m[len(m)-1]) == 4):
			sent_goog.append(1)


	val = 0
	for i in sent_goog:
		val = val + i
		sent_goog_vals.append(val)

	plt.plot(sent_goog_vals, color='g')
	
	plt.title("Sentiment Graph")
	plt.ylabel('Sentiment')
	plt.xlabel('Time')
	print "Green = Google\nRed = Apple\nBlue = Microsoft"
	print "Done"
	plt.show()


def computeWordCloud():
	#MICROSOFT
	file_tweets = open('tweet_data/msft.dat', 'r')
	tweets = []
	for i in file_tweets.readlines():
		if (not i.find("***")):
			continue
		tmp = i.decode('unicode-escape')
		tmp = unicodedata.normalize('NFKD', tmp).encode('ascii','ignore')
		tmp = tmp.strip('\n')
		tweets.append(tmp)

	#print tweets
	tweet_hash = {}
	for i in tweets:
		tmp = i.split()
		for j in tmp:
			if(tweet_hash.has_key(j)):
				tweet_hash[j] += 1
			else:
				tweet_hash[j] = 1
	f = open('tweet_data/msft_cloud.dat', 'w')
	for i in tweet_hash:
		for j in range(tweet_hash[i]):
			f.write(i)
			f.write(" ")
		f.write("\n")
	f.close()


	#APPLE
	file_tweets = open('tweet_data/aapl.dat', 'r')
	tweets = []
	for i in file_tweets.readlines():
		if (not i.find("***")):
			continue
		tmp = i.decode('unicode-escape')
		tmp = unicodedata.normalize('NFKD', tmp).encode('ascii','ignore')
		tmp = tmp.strip('\n')
		tweets.append(tmp)

	#print tweets
	tweet_hash = {}
	for i in tweets:
		tmp = i.split()
		for j in tmp:
			if(tweet_hash.has_key(j)):
				tweet_hash[j] += 1
			else:
				tweet_hash[j] = 1
	f = open('tweet_data/aapl_cloud.dat', 'w')
	for i in tweet_hash:
		for j in range(tweet_hash[i]):
			f.write(i)
			f.write(" ")
		f.write("\n")
	f.close()


	#Google
	file_tweets = open('tweet_data/goog.dat', 'r')
	tweets = []
	for i in file_tweets.readlines():
		if (not i.find("***")):
			continue
		tmp = i.decode('unicode-escape')
		tmp = unicodedata.normalize('NFKD', tmp).encode('ascii','ignore')
		tmp = tmp.strip('\n')
		tweets.append(tmp)

	#print tweets
	tweet_hash = {}
	for i in tweets:
		tmp = i.split()
		for j in tmp:
			if(tweet_hash.has_key(j)):
				tweet_hash[j] += 1
			else:
				tweet_hash[j] = 1
	f = open('tweet_data/goog_cloud.dat', 'w')
	for i in tweet_hash:
		for j in range(tweet_hash[i]):
			f.write(i)
			f.write(" ")
		f.write("\n")
	f.close()

	print "Computing word cloud for Microsoft..."
	os.system("cp tweet_data/msft_cloud.dat ../libs/mainline/words.txt")
	os.system("../libs/mainline/word_count.py msft > out_files/msft_cloud.out")
	print "Done"

	print "Computing word cloud for Apple..."
	os.system("cp tweet_data/aapl_cloud.dat ../libs/mainline/words.txt")
	os.system("../libs/mainline/word_count.py aapl > out_files/aapl_cloud.out")
	print "Done"

	print "Computing word cloud for Google..."
	os.system("cp tweet_data/goog_cloud.dat ../libs/mainline/words.txt")
	os.system("../libs/mainline/word_count.py goog > out_files/goog_cloud.out")
	print "Done"

def displayWordCloud():
	msftWin = Tkinter.Toplevel()
	msftWin.title("Microsoft Word Cloud")
	msft_img = ImageTk.PhotoImage(Image.open("word_clouds/msft_word_cloud.png"))

	# get the image size
	w = msft_img.width()
	h = msft_img.height()

	# position coordinates of root 'upper left corner'
	x = 0
	y = 0

	# make the root window the size of the image
	msftWin.geometry("%dx%d+%d+%d" % (w, h, x, y))

	# root has no image argument, so use a label as a panel
	panel1 = Tkinter.Label(msftWin, image=msft_img)
	panel1.pack(side='top', fill='both', expand='yes')

	# save the panel's image from 'garbage collection'
	panel1.image = msft_img



gui = Tkinter.Tk()
gui.geometry("300x300")
gui.title("Twitter Stock Prediction")

entry = Tkinter.Entry(gui, width=10)
#entry.pack()

btnGoogMoveAvg = Tkinter.Button(gui, text="Google Stock Data", command=googMoveAvg)
btnAaplMoveAvg = Tkinter.Button(gui, text="Apple Stock Data", command=aaplMoveAvg)
btnMsftMoveAvg = Tkinter.Button(gui, text="Microsoft Stock Data", command=msftMoveAvg)
btnTwitter = Tkinter.Button(gui, text="Sentiment Analysis", command=twitter)
btnWordCloud = Tkinter.Button(gui, text="Compute Word Cloud", command=computeWordCloud)
btnWordCloudDisplay = Tkinter.Button(gui, text="Display Word Cloud", command=displayWordCloud)


btnGoogMoveAvg.grid(sticky=Tkinter.W+Tkinter.E)
btnAaplMoveAvg.grid(sticky=Tkinter.W+Tkinter.E)
btnMsftMoveAvg.grid(sticky=Tkinter.W+Tkinter.E)
btnTwitter.grid(sticky=Tkinter.W+Tkinter.E)
btnWordCloud.grid(sticky=Tkinter.W+Tkinter.E)
btnWordCloudDisplay.grid(sticky=Tkinter.W+Tkinter.E)




gui.mainloop()








