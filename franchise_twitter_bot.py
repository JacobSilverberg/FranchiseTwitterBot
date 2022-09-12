import tweepy
from tkinter import *
from credentials import consumer_key, consumer_secret, access_token, access_token_secret
from pull_yahoo_transactions import pull_yahoo_transactions
from datetime import datetime
import pytz


# add, drop, trade = pull_yahoo_transactions(2021)
# print(add)
# print(drop)
# print(trade)

yahoo_adds = [{'transaction_key': '414.l.702594.tr.74', 'transaction_id': '74', 'type': 'add/drop', 'status': 'successful', 'timestamp': '1662910637', 'players': {'0': {'player': [[{'player_key': '414.p.100004'}, {'player_id': '100004'}, {'name': {'full': 'Cincinnati', 'first': 'Cincinnati', 'last': '', 'ascii_first': 'Cincinnati', 'ascii_last': ''}}, {'editorial_team_abbr': 'Cin'}, {'display_position': 'DEF'}, {'position_type': 'DT'}], {'transaction_data': [{'type': 'add', 'source_type': 'freeagents', 'destination_type': 'team', 'destination_team_key': '414.l.702594.t.6', 'destination_team_name': 'Donovan McNabb'}]}]}, '1': {'player': [[{'player_key': '414.p.100009'}, {'player_id': '100009'}, {'name': {'full': 'Green Bay', 'first': 'Green Bay', 'last': '', 'ascii_first': 'Green Bay', 'ascii_last': ''}}, {'editorial_team_abbr': 'GB'}, {'display_position': 'DEF'}, {'position_type': 'DT'}], {'transaction_data': {'type': 'drop', 'source_type': 'team', 'source_team_key': '414.l.702594.t.6', 'source_team_name': 'Donovan McNabb', 'destination_type': 'waivers'}}]}, 'count': 2}}]
yahoo_drops = [{'transaction_key': '406.l.79095.tr.716', 'transaction_id': '716', 'type': 'drop', 'status': 'successful', 'timestamp': '1640957652', 'players': {'0': {'player': [[{'player_key': '406.p.100011'}, {'player_id': '100011'}, {'name': {'full': 'Indianapolis', 'first': 'Indianapolis', 'last': '', 'ascii_first': 'Indianapolis', 'ascii_last': ''}}, {'editorial_team_abbr': 'Ind'}, {'display_position': 'DEF'}, {'position_type': 'DT'}], {'transaction_data': {'type': 'drop', 'source_type': 'team', 'source_team_key': '406.l.79095.t.11', 'source_team_name': 'SILVERSLAMMMERRRRSSS', 'destination_type': 'waivers'}}]}, 'count': 1}}, {'transaction_key': '406.l.79095.tr.715', 'transaction_id': '715', 'type': 'drop', 'status': 'successful', 'timestamp': '1640957637', 'players': {'0': {'player': [[{'player_key': '406.p.9520'}, {'player_id': '9520'}, {'name': {'full': 'Ryan Succop', 'first': 'Ryan', 'last': 'Succop', 'ascii_first': 'Ryan', 'ascii_last': 'Succop'}}, {'editorial_team_abbr': 'TB'}, {'display_position': 'K'}, {'position_type': 'K'}], {'transaction_data': {'type': 'drop', 'source_type': 'team', 'source_team_key': '406.l.79095.t.11', 'source_team_name': 'SILVERSLAMMMERRRRSSS', 'destination_type': 'waivers'}}]}, 'count': 1}}]
yahoo_trades = [{'transaction_key': '406.l.79095.tr.567', 'transaction_id': '567', 'type': 'trade', 'status': 'successful', 'timestamp': '1637981930', 'trader_team_key': '406.l.79095.t.2', 'trader_team_name': '2020 Vision', 'tradee_team_key': '406.l.79095.t.11', 'tradee_team_name': 'SILVERSLAMMMERRRRSSS', 'players': {'0': {'player': [[{'player_key': '406.p.29255'}, {'player_id': '29255'}, {'name': {'full': 'Will Fuller V', 'first': 'Will', 'last': 'Fuller V', 'ascii_first': 'Will', 'ascii_last': 'Fuller V'}}, {'editorial_team_abbr': 'Mia'}, {'display_position': 'WR'}, {'position_type': 'O'}], {'transaction_data': [{'type': 'trade', 'source_type': 'team', 'source_team_key': '406.l.79095.t.2', 'source_team_name': '2020 Vision', 'destination_type': 'team', 'destination_team_key': '406.l.79095.t.11', 'destination_team_name': 'SILVERSLAMMMERRRRSSS'}]}]}, '1': {'player': [[{'player_key': '406.p.32719'}, {'player_id': '32719'}, {'name': {'full': 'Chase Claypool', 'first': 'Chase', 'last': 'Claypool', 'ascii_first': 'Chase', 'ascii_last': 'Claypool'}}, {'editorial_team_abbr': 'Pit'}, {'display_position': 'WR'}, {'position_type': 'O'}], {'transaction_data': [{'type': 'trade', 'source_type': 'team', 'source_team_key': '406.l.79095.t.11', 'source_team_name': 'SILVERSLAMMMERRRRSSS', 'destination_type': 'team', 'destination_team_key': '406.l.79095.t.2', 'destination_team_name': '2020 Vision'}]}]}, 'count': 2}}]

