import requests
import pandas as pd 

start_year = 2008
end_year = 2023


# Making an empty Dataframe which will hold our final output
total_data = pd.DataFrame([], columns=['Week Ending/Date','Location','Average_Price'])

for year_index in range(start_year,end_year+1):
    res = requests.get(f'https://www.teaboard.gov.in/WEEKLYPRICES/{year_index}')

    if(res.status_code != 200 ):
        print(f"Could not gather the data successfully from the URL of year: {year_index}")
    else:
        print(f"Data successfully gathered from the URL of year: {year_index}")

        # This line reads the Text/Html Content from the URL and makes a list of dataframes
        df_list = pd.read_html(res.content)
        
        # The "WEEKLY AVERAGE PRICES OF TOTAL TEA SOLD AT INDIAN AUCTION DURING - 20xx" is present at index 1
        req_table = df_list[1]

        # Dropping column "Tea serve" as it is not asked in the problem statement
        req_table.drop(['Tea Serve'], axis=1,inplace=True)

        # Melt function in pandas: To keep (WEEK) as constant, (LOCATION) as our variable name, and (Price) as our value for the variable
        req_table_modified = pd.melt(req_table, id_vars='Week Ending/Date', var_name='Location', value_name='Average_Price')
        
        # Concatenating our This_Year data to our TOTAL_DATA 
        total_data = pd.concat([total_data,req_table_modified])

# Storing the parsed data into a CSV file
total_data.to_csv('total_data.csv',index=False)


# If we want the Data to be sorted as per the Date

# total_data['Week Ending/Date'] = pd.to_datetime(total_data['Week Ending/Date'])
# total_data = total_data.sort_values(by='Week Ending/Date')
# total_data['Week Ending/Date'] = total_data['Week Ending/Date'].dt.strftime('%d-%m-%Y')
# total_data = total_data.fillna("NA")
# total_data.to_csv('Sorted_Data.csv',index=False)