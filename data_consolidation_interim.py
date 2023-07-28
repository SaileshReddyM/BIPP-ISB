import glob
import pandas as pd 
from pathlib import Path


def get_interim_data():

    project_dir = Path(__file__).parent    
    raw_data_dir = project_dir / "raw_data"             
    interim_data_dir = project_dir / "interim_data"

    interim_data_dir.mkdir(parents=True,exist_ok=True)

    table_names = ["wap_tea_city","wap_tea_india","wap_leaf_and_dust_city","wap_leaf_and_dust_india"]

    for table_name in table_names:
         
        table_data_all_years = [ pd.read_csv(file)
                            for file in glob.glob(f"./raw_data/**/{table_name}_*.csv")]
        
        if "india" in table_name:
            new_column_names = {
                    '0': 'Week Ending/Date',
                    '1': 'NORTH INDIA',
                    '2': 'SOUTH INDIA',
                    '3': 'ALL INDIA',
                }
            for df in table_data_all_years:
                df.rename(columns=new_column_names, inplace=True)
                df.drop(index=[0,1], inplace=True)
                df.reset_index(drop=True, inplace=True)
        
        table_data_all_years_melted = [ pd.melt(df, id_vars='Week Ending/Date', var_name='Location', value_name='Average_Price')
                            for df in table_data_all_years]
        
        concat_table = pd.concat(table_data_all_years_melted)

        column_names_in_table = concat_table.columns

        for column_name in column_names_in_table:
            if(column_name == "Average_Price"):
                concat_table['Bracketed_val_avg_price'] = concat_table[column_name].str.extract(r'\((.*?)\)')
                concat_table['Bracketed_val_avg_price'] = concat_table['Bracketed_val_avg_price'].str.strip()
                concat_table['Average_price'] = concat_table[column_name].str.extract(r'^(.*?)\(')
                concat_table['Average_price'] = concat_table['Average_price'].str.strip()

                concat_table.drop(columns=column_name, inplace=True)
        
        concat_table["Bracketed_val_avg_price"] = concat_table["Bracketed_val_avg_price"].fillna("NA")
        concat_table["Bracketed_val_avg_price"] = concat_table["Bracketed_val_avg_price"].replace({"NS": "NA", "N.S.": "NA","N.S": "NA","(N.S":"NA", "(N.S)":"NA"}, regex=False)
        concat_table["Average_price"] = concat_table["Average_price"].fillna("NA")
        concat_table["Average_price"] = concat_table["Average_price"].replace({"NS": "NA", "N.S.": "NA", "N.S": "NA","(N.S)":"NA","(N.S":"NA"}, regex=False)


   

        print(concat_table)
        concat_table.to_csv(f"./interim_data/{table_name}.csv")





get_interim_data()