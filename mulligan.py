import datetime
import pprint

import trackopy
import json

import xlsxwriter


class Mulligan(object):
    """A class to compute the performance of cards in certain match ups. The goal is to improve your mulligan and/or to
        identify cards that are weak against certain match ups in order to find room for tech cards. The Mulligan class
        has the following properties:

    Attributes:
        data_source: System path to your track-o-bot history in .json format. E.g. 'C:\\Users\\tommy\\history.json'
            Alternatively, you can insert your track-o-bot account data as dictionary. E.g.
            {"username": "YourAccount", "password": "YourPassword"}

        deck_type: Deck type in tuple format from track-o-bot. E.g. ("Miracle", "Rogue")

        opponent_deck_type_tuples_list: List of opponents you are interested in. E.g.:
        [("Aggro", "Shaman"), ("Midrange", "Shaman"), ("Reno", "Warlock")]
        
        deck_list: List (or single card) you want to evaluate. E.g.
            deck_list = ["Counterfeit Coin", "Backstab", "Preparation", "Small-Time Buccaneer"]

        max_turn: Until which turn you want to check your games? Games are often decided until turn 5 or 6 so if you set
            this 5 all cards that are played after turn 5 will be ignored. If you set this to 20 or higher, all turns
            will be included.
    """

    def __init__(self, data_source, deck_type, opponent_deck_type_tuples_list, deck_list, max_turn):
        # Check if the user supplied data in .json format.
        pages = [] # contains the data page(s)
        if '.json' in data_source:
            with open(data_source) as file:
                page = json.load(file)
            # Standard history page contains stuff we don't need. Here we get rid of it. Todo: adapt for multiple pages.
            if 'history' in page:
                pages.append(page['history'])
            else:
                pages.append(page)
        # Check if we can connect to track-o-bot with the data
        elif {'username', 'password'}.issubset(data_source):
            print("Found username and password. Connecting to track-o-bot.com ...")
            pages = self.get_pages_from_trackobot_page(data_source['username'], data_source['password'])

        else:
            raise Warning("From mulligan.__init__: misuse of data_source.\
                          Please supply a path to a .json file (e.g. 'C:\history.json')\
                          or username and password for track-o-bot\
                          (e.g. {'username': 'your_name', 'password': 'your_passowrd'}")

        self.data = pages
        self.deck_type = deck_type
        self.opponent_deck_type_tuples_list = opponent_deck_type_tuples_list
        if not self.opponent_deck_type_tuples_list:
            print("No match-ups given. Data from track-o-bot will be loaded.")
            self.opponent_deck_type_tuples_list = self.load_decklists_from_json("testdata\\track-o"
                                                                                "-bot_decklists_16022017.json")
            # Todo: we could create a user here or ask for pw/user, but the list does not contain 'Other' decks
            # user = trackopy.Trackobot.create_user()
            # trackobot = trackopy.Trackobot(user['username'], user['password'])
            # decks = trackobot.decks()

        if not deck_list:
            raise Warning("From mulligan.__init__: misuse of variable.\
                          Please insert at least one card to evaluate. E.g. ['Coin']")
        self.deck_list = deck_list
        if not max_turn:
            raise Warning("From mulligan.__init__: misuse of variable.\
                          Set max_turn to at least 1 (or better higher) to find cards.")
        if max_turn >= 20:
            max_turn = 9999
            print("max_turn was set to 20 or higher. Checking all turns now.")
        self.max_turn = max_turn

    def get_pages_from_trackobot_page(self, username, password, date=None):
        pages = []
        if not date:
            date = datetime.datetime.now()
        trackobot = trackopy.Trackobot(username, password)
        # Track-o-bot only saves the card history for 10 days.
        # Therefore, we only search for games in last 10 days.
        minus_ten_days = date - datetime.timedelta(days=+10)

        i = 1
        page = trackobot.history(i)['history']

        while self.serach_pages_younger_than(page, minus_ten_days):
            pages.append(page.copy())
            i += 1
            page = trackobot.history(i)['history']
        return pages

    def serach_pages_younger_than(self, pages, date):
        pages_younger_than = []
        for page in pages:
            if page['added'] > date.isoformat():
                pages_younger_than.append(page)
        if not pages_younger_than:
            print("Page older than 10 days. No card data available.", page['added'])
        return pages_younger_than

    def find_card(self, card, game, max_turn):
        # iterate over all cards used in the game
        for cards in game['card_history']:
            # check that "me" played the card and not opponent
            if (cards['player'] == 'me') & (card in cards['card'].values()) & (cards['turn'] <= max_turn):
                return game
        return False

    def find_hero_deck(self, pages, hero, hero_deck):
        result_games = []
        for page in pages:
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
                # check that "me" played the card and not opponent
                if (cards['player'] == 'me') & (card in cards['card'].values()) & (cards['turn'] <= max_turn):
                    number_card_was_played += 1
            # # number of wins????
        if number_card_was_played < len(valid_games):
            raise Warning("From muligan.number_card_was_played: misuse of function.\
                          Card was not found in all games. Make sure to call this function with only valid games.")
        return number_card_was_played

    def count_wins(self, games):
        number_of_wins = 0
        for game in games:
            if game['result'] == "win":
                number_of_wins += 1
        return number_of_wins

    def evaluate_card(self, card, games, max_turn):
        games_with_card_played = []
        for game in games:
            if self.find_card(card, game, max_turn):
                games_with_card_played.append(self.find_card(card, game, max_turn).copy())

        return games_with_card_played

    def evaluate_deck_list(self, deck_list, games, max_turn):
        result_list = []
        for card in deck_list:
            games_with_card_played = self.evaluate_card(card, games, max_turn)
            card_result = {'card': card,
                           'number of wins with card': self.count_wins(games_with_card_played),
                           'number of games with card': len(games_with_card_played),
                           'times played': self.number_card_was_played(card, games_with_card_played, max_turn)}
            result_list.append(card_result.copy())
        return result_list

    def print_result(self, result_list):
        for result in result_list:
            print("----------------------------------------")
            if result['number of games'] > 0:
                print("Result for", result['opponent_deck'], result['opponent'])
                print("Number of games:", result['number of games'])
                print("Number of wins:", result['number of wins'])
                print("Win %: {0:.2f}".format((result['number of wins']/result['number of games'])*100))
                for cards in result['cards_evaluated']:
                    if cards['times played'] > 0:
                        print("Number of games with card:", cards['number of games with card'])
                        print(cards['card'], "was played", cards['times played'])
                        print("Number of wins with:", cards['card'], cards['number of wins with card'])
                        print("Win %: {0:.2f}".format((cards['number of wins with card']/cards['number of games with '
                                                                                               'card'])*100))
            else:
                print("No games against", result['opponent_deck'], result['opponent'])

    def print_result_to_xlsx(self, result_list, filename="mullipy_results.xlsx"):
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet(self.deck_type[1] + " " + self.deck_type[0])

        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0
        # headlines
        worksheet.write(0, 0, "Opponent Hero")
        worksheet.write(0, 1, "Opponent Deck")
        worksheet.write(0, 2, "Number of wins")
        worksheet.write(0, 3, "Number of losses")
        worksheet.write(0, 4, "Win %")
        worksheet.write(0, 5, "Card")
        worksheet.write(0, 6, "Times played")
        worksheet.write(0, 7, "Number of wins with card")
        worksheet.write(0, 8, "Number of losses with card")
        worksheet.write(0, 9, "Win % with card played")

        for result in result_list:
            if result['number of games'] > 0:
                row += 1
                if not result['opponent_deck']:
                    readable_deck = "Other"
                else:
                    readable_deck = result['opponent_deck']
                worksheet.write(row, col, result['opponent'])
                worksheet.write(row, col + 1, readable_deck)
                worksheet.write(row, col + 2, result['number of wins'])
                worksheet.write(row, col + 3, result['number of games'] - result['number of wins'])
                worksheet.write(row, col + 4, result['number of wins']/result['number of games']*100)
                for cards in result['cards_evaluated']:
                    row += 1
                    worksheet.write(row, col + 5, cards['card'])
                    worksheet.write(row, col + 6, cards['times played'])
                    worksheet.write(row, col + 7, cards['number of wins with card'])
                    worksheet.write(row, col + 8, cards['number of games with card'] -cards['number of wins with card'])
                    if cards['number of games with card'] > 0:
                        worksheet.write(row, col + 9, cards['number of wins with card']/cards['number of games with '
                                                                                          'card']*100)
                    else:
                        worksheet.write(row, col + 9, "N/A")
        workbook.close()

    def load_decklists_from_json(self, path):
        with open(path) as file:
            data = json.load(file)

        opponent_deck_type_tuples_list = []
        for deck in data['decks']:
            if deck['active']:
                opponent_deck_type_tuples_list.append((deck['name'], deck['hero']))
        return opponent_deck_type_tuples_list

    def evaluate2(self):

        pages = self.data
        deck_list = self.deck_list

        # our deck
        hero = self.deck_type[1]
        hero_deck = self.deck_type[0]
        max_turn = self.max_turn

        result_list = []
        # result type example: [{'opponent': 'Shaman', 'opponent_deck': 'Aggro' 'number of games': 3, 'number of
        # wins': 2, 'cards_evaluated': [{'card': 'Eviscerate', 'number of wins with card': 2, 'number of games': 2,
        # 'times played': 1}, {'card': 'Backstab', 'number of wins with card': 1, 'number of games': 1,
        # 'times played': 1}] }]

        valid_games = self.find_hero_deck(pages, hero, hero_deck)

        # opponent deck(s)
        opponent_deck_type_tuples_list = self.opponent_deck_type_tuples_list

        for deck_types in opponent_deck_type_tuples_list:
            opponent = deck_types[1]
            opponent_deck = deck_types[0]

            # get all games vs one archetype
            games_vs_opponent = self.find_opponent_deck(valid_games, opponent, opponent_deck)

            result = {'opponent': opponent, 'opponent_deck': opponent_deck,
                      'number of games': len(games_vs_opponent),
                      'number of wins': self.count_wins(games_vs_opponent),
                      'cards_evaluated': self.evaluate_deck_list(deck_list, games_vs_opponent,
                                                                 max_turn)}

            result_list.append(result.copy())

        return result_list
