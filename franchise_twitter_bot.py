import tweepy
from tkinter import *
from credentials import consumer_key, consumer_secret, access_token, access_token_secret
from pull_yahoo_transactions import pull_yahoo_transactions
from datetime import datetime
import pytz

# pull transaction data into yahoo, assign to variables
yahoo_adds, yahoo_drops, yahoo_trades = pull_yahoo_transactions(2022)

# set up tweety API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# set UTC variable for timestamp comparison
utc = pytz.UTC

# get timestamp of most recent tweet and convert to comparable datetime object
tweet = api.user_timeline(count=1)
most_recent_tweet_time = tweet[0].created_at
most_recent_tweet_time = most_recent_tweet_time.replace(tzinfo=utc)

def convert_timestamp(timestamp):
    """
    Handles conversion of timestamp from yahoo data into datetime object for comparison with tweet datetime
    """
    transaction_time = datetime.fromtimestamp(int(timestamp))
    transaction_time = transaction_time.replace(tzinfo=utc)
    return transaction_time

def process_add_transactions(add):
    """
    Parses the add transactions in order to pull out the relevant details for tweeting:
    Added player name, faab_bid, add source, owner name, dropped player name, dropped to source, timestamp.
    """
    for i in range(len(add)):
        # iterate through add/drop transactions
        if add[i]['type'] == "add/drop":
            # if faab_bid placed on the added player, print faab_bid value, else leave variable as None
            added_faab_bid_AD = None
            if 'faab_bid' in add[i].keys():
                added_faab_bid_AD = add[i]['faab_bid']

            # pull desired information into variables for tweet
            added_player_name_AD = add[i]['players']['0']['player'][0][2]['name']['full']
            dropped_player_name_AD = add[i]['players']['1']['player'][0][2]['name']['full']
            added_from_source_AD = add[i]['players']['0']['player'][1]['transaction_data'][0]['source_type']
            dropped_to_source_AD = add[i]['players']['1']['player'][1]['transaction_data']['destination_type']
            added_owner_name_AD = add[i]['players']['0']['player'][1]['transaction_data'][0]['destination_team_name']
            timestamp_AD = add[i]['timestamp']

            # legibility replacement
            if added_from_source_AD == "freeagents":
                added_from_source_AD = "free agency"
            if dropped_to_source_AD == "freeagents":
                dropped_to_source_AD = "free agency"

            # convert timestamp for comparison
            conv_timestamp_AD = convert_timestamp(timestamp_AD)

            # if transaction has occurred since most recent tweet:
            if conv_timestamp_AD > most_recent_tweet_time:
                # format tweet string
                if added_faab_bid_AD is None:
                    tweet_string_AD = "Player Add & Drop:\n\n" + added_player_name_AD + " added by " + added_owner_name_AD + " from " + added_from_source_AD + " and dropped " + dropped_player_name_AD + " to " + dropped_to_source_AD + "."
                else:
                    tweet_string_AD = "Player Add & Drop:\n\n" + added_player_name_AD + " added by " + added_owner_name_AD + " for " + added_faab_bid_AD + " FAAB dollars from " + added_from_source_AD + " and dropped " + dropped_player_name_AD + " to " + dropped_to_source_AD + "."

                # publish tweet with transaction
                api.update_status(tweet_string_AD)

                # console print for confirmation
                print("Tweeted Add/Drop of", added_player_name_AD, "for", dropped_player_name_AD)

        # iterate through only add transactions
        if add[i]['type'] == "add":
            # if faab_bid placed on the added player, print faab_bid value, else leave variable as None
            added_faab_bid_add = None
            if 'faab_bid' in add[i].keys():
                added_faab_bid_add = add[i]['faab_bid']

            # pull desired information into variables for tweet
            added_player_name_add = add[i]['players']['0']['player'][0][2]['name']['full']
            added_from_source_add = add[i]['players']['0']['player'][1]['transaction_data'][0]['source_type']
            added_owner_name_add = add[i]['players']['0']['player'][1]['transaction_data'][0]['destination_team_name']
            timestamp_add = add[i]['timestamp']

            # legibility replacement
            if added_from_source_add == "freeagents":
                added_from_source_add = "free agency"

            # convert timestamp for comparison
            conv_timestamp_add = convert_timestamp(timestamp_add)

            # if transaction has occurred since most recent tweet:
            if conv_timestamp_add > most_recent_tweet_time:
                if added_faab_bid_add is None:
                    tweet_string_add = "Player Add:\n\n" + added_player_name_add + " added by " + added_owner_name_add + " from " + added_from_source_add + "."
                else:
                    tweet_string_add = "Player Add:\n\n" + added_player_name_add + " added by " + added_owner_name_add + " for " + added_faab_bid_add + " FAAB dollars from " + added_from_source_add + "."

                # publish tweet with transaction
                api.update_status(tweet_string_add)

                # console print for confirmation
                print("Tweeted Add of", added_player_name_add)

    return


