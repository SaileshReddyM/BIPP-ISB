import pandas as pd
from pathlib import Path
import json

def convert_json_to_excel():

    project_dir = Path(__file__).parent  

    table_names = ["codebook_wap_city_leaf_dust","codebook_wap_city_tea","codebook_wap_india_leaf_dust","codebook_wap_india_tea"]

    for table in table_names:

        with open(project_dir /f"{table}.json", 'r') as json_file:
            data_dict = json.load(json_file)

        data1 = pd.json_normalize(data_dict['variables'])
        data2 = pd.json_normalize(data_dict['additional_information'])
        data3 = pd.json_normalize(data_dict['metadata'])

        with pd.ExcelWriter(project_dir/f"{table}.xlsx", engine='openpyxl') as writer:

            data1.to_excel(writer, sheet_name='Sheet1', index=False)

            data2.to_excel(writer, sheet_name='Sheet2', index=False)

            data3.to_excel(writer, sheet_name="Sheet3", index=False)

convert_json_to_excel()