import tweepy
import requests
import re
import random
import pickle
from bs4 import BeautifulSoup

try:
    # Twitter credentials
    # You can get these from https://apps.twitter.com for your account
    CONSUMER_KEY: str = "YOUR_CONSUMER_KEY"
    CONSUMER_SECRET: str = "YOUR_CONSUMER_SECRET"
    ACCESS_KEY: str = "YOUR_ACCESS_KEY"
    ACCESS_SECRET: str = "YOUR_ACCESS_SECRET"

    # Setting up the authentication and API for Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Get the lyric links, using cupcakKe as placeholder
    # You can place any artist found in LyricsWikia
    artist_page: str = "http://lyrics.wikia.com/wiki/CupcakKe"
    artist_identifier: str = artist_page[23:] + ":"
    page = requests.get(artist_page).text
    full_links: list = []
    soup = BeautifulSoup(page, "html.parser")
    for link in soup.find_all("a", href=re.compile(artist_identifier)):
        forbidden_suffix: str = "?action=edit&redlink=1"
        # Two lines below are cupcakKe specific
        # Remove them and edit line 27 to adapt to your needs
        remove_albums: str = "(201"
        remove_remix: str = "Panda_Remix"
        if (
            forbidden_suffix not in link["href"]
            and remove_albums not in link["href"]
            and remove_remix not in link["href"]
        ):
            full_links.append("http://lyrics.wikia.com" + (link.get("href")))

    # Main function for getting the lyrics
    def main():
        # Create a pickle file for maintaining the 48 last songs
        # Edit the number according to your needs
        pickle_file = open("songfile.pickle", "ab")
        try:
            last_48_songs: list = pickle.load(open("songfile.pickle", "rb"))
        except EOFError:
            last_48_songs: list = []

        # Get a random song from the artist
        lyric_link_index: int = random.randint(0, len(full_links) - 1)
        while lyric_link_index in last_48_songs:
            lyric_link_index = random.randint(0, len(full_links) - 1)

        # Add the songs to the pickle file
        if len(last_48_songs) < 48:
            last_48_songs.append(lyric_link_index)
            with open("songfile.pickle", "wb") as pickle_file:
                pickle.dump(last_48_songs, pickle_file)
        else:
            last_48_songs.remove(last_48_songs[0])
            last_48_songs.append(lyric_link_index)
            with open("songfile.pickle", "wb") as pickle_file:
                pickle.dump(last_48_songs, pickle_file)

        # Get the lyrics from the song
        lyrics_request = requests.get(full_links[lyric_link_index]).text
        lyric_soup = BeautifulSoup(lyrics_request, "html.parser")
        lyrics = lyric_soup.find("div", {"class": "lyricbox"})

        for br in lyrics("br"):
            br.replace_with("\n")
            lyric_list = lyrics.getText().split("\n")

        # Get 1-4 lines and then form the tweet
        number_of_lines: int = random.randint(1, 4)
        start_index: int = random.randint(0, len(lyric_list) - 1)
        tweet: str = lyric_list[start_index]

        if tweet == "":
            start_index -= 1
            tweet = lyric_list[start_index]

        for x in range(number_of_lines - 1):
            lyric_range = start_index + number_of_lines
            if lyric_range < len(lyric_list):
                start_index += 1
                if lyric_list[start_index] != "":
                    tweet = tweet + "\n" + lyric_list[start_index]
                else:
                    break

        api.update_status(tweet)

    if __name__ == "__main__":
        main()

except Exception as e:
    print(e)
