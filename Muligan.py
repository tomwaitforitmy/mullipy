
import trackopy
import json
from pprint import pprint

print('Import ok')


with open('C:\\Users\\tommy\\history.json') as file:
    page = json.load(file)

#with open('E:\\Code\\Python\\trackopy\\userdata.track-o-bot.json') as file2:
#    userdata = json.load(file2)

#pprint(userdata)

# trackobot = trackopy.Trackobot(userdata['username'], userdata['password'])

# print('login ok')
# Get your stats by arena, class, or deck
# stats = trackobot.stats(stats_type='decks')

# print('stats ok')

print('history item:')
# old shit:
# print(len(page))

# print(list(page['history'].keys()))
#history von trackobot
#pprint(page['history'][0])

# History von json/trackopy CLI
#pprint(page)
# end old shit

deck_list = ["Counterfeit Coin","Backstab","Preparation", "Small-Time Buccaneer", "Patches, the Pirat", "Swashburglar", "Cold Blood", "Eviscerate", "Sap","Bloodmage Thalnos", "Fan of Knives", "SI:7 Agent", "Edwin VanCleef", "Shaku, the Collector", "Tomb Pillager", "Azure Drake", "Leeroy Jenkins", "Gadgetzan Auctioneer"]
#deck_list = ["Eviscerate"]
opponent_deck_type_tuples_list = [("Aggro", "Shaman"), ("Midrange", "Shaman"), ("Reno", "Warlock")]
#opponent_deck_type_tuples_list = [("Aggro", "Shaman")]


for deck_types in opponent_deck_type_tuples_list:
    hero = "Rogue"
    hero_deck = "Miracle"
    opponent = deck_types[1]
    opponent_deck = deck_types[0]
    max_turn = 10
    ##print( opponent_deck, opponent)

    for card in deck_list:
        game_ids = []
        games_i_want_to_save = []
        number_of_total_games = 0
        number_of_total_wins = 0
        number_of_valid_games = 0
        number_card_was_played = 0
        number_of_wins = 0
        number_of_wins_with_card = 0
        for game in page:
            if (game["hero"] == hero ) & (game["hero_deck"] == hero_deck) & (game["opponent_deck"] == opponent_deck) & (game["opponent"] == opponent):
                for cards in game['card_history']:
                    if (cards['player'] == 'me') & (card in cards['card'].values()) & (cards['turn'] <= max_turn):
                        #print(game['result'])
                        if( game['id'] not in game_ids):
                            number_of_valid_games += 1
                            games_i_want_to_save.append(game.copy())
                            game_ids.append(game['id'])
                            if(game['result'] == "win"):
                                number_of_wins_with_card += 1
                        #print(cards['turn'])
                        number_card_was_played += 1
                #pprint(game)
                number_of_total_games += 1
                if(game['result'] == "win"):
                    number_of_wins += 1

        if(number_of_valid_games > 0):
            print("--------------------------", card)
            print("In", number_of_valid_games, "games", card, "was played", number_card_was_played, "times including turn", max_turn)
            print("Wins with", card, ":", number_of_wins_with_card)
            win_percent = 0.0
            if(number_of_valid_games > 0):
                win_percent = (number_of_wins_with_card/number_of_valid_games)*100
            print("Win percent: {0:.2f}".format(win_percent), "%")

    print("------")
    print("Number of games", hero_deck, hero, "vs", opponent_deck, opponent, ":", number_of_total_games)
    print("Total wins:", number_of_wins)
    print("Win percent: {0:.2f}".format((number_of_wins/number_of_total_games)*100), "%")
    print("#################################")


