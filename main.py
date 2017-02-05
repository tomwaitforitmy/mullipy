import muligan

path_to_data = "C:\\Users\\tommy\\history.json"
deck_type = ("Miracle", "Rogue")
deck_list = ["Counterfeit Coin","Backstab","Preparation", "Small-Time Buccaneer", "Patches, the Pirat", "Swashburglar", "Cold Blood", "Eviscerate", "Sap","Bloodmage Thalnos", "Fan of Knives", "SI:7 Agent", "Edwin VanCleef", "Shaku, the Collector", "Tomb Pillager", "Azure Drake", "Leeroy Jenkins", "Gadgetzan Auctioneer"]
opponent_deck_type_tuples_list = [("Aggro", "Shaman"), ("Midrange", "Shaman"), ("Reno", "Warlock")]
max_turn = 10
calculator = muligan.Muligan(path_to_data, deck_type, opponent_deck_type_tuples_list, deck_list, max_turn)
calculator.evaluate()
