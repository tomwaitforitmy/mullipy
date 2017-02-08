import muligan
from pprint import pprint

path_to_data = "C:\\Users\\tommy\\page08022017.json"
deck_type = ("Miracle", "Rogue")
#deck_list = ["Counterfeit Coin","Backstab","Preparation", "Small-Time Buccaneer", "Patches, the Pirat", "Swashburglar", "Cold Blood", "Eviscerate", "Sap","Bloodmage Thalnos", "Fan of Knives", "SI:7 Agent", "Edwin VanCleef", "Shaku, the Collector", "Tomb Pillager", "Azure Drake", "Leeroy Jenkins", "Gadgetzan Auctioneer"]
deck_list = ["Counterfeit Coin","Eviscerate"]
opponent_deck_type_tuples_list = [("Aggro", "Shaman"), ("Reno", "Warlock"), ("Pirate", "Warrior"), ("Miracle", "Rogue")]
max_turn = 20
calculator = muligan.Muligan(path_to_data, deck_type, opponent_deck_type_tuples_list, deck_list, max_turn)
result_list = calculator.evaluate2()

#pprint(result_list)

calculator.print_result(result_list)
