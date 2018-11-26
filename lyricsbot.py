import tweepy, urllib2, sys, re, random, pickle
from bs4 import BeautifulSoup

try:
	#Twitter credentials, you can get these from https://apps.twitter.com for your account
	CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
	CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
	ACCESS_KEY = 'YOUR_ACCESS_KEY'
	ACCESS_SECRET = 'YOUR_ACCESS_SECRET'

	#Setting up the authentication and API for Twitter
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

	#Get the lyric links, using cupcakKe as placeholder. You can place any artist found in LyricsWikia.
	artistPage = "http://lyrics.wikia.com/wiki/CupcakKe"
	artistIdentifier = artistPage[23:] + ":"
	page = urllib2.urlopen(artistPage)
	fullLinks = []
	last48Songs = []
	soup = BeautifulSoup(page, 'html.parser')
	for link in soup.find_all('a', href=re.compile(artistIdentifier)):
		forbiddenSuffix = "?action=edit&redlink=1"
		#Two lines below are cupcakKe specific
		removeAlbums = "(201"
		removeRemix = "Panda_Remix"
		if forbiddenSuffix not in link['href'] and removeAlbums not in link['href'] and removeRemix not in link['href']:
			fullLinks.append('http://lyrics.wikia.com' + (link.get('href')))

	#Main function for getting the lyrics
	def main():
		#Create a pickle file for maintaining the 24 last songs
		pickle_file = open('songfile.pickle', 'ab')
		try:
			last48Songs = pickle.load(open('songfile.pickle', 'rb'))
		except EOFError:
			last48Songs = []
				
		#Get a random song from the artist
		lyricLinkIndex = (random.randint(0, len(fullLinks)-1))
		while lyricLinkIndex in last48Songs:
			lyricLinkIndex = (random.randint(0, len(fullLinks)-1))

		#Add the songs to the pickle file
		if len(last48Songs) < 48:
			last48Songs.append(lyricLinkIndex)
			with open ('songfile.pickle', 'wb') as pickle_file:
				pickle.dump(last48Songs, pickle_file)
		else:
			last48Songs.remove(last48Songs[0])
			last48Songs.append(lyricLinkIndex)
			with open ('songfile.pickle', 'wb') as pickle_file:
				pickle.dump(last48Songs, pickle_file)

		#Get the lyrics from the song
		lyricsRequest = urllib2.urlopen(fullLinks[lyricLinkIndex])
		lyricSoup = BeautifulSoup(lyricsRequest, 'html.parser')
		lyrics = lyricSoup.find('div',  {"class": "lyricbox"})

		for br in lyrics("br"):
			br.replace_with("\n")
			lyricList = lyrics.getText().split("\n")

		#Get 1-4 lines and then form the tweet
		numberOfLines = (random.randint(1,4))
		startIndex = (random.randint(0, len(lyricList)-1))
		tweet = lyricList[startIndex]

		if tweet == "":
			startIndex -= 1
			tweet = lyricList[startIndex]
					
		for x in range(numberOfLines-1):
			lyricRange = startIndex + numberOfLines
			if lyricRange < len(lyricList):
				startIndex += 1
				if lyricList[startIndex] != "":
					tweet = tweet + "\n" + lyricList[startIndex]
				else:
					break

		api.update_status(tweet)

	if __name__ == "__main__":
		main()

except Exception as e:
    print(e.message)