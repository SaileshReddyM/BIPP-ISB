import requests
import pandas as pd 
import os

def table_name(i,this_year):
    if i == 0:
        return f"{this_year}_data/wap_leaf&dust_city_{this_year}.csv"
    if i == 1:
        return f"{this_year}_data/wap_tea_city_{this_year}.csv"
    if i == 2:
        return f"{this_year}_data/wap_leaf&dust_india_{this_year}.csv"
    if i == 3:
        return f"{this_year}_data/wap_tea_india_{this_year}.csv"
    else:
        return f"{this_year}_data/additional_table.csv"

def get_year_to_year_data(year1,year2):
    
    start_year = year1
    end_year = year2

    # total_data = pd.DataFrame([], columns=['week ending/date','location','average_price'])

    for year_index in range(start_year,end_year+1):
        res = requests.get(f'https://www.teaboard.gov.in/WEEKLYPRICES/{year_index}')

        if(res.status_code != 200 ):
            print(f"Could not gather the data successfully from the URL of year: {year_index}")
        else:

            if not os.path.exists(f"{year_index}_data"):
                os.mkdir(f"{year_index}_data")
            
            df_list = pd.read_html(res.content)

            for i in range(0,len(df_list)-1):
                df_list[i].to_csv(table_name(i,year_index),index=False)
            
            

get_year_to_year_data(2008,2023)

