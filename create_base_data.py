import os
import pandas as pd

#Folder Path
folder_path = "C:/Users/sriva/OneDrive/Chicago Booth/Braintrust Data/VC Scraping list"

#Initialize an empty DataFrame to hold all the data
all_data = pd.DataFrame()

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        # Read the CSV file into a DataFrame
        data = pd.read_csv(file_path)
        # Append the data to the all_data DataFrame
        all_data = pd.concat([all_data, data], ignore_index=True)

# De-duplicate the data based on company names and websites
final_data = all_data.drop_duplicates(subset=['Organization Name', 'Website'])

print(final_data.shape)
final_data.to_csv("master_table.csv")