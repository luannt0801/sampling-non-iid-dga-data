import os
import numpy as np
import pandas as pd
import random

def return_name_folder(parent_folder):
    for folder_name in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, folder_name)
        if os.path.isdir(folder_path):
            print("Subfolder:", folder_name)
            return folder_name

def return_file_name(folder_path):
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            print("File:", file_name)
            return file_name

def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            print("Content of", file_path, ":\n", content)
    except FileNotFoundError:
        print("File", file_path, "not found!")

def save_dataframe():
    data_folder = 'data'
    dga_types = [dga_type for dga_type in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, dga_type))]
    print(dga_types)
    my_df = pd.DataFrame(columns=['domain', 'type', 'label'])
    for dga_type in dga_types:
        files = os.listdir(os.path.join(data_folder, dga_type))
        for file in files:
            with open(os.path.join(data_folder, dga_type, file), 'r') as fp:
                domains_with_type = [[(line.strip()), dga_type, 1] for line in fp.readlines()]
                appending_df = pd.DataFrame(domains_with_type, columns=['domain', 'type', 'label'])
                my_df = pd.concat([my_df, appending_df], ignore_index=True)

    with open(os.path.join(data_folder, 'benign.txt'), 'r') as fp:
        domains_with_type = [[(line.strip()), 'benign', 0] for line in fp.readlines()[:60000]]
        appending_df = pd.DataFrame(domains_with_type, columns=['domain', 'type', 'label'])
        my_df = pd.concat([my_df, appending_df], ignore_index=True)
    
    return my_df

def sampling_noniid_data(df, fraction, num_labels, n):
    label_data_list = []

    num_samples_total = len(df)
    num_samples_per_label = int(fraction * num_samples_total / num_labels)

    # random_labels = random.sample(df['type'].unique(), n)
    random_labels = random.sample(df['type'].unique().tolist(), n)

    print("random label: ", random_labels)
    # for label_name in df['type'].unique():
    for label_name in random_labels:
        print("Cac label: ",label_name)
        label_df = df[df['type'] == label_name]
        label_data = label_df.sample(n=num_samples_per_label, replace=True, random_state=0)
        label_data_list.append(label_data)
    final_df = pd.concat(label_data_list)
    return final_df


if __name__ == "__main__":
    data_raw_frame = save_dataframe()
    data_raw_frame.to_excel('dataframe.xlsx', index=False)

    # count sample - label
    sample_counts_per_label = data_raw_frame.groupby('type').size()
    # print("\nSố lượng mẫu của từng nhãn raw:")
    # print(sample_counts_per_label)

    noniid_dataframe = sampling_noniid_data(data_raw_frame,0.3,2,4)
    print(noniid_dataframe)
    noniid_count = noniid_dataframe.groupby('type').size()
    print("\nSố lượng mẫu của từng nhãn:")
    print(noniid_count)
    text_file_path = "iid_data_2.txt"
    noniid_dataframe.to_csv(text_file_path, sep='\t', index=False)
    
    print("DataFrame saved to text file successfully!")

    # random_labels = data_raw_frame['type'].sample(5)
    # print(random_labels)