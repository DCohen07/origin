import numpy as np
import pandas as pd
import config

xag = pd.read_csv("/home/dancoh/Documents/attract_DE_test/xag.csv", header = None, names = ["userId", "itemId", "rating", "timestamp"])

def lookupFiles(item_to_keep, path_to_copy, filename):
    
    lookupDF = pd.DataFrame(xag[item_to_keep])
    lookupDF.drop_duplicates(keep = "first", inplace = True, ignore_index = True)
    lookupDF.reset_index(inplace = True)
    lookupDF.rename(columns = {"index": item_to_keep + f"AsInteger"}, inplace = True)
    lookupDF.to_csv(f"{path_to_copy}{filename}", header = True, index = False)

    return lookupDF

lookupuser = lookupFiles("userId", "/home/dancoh/Documents/attract_DE_test/", "lookupuser.csv")
lookup_product = lookupFiles("itemId", "/home/dancoh/Documents/attract_DE_test/", "lookup_product.csv")

dataset_join = xag.merge(lookupuser, on = "userId", how = "left").merge(lookup_product, on = "itemId", how = "left")

def aggregateFile(path_to_copy, filename):
    
    agg_rating = dataset_join.groupby(by = ["userIdAsInteger", "itemIdAsInteger"]).agg({"rating": "sum", "timestamp": "first"})
    max_date = agg_rating.timestamp.max()
    day_in_second = 86400
    penalty = 0.95
    threshold = 0.01

    agg_rating.timestamp = ((max_date - agg_rating.timestamp) / day_in_second).apply(np.floor)
    agg_rating.rating = agg_rating.rating*(penalty**agg_rating.timestamp)
    agg_rating["validate"] = np.where(agg_rating.rating > threshold, True, False)
    agg_rating = agg_rating[agg_rating.validate == True].drop(["timestamp","validate"], axis = 1)
    agg_rating.to_csv(f"{path_to_copy}{filename}", header = True, index = False)

    return agg_rating

aggregateFile()