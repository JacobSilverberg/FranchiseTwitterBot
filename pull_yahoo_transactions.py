from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import math

def pull_yahoo_transactions(year):
    """
    connects to yahoo's API and pulls dict of given year's fantasy football transactions.
    :param year: Int
    :return: added_players dict, dropped_players dict, traded_players dict
    """
    league_id = {2022: '414.l.702594',
                 2021: '406.l.79095',
                 2020: '399.l.136422',
                 2019: '390.l.180951',
                 2018: '380.l.173434',
                 2017: '371.l.780538',
                 2016: '359.l.1634',
                 2015: '348.l.18148',
                 2014: '331.l.300822',
                 }

    # connect to yahoo api
    sc = OAuth2(None, None, from_file="oauth2.json")

    # get game object
    game = yfa.game.Game(sc, 'nfl')

    # get the league object of 2021 Franchise league (hardcoded from return of leagues)
    franchise = game.to_league(league_id[year])

    # get all add, drop and trade transactions
    added_players = franchise.transactions('add', '2000')
    dropped_players = franchise.transactions('drop', '2000')
    traded_players = franchise.transactions('trade', '2000')

    # print(added_players)
    # print(dropped_players)
    # print(traded_players)

    return added_players, dropped_players, traded_players