# set up tweety API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# set UTC variable for timestamp comparison
utc = pytz.UTC

timestamp = 1662910637
transaction_time = datetime.fromtimestamp(timestamp)

# get timestamp of most recent tweet
tweet = api.user_timeline(count=1)
most_recent_tweet_time = tweet[0].created_at

# convert timestampts to comparable datetime objects
transaction_time = transaction_time.replace(tzinfo=utc)
most_recent_tweet_time = most_recent_tweet_time.replace(tzinfo=utc)

# comparison of datetimes of most recent tweet against
# if transaction_time > most_recent_tweet_time:
#     print("True")
# elif most_recent_tweet_time > transaction_time:
#     print("False")
# else:
#     print("Doesn't work")

def convert_timestamp(timestamp):
    """
    Handles conversion of timestamp into datetime for comparison
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

            # convert timestamp for comparison
            conv_timestamp_AD = convert_timestamp(timestamp_AD)

            # if transaction has occurred since most recent tweet:
            if conv_timestamp_AD > most_recent_tweet_time:
                # format tweet string
                if added_faab_bid_AD is None:
                    tweet_string = "Player Add & drop:\n\n" + added_owner_name_AD + " added " + added_player_name_AD + " from " + added_from_source_AD + " and dropped " + dropped_player_name_AD + " to " + dropped_to_source_AD + "."
                else:
                    tweet_string = "Player Add & drop:\n\n" + added_owner_name_AD + " added " + added_player_name_AD + " for " + added_faab_bid_AD + " FAAB dollars from " + added_from_source_AD + " and dropped" + dropped_player_name_AD + "to " + dropped_to_source_AD + "."

                # publish tweet with transaction
                api.update_status(tweet_string)

                # console print for confirmation
                print("Tweeted Add/Drop of", added_player_name_AD, "for", dropped_player_name_AD)

        # iterate through only add transactions
        if add[i]['type'] == "add":
            if 'faab_bid' in add[i].keys():
                added_faab_bid_add = add[i]['faab_bid']

            added_player_name_add = add[i]['players']['0']['player'][0][2]['name']['full']
            timestamp_add = add[i]['timestamp']
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
    return


def process_trade_transactions(trade):
    """
    Parses the trade transactions in order to pull out the relevant details for tweeting:
    Trading team names, list of traded players received, timestamp.
    """
    for i in range(len(trade)):
        trader_team_name = trade[i]['trader_team_name']
        tradee_team_name = trade[i]['tradee_team_name']
        trader_receives = []
        tradee_receives = []
        timestamp_trade = trade[i]['timestamp']

        players_traded_count = trade[i]['players']['count']
        for j in range(players_traded_count):
            traded_player_name = trade[i]['players'][str(j)]['player'][0][2]['name']['full']
            traded_player_destination_owner = trade[i]['players'][str(j)]['player'][1]['transaction_data'][0]['source_team_name']
            if traded_player_destination_owner == trader_team_name:
                trader_receives.append(traded_player_name)
            else:
                tradee_receives.append(traded_player_name)
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