# LyricsBot
Twitter bot for getting lyrics from LyricsWikia from a certain artist. The artist can be determined, I used cupcakKe as an example. I've learned Python independently in 2014 but never used it since. I used to be an active Twitter user and there are a lot of interesting bots, so I decided to make one myself. Python seemed to be the perfect language for this purpose.

~~Bot also running at https://twitter.com/cupcakKesays on my Raspberry Pi.~~
**Update 14/11/2020:** LyricsWikia has shut down - thus, the code and the Twitter bot do not work anymore.

**Note:** *cupcakKe's lyrics are very NSFW* 👀

# Features
  - Easy to apply any artist to the bot
  - When getting the song, checks whether it has been used in last 24 hours (maintained by a pickle file) (Update 25/06/2018: now 48 hours/songs, as cupcakKe's discography is large enough)
  - Forms an 1-4 line Tweet, the number of lines is randomized
  - Posting every hour, this also can be modified
  - Checks for newlines and removes them
  
 # What did I do/learn?
  - Python basics revise 😉
  - How bots overall work
  - Little about Twitter API
  - Web scraping with BeautifulSoup
  - Pickle files
  - Cron jobs
