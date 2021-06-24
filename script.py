import pandas as pd

xag = pd.read_csv("/home/dancoh/Documents/attract_DE_test/xag.csv", header = None, names = ["userId", "itemId", "rating", "timestamp"])

def filePreparation(item_to_drop, column_name, path_to_copy, filename):
    
    lookupDF = xag.drop(item_to_drop, axis = 1)
    lookupDF.drop_duplicates(keep = "first", inplace = True, ignore_index = True)
    lookupDF.reset_index(inplace = True)
    lookupDF.rename(columns = {"index": column_name}, inplace = True)
    lookupDF.to_csv(f"{path_to_copy}{filename}", header = True, index = False)
    
