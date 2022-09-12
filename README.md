# Franchise Twitter Bot

![FFL Logo](/Franchise_Fantasy_League_Logo.jpg)

The Franchise Twitter Bot is a Twitter bot I created for the Yahoo Fantasy Football league that I run called the Franchise Fantasy League.

The league is very active in communication and I wanted to provide another avenue for my league members to engage further.

Tweepy, tkinter and yahoo_fantasy_api are all utilized in this project.

franchise_twitter_bot.py holds the bulk of the logic. The program calls on pull_yahoo_transactions in order to bring in the raw data from Yahoo's API. It determines when the most recent tweet from the Twitter account went out and uses that as a benchmark to determine whether to tweet player transactions or not.

Tkinter is utilized to create a GUI where the user can select if they want to process player Adds, Drops or Trades individually.  

When selected to run, the different process transactions function parse through the raw data, pulling the relevant player, team and transaction information to compose the tweet. The tweet is then sent out for all the selected transaction types that have occurred since that most recent tweet.