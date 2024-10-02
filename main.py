import pandas as pd
from openAI_test import run_AI_check
from pre_process import return_base_data
from post_process import post_process
from post_process import save_new_data_to_csv

#Always clear the split_output folder before running the code to maintain cleanliness in the final output

if __name__ == "__main__":
    input_path = "C:/Users/sriva/Personal_Projects/WebScraper/current_input/split_input/"
    temp_path = "C:/Users/sriva/Personal_Projects/WebScraper/current_output/temp_output/"
    output_path = "C:/Users/sriva/Personal_Projects/WebScraper/current_output/split_output/"
    # path = "C:/Users/sriva/Personal_Projects/WebScraper/new_sample01.csv"

    scrape_split = 13
    #running for batch 1 to 5
    for i in range(13, 20):
        print(f'---------ITERATION-{i+1}--------------------------------------------------------')
        data_path = input_path+f'input_data_{i+1}.csv'
        
        base_data = return_base_data(data_path)
        print("Base Data Ready")

        if i<scrape_split:
            main_data = run_AI_check(base_data, i, False)
            new_temp_path = temp_path+f'temp_ext_{i+1}.csv'
        else:
            main_data = run_AI_check(base_data, i, True)
            new_temp_path = temp_path+f'temp_{i+1}.csv'

        main_data.to_csv(new_temp_path, index=False)
        print("AI Evaluation Complete, data saved")

        main_data_post_process = post_process(main_data, data_path)

        new_output_path = output_path+f'final_output_{i+1}.csv'
        save_new_data_to_csv(main_data_post_process, new_output_path)
        print(f"Final Output of Iteration: {i+1} saved")


    #load initial data 
    # base_data = return_base_data(path)

    #run AI check
    # main_data = run_AI_check(base_data)
    # main_data.to_csv("new_temp01.csv")

    # post processing of data
    # main_data_post_process = post_process(main_data, path)

    # #saving
    # save_new_data_to_csv(main_data_post_process, "new_FINAL01.csv") 