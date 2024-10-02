import pandas as pd

if __name__ == "__main__":
    path = "C:/Users/sriva/Personal_Projects/WebScraper/current_input/new_master.csv"
    df = pd.read_csv(path)

    num_splits = 20
    rows_per_split = len(df) // num_splits

    # Split the DataFrame and save each part as a new CSV file
    for i in range(num_splits):
        start_row = i * rows_per_split
        if i == num_splits - 1:  # for the last split, include all remaining rows
            end_row = len(df)
        else:
            end_row = (i + 1) * rows_per_split
    
        split_df = df.iloc[start_row:end_row]
        split_df.to_csv(f'C:/Users/sriva/Personal_Projects/WebScraper/current_input/split_input/input_data_{i+1}.csv', index=False)