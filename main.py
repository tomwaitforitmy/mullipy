import mulligan
from pprint import pprint

#path_to_data = "C:\\Users\\tommy\\page08022017.json"

path_to_data = "userdata.track-o-bot.json"
deck_type = ("Miracle", "Rogue")
#deck_list = ["Counterfeit Coin", "Backstab"]
deck_list = ["Counterfeit Coin","Backstab","Preparation", "Small-Time Buccaneer", "Patches the Pirate", "Swashburglar", "Cold Blood", "Eviscerate", "Sap","Bloodmage Thalnos", "Fan of Knives", "SI:7 Agent", "Edwin VanCleef", "Shaku, the Collector", "Tomb Pillager", "Azure Drake", "Leeroy Jenkins", "Gadgetzan Auctioneer"]
opponent_deck_type_tuples_list = []#[("Aggro", "Shaman"),("Jade", "Shaman"), ("Pirate", "Warrior")]
calculator = mulligan.Mulligan(deck_type, opponent_deck_type_tuples_list, deck_list)
result_list = calculator.evaluate_json(path_to_data)

#pprint(result_list)

#calculator.print_result(result_list)
calculator.print_result_to_xlsx(result_list)
