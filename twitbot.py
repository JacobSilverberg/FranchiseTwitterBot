# created utilizing the tutorial found at:
# https://www.freecodecamp.org/news/creating-a-twitter-bot-in-python-with-tweepy-ac524157a607

import tweepy
from tkinter import *
from credentials import consumer_key, consumer_secret, access_token, access_token_secret

# set up tweety API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def follow_followers():
    """
    Follows back all of the account's current followers
    """
    for follower in tweepy.Cursor(api.get_followers).items():
        api.create_friendship(user_id=follower.id_str)
        print(follower.id_str)

# functions for returning the input data from GUI
def getE1():
    return E1.get()
def getE2():
    return E2.get()
def getE3():
    return E3.get()
def getE4():
    if var4.get() == "Yes":
        return True
    else:
        return False
def getE5():
    if var5.get() == "Yes":
        return True
    else:
        return False
def getE6():
    if var6.get() == "Yes":
        return True
    else:
        return False
def getE7():
    if var7.get() == "Yes":
        return True
    else:
        return False


# tkinter root creation
root = Tk()

# variable initialization for tkinter OptionMenus
options = ["Yes", "No"]
var4 = StringVar()
var5 = StringVar()
var6 = StringVar()
var7 = StringVar()

# tkinter label, text entry and OptionMenu creation
label1 = Label(root, text="Search")
E1 = Entry(root, bd=5)
label2 = Label(root, text="Number of Tweets")
E2 = Entry(root, bd=5)
label3 = Label(root, text="Response")
E3 = Entry(root, bd=5)
label4 = Label(root, text="Reply?")
E4 = OptionMenu(root, var4, *options)
label5 = Label(root, text="Retweet?")
E5 = OptionMenu(root, var5, *options)
label6 = Label(root, text="Favorite?")
E6 = OptionMenu(root, var6, *options)
label7 = Label(root, text="Follow?")
E7 = OptionMenu(root, var7, *options)


def mainFunction():
    """
    Main function. Gets user input from GUI. Will search for input text string up to the number of tweets specified.
    Reply, Retweet, Favorite, Follow have boolean selector to determine actions on found tweets.
    """
    search = getE1()
    number_of_tweets = int(getE2())
    response = getE3()
    reply = getE4()
    retweet = getE5()
    favorite = getE6()
    follow = getE7()

    # reply to the tweet with the givene response
    if reply is True:
        for tweet in tweepy.Cursor(api.search_tweets, search).items(number_of_tweets):
            try:
                tweet_id = tweet.user.id
                username = tweet.user.screen_name
                api.update_status("@" + username + " " + response, in_reply_to_status_id=tweet_id)
                print("Replied with '" + response + "'")

            except tweepy.errors.TweepyException as e:
                print(e)

    # retweet the found tweet
    if retweet is True:
        for tweet in tweepy.Cursor(api.search_tweets, search).items(number_of_tweets):
            try:
                tweet.retweet()
                print('Retweeted the tweet')

            except tweepy.errors.TweepyException as e:
                print(e)

            except StopIteration:
                break

    # favorite the found tweet
    if favorite is True:
        for tweet in tweepy.Cursor(api.search_tweets, search).items(number_of_tweets):
            try:
                tweet.favorite()
                print('Favorited the tweet')

            except tweepy.errors.TweepyException as e:
                print(e)

            except StopIteration:
                break

    # follow the tweet's author
    if follow is True:
        for tweet in tweepy.Cursor(api.search_tweets, search).items(number_of_tweets):
            try:
                tweet_id = tweet.user.id
                api.create_friendship(user_id=tweet_id)
                print("Followed ID", tweet_id)

            except tweepy.errors.TweepyException as e:
                print(e)

            except StopIteration:
                break


# create submit button calling mainFunction
submit = Button(root, text="Submit", command=mainFunction)

# pack all labels, inputs and dropdowns
label1.pack()
E1.pack()
label2.pack()
E2.pack()
label3.pack()
E3.pack()
label4.pack()
E4.pack()
label5.pack()
E5.pack()
label6.pack()
E6.pack()
label7.pack()
E7.pack()
submit.pack()

# main root loop
root.mainloop()
