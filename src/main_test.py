import oauth2 as oauth
import urllib
import json
import requests

 
def Request(url, key, secret, http_method = 'GET', post_body = '', http_headers = ''):
    consumer = oauth.Consumer(key = 'xqnLgbfViDnyQMCtxDYdjA', secret = 'PiibIEZ0b2mSuJlXTGkCQFeax4k8rWPrGONLh1Yk')
    token = oauth.Token(key = key, secret = secret)
    client = oauth.Client(consumer, token)
  
    request = client.request(
        url,
        method = http_method,
        body = post_body,
        headers = http_headers)
    
    return request

msQuery = urllib.quote_plus('microsoft')
aaplQuery = urllib.quote_plus('apple')
googQuery = urllib.quote_plus('google')

msft = open('tweet_data/msft.dat','a')
goog = open('tweet_data/goog.dat', 'a')
aapl = open('tweet_data/aapl.dat', 'a')

while True:

	request_ms, response_ms = Request('https://api.twitter.com/1.1/search/tweets.json?q=' + msQuery, '2211534368-OUN8bCDrLIPZQes39Q2wnRhYmEgpo7dKyUUEQHA', 'd0DFx9LUII6bjDx2OFOiF3D1BDGNiThEQGiznUm3kEsRY')
	request_aapl, response_aapl = Request('https://api.twitter.com/1.1/search/tweets.json?q=' + aaplQuery, '2211534368-OUN8bCDrLIPZQes39Q2wnRhYmEgpo7dKyUUEQHA', 'd0DFx9LUII6bjDx2OFOiF3D1BDGNiThEQGiznUm3kEsRY')
	request_goog, response_goog = Request('https://api.twitter.com/1.1/search/tweets.json?q=' + googQuery, '2211534368-OUN8bCDrLIPZQes39Q2wnRhYmEgpo7dKyUUEQHA', 'd0DFx9LUII6bjDx2OFOiF3D1BDGNiThEQGiznUm3kEsRY')

	data = json.loads(response_ms)
	tweets = data['statuses']
	for i in range(len(tweets)):
		tmp = tweets[i][u'text']
		msft.write(tmp.encode('utf-8'))
		msft.write("\n***\n")

	data = json.loads(response_goog)
	tweets = data['statuses']
	for i in range(len(tweets)):
		tmp = tweets[i][u'text']
		goog.write(tmp.encode('utf-8'))
		goog.write("\n***\n")

	data = json.loads(response_aapl)
	tweets = data['statuses']
	for i in range(len(tweets)):
		tmp = tweets[i][u'text']
		aapl.write(tmp.encode('utf-8'))
		aapl.write("\n***\n")


