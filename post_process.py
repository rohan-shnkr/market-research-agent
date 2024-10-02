import pandas as pd
from pre_process import store_data_for_post_process

def post_process(data, path):
    #Generating a score column
    score_dict = {'high':1, 'medium':0.5, 'low': 0}
    data_ext = store_data_for_post_process(path)
    data['score'] = data['AI_response'].str.lower().map(score_dict)

    #grouping and storing in a new data
    new_df = data.groupby('Company').agg(mean_score = ('score','mean'), total_datapoints = ('url','nunique')).reset_index()
    new_df = pd.merge(data_ext, new_df, on='Company', how='left')
    new_df = new_df.dropna(subset=['total_datapoints'])

    #Adding Employee Tiers
    new_df['emp_tier'] = new_df['total_employees'].apply(lambda x: employee_tier(x))

    #Final Tiering Companies
    new_df['Tier_v1'] = new_df.apply(lambda row: ai_interest_v1(row), axis=1)
    new_df['Tier_v2'] = new_df.apply(lambda row: ai_interest_v2(row), axis=1)

    return new_df

def ai_interest_v1(row):
    if row['emp_tier']==1:
        if row['mean_score']>0.75 and row['total_datapoints']>3:
            return 'Tier 1'
        elif row['mean_score']>0.5 and row['total_datapoints']>=5:
            return 'Tier 1'
        elif (0 < row['mean_score'] <=0.5) and row['total_datapoints']>=5:
            return 'Tier 2'
        else:
            return 'Not AI Invested'
    elif row['emp_tier']==2:
        if row['mean_score']>0.75 and row['total_datapoints']>5:
            return 'Tier 1'
        elif row['mean_score']>0.5 and row['total_datapoints']>=5:
            return 'Tier 2'
        elif (0 < row['mean_score'] <=0.5) and row['total_datapoints']>=5:
            return 'Tier 3'
        else:
            return 'Not AI Invested'
    else:
        if row['mean_score']>0.75 and row['total_datapoints']>8:
            return 'Tier 2'
        elif row['mean_score']>0.5 and row['total_datapoints']>=5:
            return 'Tier 3'
        elif (0 < row['mean_score'] <=0.5) and row['total_datapoints']>=5:
            return 'Tier 3'
        else:
            return 'Not AI Invested'
        
def ai_interest_v2(row):
    if row['emp_tier']==1:
        if row['total_datapoints']>1:
            if row['mean_score'] > 0.5:
                return 'Tier 1'
            elif row['mean_score'] > 0.2:
                return 'Tier 2'
            else:
                return 'Not AI Invested'
        elif row['total_datapoints']==1 and row['mean_score']==1:
            return 'Tier 1'
        else:
            return 'Not AI Invested'
    elif row['emp_tier']==2:
        if row['total_datapoints']>1:
            if row['mean_score'] >= 0.7 and row['total_datapoints']>=5:
                return 'Tier 1'
            elif row['mean_score'] > 0.5:
                return 'Tier 2'
            elif row['mean_score'] > 0.2:
                return 'Tier 3'
            else:
                return 'Not AI Invested'
        elif row['total_datapoints']==1 and row['mean_score']==1:
            return 'Tier 2'
        else:
            return 'Not AI Invested'
    else:
        if row['total_datapoints']>1:
            if row['mean_score'] >= 0.6:
                return 'Tier 2'
            elif row['mean_score'] > 0.2:
                return 'Tier 3'
            else:
                return 'Not AI Invested'
        elif row['total_datapoints']==1 and row['mean_score']==1:
            return 'Tier 3'
        else:
            return 'Not AI Invested'
        
    
def employee_tier(employees):
    if employees in ['1-10', '11-50', '51-100']:
        return 3
    elif employees in ['101-250', '251-500']:
        return 2
    else:
        return 1

def save_new_data_to_csv(data, name):
    data.to_csv(name)

# if __name__ == "__main__":
#     data = pd.read_csv("C:/Users/sriva/Personal_Projects/WebScraper/temp.csv", index_col=False)
#     path = "C:/Users/sriva/Personal_Projects/WebScraper/sample.csv"
#     new_data = post_process(data, path)
#     # final_data = new_data[new_data['AI_Investment'] != 'Low']
#     save_new_data_to_csv(new_data, "My_output.csv")