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
            that are played after turn 5 will be ignored. If you set this to 20 or higher, all turns will be included.
    """

    def __init__(self, path_to_data, deck_type, opponent_deck_type_tuples_list, deck_list, max_turn):
        """Initialize the calculator""" 
        self.path_to_data = path_to_data
        self.deck_type = deck_type
        self.opponent_deck_type_tuples_list = opponent_deck_type_tuples_list
        if not deck_list:
            raise Warning("From muligan.__init__: misuse of variable.\
                          Please insert at least one card to evaluate. E.g. ['Coin']")
        self.deck_list = deck_list
        if not max_turn:
            raise Warning("From muligan.__init__: misuse of variable.\
                          Set max_turn to at least 1 (or better higher) to find cards.")
        if max_turn >= 20:
            max_turn = 9999
            print("max_turn was set to 20 or higher. Checking all turns now.")
        self.max_turn = max_turn

    def evaluate(self):
        with open(self.path_to_data) as file:
            page = json.load(file)

        #with open('E:\\Code\\Python\\trackopy\\userdata.track-o-bot.json') as file2:
        #    userdata = json.load(file2)

        # trackobot = trackopy.Trackobot(userdata['username'], userdata['password'])

        # print('login ok')

        print('history item:')
        # old shit:
        # print(len(page))

        #history von trackobot
        #pprint(page['history'][0])



    def find_card(self, card, game, max_turn):
        #iterate over all cards used in the game
        for cards in game['card_history']:
            #check that "me" played the card and not opponent
            if (cards['player'] == 'me') & (card in cards['card'].values()) & (cards['turn'] <= max_turn):
                return game
        return False

    def find_hero_deck(self, page, hero, hero_deck):
        result_games = []
        for game in page:
            if (game["hero"] == hero) & (game["hero_deck"] == hero_deck):
                result_games.append(game.copy())
        return result_games

    def find_opponent_deck(self, page, opponent, opponent_deck):
        result_games = []
        for game in page:
            if (game["opponent"] == opponent) & (game["opponent_deck"] == opponent_deck):
                result_games.append(game.copy())
        return result_games

    def number_card_was_played(self, card, valid_games, max_turn):
        number_card_was_played = 0
        for game in valid_games:
            for cards in game['card_history']:
                #check that "me" played the card and not opponent
                if (cards['player'] == 'me') & (card in cards['card'].values()) & (cards['turn'] <= max_turn):
                    number_card_was_played += 1
            ## number of wins????
        if(number_card_was_played < len(valid_games)):
            raise Warning("From muligan.number_card_was_played: misuse of function.\
                          Card was not found in all games. Make sure to call this function with only valid games.")
        return number_card_was_played

    def count_wins(self, games):
        number_of_wins = 0
        for game in games:
            if(game['result'] == "win"):
                number_of_wins += 1
        return number_of_wins

    def evaluate_card(self, card, games, max_turn):
        games_with_card_played = []
        for game in games:
            if(self.find_card(card, game, max_turn) != False):
                games_with_card_played.append(self.find_card(card, game, max_turn).copy())

        return games_with_card_played

    def evaluate_deck_list(self, deck_list, games, max_turn):
        result_list = []
        for card in deck_list:
            games_with_card_played = self.evaluate_card(card, games, max_turn)
            card_result = {'card': card,\
                           'number of wins with card': self.count_wins(games_with_card_played),\
                           'number of games with card': len(games_with_card_played),\
                           'times played': self.number_card_was_played(card, games_with_card_played, max_turn)}
            result_list.append(card_result.copy())
        return result_list

    def print_result(self, result_list):
        for result in result_list:
            print("######")
            if (result['number of games'] > 0):
                print("Result for", result['opponent_deck'], result['opponent'])
                print("Number of games:", result['number of games'])
                print("Number of wins:", result['number of wins'])
                print("Win %: {0:.2f}".format((result['number of wins']/result['number of games'])*100))
                for cards in result['cards_evaluated']:
                    if (cards['times played'] > 0):
                        print("Number of wins with:", cards['card'], cards['number of wins with card'])
                        print(cards['card'], "was played", cards['times played'])
                        print("Number of games with card:", cards['number of games with card'])
                        print("Win %: {0:.2f}".format((cards['number of wins with card']/cards['number of games with card'])*100))
            else:
                print("No games against", result['opponent_deck'], result['opponent'])



    def evaluate2(self):
        with open(self.path_to_data) as file:
            page = json.load(file)

        if 'history' in page:
            page = page['history']

        deck_list = self.deck_list

        #our deck
        hero = self.deck_type[1]
        hero_deck = self.deck_type[0]
        max_turn = self.max_turn

        result_list = []
        #result type example: [{'opponent': 'Shaman', 'opponent_deck': 'Aggro'
        #                       'number of games': 3,
        #                       'number of wins': 2,
        #                       'cards_evaluated':
        #                       [{'card': 'Eviscerate', 'number of wins with card': 2, 'number of games': 2, 'times played': 1},
        #                        {'card': 'Backstab', 'number of wins with card': 1, 'number of games': 1, 'times played': 1}]
        #                       }]


        valid_games = self.find_hero_deck(page, hero, hero_deck)

        #opponent deck(s)
        opponent_deck_type_tuples_list = self.opponent_deck_type_tuples_list
        if not opponent_deck_type_tuples_list:
            print("No match-ups selected. All games will be summarzied.")
            opponent = "All"
            opponent_deck = "All"
            #evaluate games with per card
            result = {'opponent': opponent, 'opponent_deck': opponent_deck,\
                      'number of games': len(valid_games),\
                      'number of wins': self.count_wins(valid_games),\
                      'cards_evaluated': []} #Empty list to be filled with the cards for each match up.
            result['cards_evaluated'] = self.evaluate_deck_list(deck_list, valid_games, max_turn)

            result_list.append(result.copy())
        else:
            for deck_types in opponent_deck_type_tuples_list:
                opponent = deck_types[1]
                opponent_deck = deck_types[0]

                #get all games vs one archytype
                games_vs_opponent = self.find_opponent_deck(valid_games, opponent, opponent_deck)

                result = {'opponent': opponent, 'opponent_deck': opponent_deck,\
                          'number of games': len(games_vs_opponent),\
                          'number of wins': self.count_wins(games_vs_opponent),\
                          'cards_evaluated': []} #Empty list to be filled with the cards for each match up.

                #evaluate games per card
                result['cards_evaluated'] = self.evaluate_deck_list(deck_list, games_vs_opponent, max_turn)

                result_list.append(result.copy())

        return result_list