def process_drop_transactions(drop):
    """
    Parses the drop transactions in order to pull out the relevant details for tweeting:
    Dropped player name, dropping owner, dropped source, timestamp.
    """
    for i in range(len(drop)):
        # iterate through only drop transactions
        if drop[i]['type'] == "drop":
            dropped_player_name_drop = drop[i]['players']['0']['player'][0][2]['name']['full']
            dropped_owner_name_drop = drop[i]['players']['0']['player'][1]['transaction_data']['source_team_name']
            dropped_to_source_drop = drop[i]['players']['0']['player'][1]['transaction_data']['destination_type']
            timestamp_drop = drop[i]['timestamp']

            # legibility replacement
            if dropped_to_source_drop == "freeagents":
                dropped_to_source_drop = "free agency"

            # convert timestamp for comparison
            conv_timestamp_drop = convert_timestamp(timestamp_drop)

            # if transaction has occurred since most recent tweet:
            if conv_timestamp_drop > most_recent_tweet_time:
                tweet_string_drop = "Player Drop:\n\n" + dropped_player_name_drop + " dropped by " + dropped_owner_name_drop + " to " + dropped_to_source_drop + "."

                # publish tweet with transaction
                api.update_status(tweet_string_drop)

                # console print for confirmation
                print("Tweeted Drop of", dropped_player_name_drop)

    return


def process_trade_transactions(trade):
    """
    Parses the trade transactions in order to pull out the relevant details for tweeting:
    Trading team names, list of traded players received, timestamp.
    """
    for i in range(len(trade)):
        # pull desired information into variables for tweet, create list for traded players
        trader_team_name = trade[i]['trader_team_name']
        tradee_team_name = trade[i]['tradee_team_name']
        trader_receives = []
        tradee_receives = []
        timestamp_trade = trade[i]['timestamp']

        # iterate through each trade and add players to correct list
        players_traded_count = trade[i]['players']['count']
        for j in range(players_traded_count):
            traded_player_name = trade[i]['players'][str(j)]['player'][0][2]['name']['full']
            traded_player_destination_owner = trade[i]['players'][str(j)]['player'][1]['transaction_data'][0]['source_team_name']
            if traded_player_destination_owner == trader_team_name:
                trader_receives.append(traded_player_name)
            else:
                tradee_receives.append(traded_player_name)

        # convert timestamp for comparison
        conv_timestamp_trade = convert_timestamp(timestamp_trade)

        # if transaction has occurred since most recent tweet:
        if conv_timestamp_trade > most_recent_tweet_time:
            tweet_string_trade = "🚨🚨🚨Trade Alert🚨🚨🚨\n\n" + trader_team_name + " receives:\n" + "".join(trader_receives) + "\n\n" + tradee_team_name + " receives:\n" + "".join(tradee_receives)

            # publish tweet with transaction
            api.update_status(tweet_string_trade)

            # console print for confirmation
            print("Tweeted Trade between", trader_team_name, "and", tradee_team_name)

        return


# functions for returning the input data from GUI
def getE1():
    if var1.get() == "Yes":
        return True
    else:
        return False
def getE2():
    if var2.get() == "Yes":
        return True
    else:
        return False
def getE3():
    if var3.get() == "Yes":
        return True
    else:
        return False


# tkinter root creation
root = Tk()

# variable initialization for tkinter OptionMenus
options = ["Yes", "No"]
var1 = StringVar()
var2 = StringVar()
var3 = StringVar()

# tkinter label, text entry and OptionMenu creation
label1 = Label(root, text="Process Adds?")
E1 = OptionMenu(root, var1, *options)
label2 = Label(root, text="Process Drops?")
E2 = OptionMenu(root, var2, *options)
label3 = Label(root, text="Process Trades?")
E3 = OptionMenu(root, var3, *options)


def mainFunction():
    process_adds = getE1()
    process_drops = getE2()
    process_trades = getE3()

    if process_adds is True:
        process_add_transactions(yahoo_adds)

    if process_drops is True:
        process_drop_transactions(yahoo_drops)

    if process_trades is True:
        process_trade_transactions(yahoo_trades)


# create submit button calling mainFunction
submit = Button(root, text="Submit", command=mainFunction)

# pack all labels, inputs and dropdowns
label1.pack()
E1.pack()
label2.pack()
E2.pack()
label3.pack()
E3.pack()
submit.pack()

# main root loop
root.mainloop()
