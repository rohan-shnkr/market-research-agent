import pandas as pd
from data_load import base_load

def return_base_data(path):
    data = base_load(path)
    print("DATA IMPORTED")

    #returning columns needed for content analysis
    data = data[['Organization Name', 'Website']]
    data.rename(columns={'Organization Name': 'Company', 'Website': 'Homepage'}, inplace=True)
    return data

def store_data_for_post_process(path):
    data = base_load(path)
    data = data[['Organization Name', 'Number of Employees', 'Estimated Revenue Range', 'Industries']]
    # print(data.head())

    data = data.rename(columns={'Organization Name': 'Company', 'Number of Employees': 'total_employees', 'Estimated Revenue Range': 'revenue_range', 'Industries': 'industries'})
    # print(data.head())

    data['total_employees'] = data['total_employees'].replace({'Nov-50': '11-50', '10-Jan':'1-10'})
    print(data.head())

    return data
