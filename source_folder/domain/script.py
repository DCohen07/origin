import numpy as np
import pandas as pd
from source_folder.config.config import read_yaml


# Read config file:

CONFIG = read_yaml()

# Set the config constant

day_in_second = CONFIG["constant"]["day_in_second"]
penalty = CONFIG["constant"]["penalty"]
threshold = CONFIG["constant"]["threshold"]
data_path = CONFIG["data"]["data_path"]
filename_user = CONFIG["data"]["filename_user"]
filename_item = CONFIG["data"]["filename_item"]
path_to_copy = CONFIG["data"]["path_to_copy"]

# Import the input dataframe

xag = pd.read_csv(data_path, header = None, names = ["userId", "itemId", "rating", "timestamp"])

def lookupFiles(item_to_keep, path_to_copy, filename):
    
    """ Create and export in CSV a DataFrame with Id and IdAsInteger
    	Parameters
    	----------
    	item_to_keep: userId or itemId
        path_to_copy: path where the csv file will be copy
        filename: name of the file

    	Returns
    	-------
    	lookupDF: pd.Dataframe
    	"""

    lookupDF = pd.DataFrame(xag[item_to_keep])
    lookupDF.drop_duplicates(keep = "first", inplace = True, ignore_index = True)
    lookupDF.reset_index(inplace = True)
    lookupDF.rename(columns = {"index": item_to_keep + f"AsInteger"}, inplace = True)
    lookupDF.to_csv(f"{path_to_copy}{filename}.csv", header = True, index = False)

    return lookupDF

# Call lookup object to write the csv files
lookupuser = lookupFiles("userId", path_to_copy, filename_user)
lookup_product = lookupFiles("itemId", path_to_copy, filename_item)

# Join the lookupDF to pick the userAsInteger and itemAsInteger columns

dataset_join = xag.merge(lookupuser, on = "userId", how = "left").merge(lookup_product, on = "itemId", how = "left")

def aggratingFile(path_to_copy, filename):
    
    """ Create and export the agg_rating.csv file
        Parameters: 
        ----------
        path_to_copy: path where the csv file will be copy
        filename: name of the file
        
        Returns
    	-------
    	agg_rating: pd.Dataframe
    """

    agg_rating = dataset_join.groupby(by = ["userIdAsInteger", "itemIdAsInteger"]).agg({"rating": "sum", "timestamp": "first"})
    max_date = agg_rating.timestamp.max()

    # We calculate the difference between the current date and the max date then we convert it in days 
    agg_rating.timestamp = ((max_date - agg_rating.timestamp) / day_in_second).apply(np.floor) 
    
    agg_rating.rating = agg_rating.rating*(penalty**agg_rating.timestamp)
    agg_rating["validate"] = np.where(agg_rating.rating > threshold, True, False)
    agg_rating = agg_rating[agg_rating.validate == True].drop(["timestamp","validate"], axis = 1)
    agg_rating.reset_index(inplace = True)
    agg_rating.to_csv(f"{path_to_copy}{filename}.csv", header = True, index = False)

    return agg_rating

agg_file = aggratingFile(path_to_copy, "agg_rating")