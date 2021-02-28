# Twitter-Bot
Script pulls from *Reddit API* to parse through r/PokemonGoRaids and utilizes the *Twitter API* to post. It looks through the subreddit given the parameters of the last 10 **new** posts and the Pokemon name. Prior to receiving the name, reads through a .csv created from all possible Pokemon in ```https://gist.github.com/simsketch/1a029a8d7fca1e4c142cbfd043a68f19```
to verify it, and posts a reply to the mentioned post. Additionally added most recent raid found, every hour.

Find the bot at @PokemonRaidBot or the link below (live now, using *Heroku*):
https://twitter.com/PokemonRaidBot

![](media/twitter_main.png)

For future updates (TO-DO):
- [ ] Additional error handling for more situations.
- [ ] Add option for multiple Pokemon input.
- [ ] Add more commands such as: 
  * Most recent raid (**DONE**)
  * Last time a Pokemon raid was spotted for a specific name
  * The last x Pokemon spotted
  * Friend code of poster
- [X] Run on server instead of local machine for 24/7 access.
- [X] Store tweet ID's to exclude tweets when re-running.

**Twitter API:**
https://developer.twitter.com/en/docs

**Reddit API:**
https://www.reddit.com/dev/api/
