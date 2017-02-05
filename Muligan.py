import trackopy
import json
from pprint import pprint

class Muligan(object):
    """A class to compute the performance of cards in certain match ups with
    following properties:

    Attributes:
        path_to_data: System path to your track-o-bot history in .json format. E.g. 'C:\\Users\\tommy\\history.json'
        
        deck_type: Deck type in tuple format from track-o-bot. E.g. ("Miracle", "Rogue")
        
        opponent_deck_type_tuples_list: List of opponents you are interested in. E.g. [("Aggro", "Shaman"), ("Midrange", "Shaman"), ("Reno", "Warlock")]
        
        deck_list: List (or single card) you want to evaluate. E.g.
            deck_list = ["Counterfeit Coin", "Backstab", "Preparation", "Small-Time Buccaneer"]
            
        max_turn: Until which turn you want to check your games? Games are often decided until turn 5 or 6 so if you set this 5 all cards
            that are played after turn 5 will be ignored. If you set this to 10, all turns will be included.
    """

    def __init__(self, path_to_data, deck_type, opponent_deck_type_tuples_list, deck_list, max_turn):
        """Initialize the calculator""" 
        self.path_to_data = path_to_data
        self.deck_type = deck_type
        self.opponent_deck_type_tuples_list = opponent_deck_type_tuples_list
        self.deck_list = deck_list
        self.max_turn = max_turn

#'C:\\Users\\tommy\\history.json'
#["Counterfeit Coin","Backstab","Preparation", "Small-Time Buccaneer", "Patches, the Pirat", "Swashburglar", "Cold Blood", "Eviscerate", "Sap","Bloodmage Thalnos", "Fan of Knives", "SI:7 Agent", "Edwin VanCleef", "Shaku, the Collector", "Tomb Pillager", "Azure Drake", "Leeroy Jenkins", "Gadgetzan Auctioneer"]
#[("Aggro", "Shaman"), ("Midrange", "Shaman"), ("Reno", "Warlock")]

    def evaluate(self):
        with open(self.path_to_data) as file:
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

        deck_list = self.deck_list
        #deck_list = ["Eviscerate"]
        opponent_deck_type_tuples_list = self.opponent_deck_type_tuples_list
        #opponent_deck_type_tuples_list = [("Aggro", "Shaman")]


        hero = self.deck_type[1]
        hero_deck = self.deck_type[0]
        for deck_types in opponent_deck_type_tuples_list:
            opponent = deck_types[1]
            opponent_deck = deck_types[0]
            max_turn = self.max_turn
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


