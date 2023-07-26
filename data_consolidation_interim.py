import glob
import pandas as pd 
import os


def find_text_files(directory):
    pattern = f"{directory}/20??_data/*.csv"  
    return glob.glob(pattern)


def get_interim_data():

    directory_path = "/Users/sailesh/Desktop/BIPP-ISB/raw_data/"

    text_files_in_directory = find_text_files(directory_path)

    if not os.path.exists("interim_data"):
        os.mkdir(f"interim_data")

    if not os.path.exists("interim_data/tea_sold_city"):
        os.mkdir("interim_data/tea_sold_city")
    if not os.path.exists("interim_data/tea_sold_india"):
        os.mkdir("interim_data/tea_sold_india")
    if not os.path.exists("interim_data/leafdust_sold_city"):
        os.mkdir("interim_data/leafdust_sold_city")
    if not os.path.exists("interim_data/leafdust_sold_india"):
        os.mkdir("interim_data/leafdust_sold_india")
            
    for file in text_files_in_directory:
        df = pd.read_csv(file)

        if "india" in file:
            new_column_names = {
                    '0': 'Week Ending/Date',
                    '1': 'NORTH INDIA',
                    '2': 'SOUTH INDIA',
                    '3': 'ALL INDIA',
                }
            
            df.rename(columns=new_column_names, inplace=True)
            df.drop(index=[0,1], inplace=True)
            df.reset_index(drop=True, inplace=True)

        table_modified = pd.melt(df, id_vars='Week Ending/Date', var_name='Location', value_name='Average_Price')
        
        this_year = file.split("/")[6].split("_")[0]
        if "leaf&dust_city" in file:
            table_modified.to_csv(f"interim_data/leafdust_sold_city/{this_year}.csv",index=False)
        if "leaf&dust_india" in file:
            table_modified.to_csv(f"interim_data/leafdust_sold_india/{this_year}.csv",index=False)
        if "tea_city" in file:
            table_modified.to_csv(f"interim_data/tea_sold_city/{this_year}.csv",index=False)
        if "tea_india" in file:
            table_modified.to_csv(f"interim_data/tea_sold_india/{this_year}.csv",index=False)    

get_interim_data()