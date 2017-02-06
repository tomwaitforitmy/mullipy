import unittest
import muligan

class MyTest(unittest.TestCase):
    def assert_card_result(self, result_list, opponent, opponent_deck, card, real_times_played, real_wins):
        for results in result_list:
            if(results['opponent'] == opponent) & (results['opponent_deck'] == opponent_deck):
                for cards in results['cards_evaluated']:
                    if(cards['card'] == card):
                        assert(cards['times played'] == real_times_played)
                        assert(cards['number of wins with card'] == real_wins)

    def assert_matchup_result(self, result_list, opponent, opponent_deck, real_number_of_games, real_wins):
        for results in result_list:
            if(results['opponent'] == opponent) & (results['opponent_deck'] == opponent_deck):
                assert(results['number of games'] == real_number_of_games)
                assert(results['number of wins'] == real_wins)

    def test_evalualte(self):
        path_to_data = "C:\\Users\\tommy\\history.json"
        deck_type = ("Miracle", "Rogue")
        deck_list = ["Eviscerate"]
        opponent_deck_type_tuples_list = [("Aggro", "Shaman")]
        max_turn = 10
        calculator = muligan.Muligan(path_to_data, deck_type, opponent_deck_type_tuples_list, deck_list, max_turn)
        result_list = calculator.evaluate2()

        #In this test data set:
        #3 games in total vs Aggro Shaman
        #2 games where won in total
        #1 game with Eviscerate was won
        #Eviscerate was played 3 times
        self.assert_matchup_result(result_list, "Shaman", "Aggro", 3, 2)
        #only one card was evaluated
        assert(result_list[0]['cards_evaluated'][0]['number of wins with card'] == 1)
        assert(result_list[0]['cards_evaluated'][0]['times played'] == 3)

    def test_evalualte_with_complex_input(self):
        path_to_data = "C:\\Users\\tommy\\history.json"
        deck_type = ("Miracle", "Rogue")
        deck_list = ["Eviscerate"]
        opponent_deck_type_tuples_list = [("Aggro", "Shaman"), ("Midrange", "Shaman"), ("Reno", "Warlock")]
        max_turn = 10
        calculator = muligan.Muligan(path_to_data, deck_type, opponent_deck_type_tuples_list, deck_list, max_turn)
        result_list = calculator.evaluate2()

        #I get lucky here because Aggro Shaman is the first result
        #In this test data set:
        #3 games in total vs Aggro Shaman
        #2 games where won in total
        #1 game with Eviscerate was won
        #Eviscerate was played 3 times
        self.assert_card_result(result_list, "Shaman", "Aggro", "Eviscerate", 3, 1)
        self.assert_matchup_result(result_list, "Shaman", "Aggro", 3, 2)

    def test_evalualte_with_complex_page_input(self):
        path_to_data = "C:\\Users\\tommy\\page08022017.json"
        deck_type = ("Miracle", "Rogue")
        deck_list = ["Eviscerate", "Counterfeit Coin"]
        opponent_deck_type_tuples_list = [("Aggro", "Shaman"), ("Reno", "Warlock"), ("Pirate", "Warrior"), ("Miracle", "Rogue")]
        max_turn = 20
        calculator = muligan.Muligan(path_to_data, deck_type, opponent_deck_type_tuples_list, deck_list, max_turn)
        result_list = calculator.evaluate2()

        #Score vs e.g. Aggro Shaman 2 wins 2 loses
        self.assert_matchup_result(result_list, "Shaman", "Aggro", 4, 2)
        self.assert_matchup_result(result_list, "Warrior", "Pirate", 1, 0)
        self.assert_matchup_result(result_list, "Rogue", "Miracle", 1, 0)
        self.assert_matchup_result(result_list, "Warlock", "Reno", 0, 0) #no match recorded

        #Eviscerate for instance was played 3 times and has 0 wins vs Aggro Shaman
        self.assert_card_result(result_list, "Shaman", "Aggro", "Eviscerate", 3, 0)
        self.assert_card_result(result_list, "Warrior", "Pirate", "Eviscerate", 1, 0)
        self.assert_card_result(result_list, "Rogue", "Miracle", "Eviscerate", 1, 0)
        self.assert_card_result(result_list, "Warlock", "Reno", "Eviscerate", 0, 0) #not played

        self.assert_card_result(result_list, "Shaman", "Aggro", "Counterfeit Coin", 3, 1)
        self.assert_card_result(result_list, "Warrior", "Pirate", "Counterfeit Coin", 1, 0)
        self.assert_card_result(result_list, "Rogue", "Miracle", "Counterfeit Coin", 0, 0) #not played
        self.assert_card_result(result_list, "Warlock", "Reno", "Counterfeit Coin", 0, 0) #not played

    def test_evalualte_with_empty_opponent_list(self):
        path_to_data = "C:\\Users\\tommy\\page08022017.json"
        deck_type = ("Miracle", "Rogue")
        deck_list = ["Eviscerate", "Counterfeit Coin"]
        opponent_deck_type_tuples_list = []
        max_turn = 20
        calculator = muligan.Muligan(path_to_data, deck_type, opponent_deck_type_tuples_list, deck_list, max_turn)
        result_list = calculator.evaluate2()

        #Score vs e.g. Aggro Shaman 2 wins 2 loses
        self.assert_matchup_result(result_list, "All", "All", 6, 2)

        #Eviscerate for instance was played 3 times and has 0 wins vs Aggro Shaman
        self.assert_card_result(result_list, "All", "All", "Eviscerate", 5, 0)

        self.assert_card_result(result_list, "Shaman", "Aggro", "Counterfeit Coin", 4, 1)

if __name__ == '__main__':
    unittest.main()
