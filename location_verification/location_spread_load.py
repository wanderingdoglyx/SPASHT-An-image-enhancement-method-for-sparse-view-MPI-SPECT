import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import datetime

pilot_study_folder_path='/home/y.zezhang/2024_false_defect_project/location_verification/pilot_study'

def actual_coordinate(x,y,number_of_image_row=15,number_of_image_column=4):
    
    block_length_x=1/number_of_image_row
    block_length_y=1/number_of_image_column
    
    actual_x=np.array(x) % block_length_x
    actual_y=np.array(y) % block_length_y
    
    return actual_x,actual_y
# Function to process the coordinates column
def process_coordinates(coordinates):
    x = []
    y = []
    for coord in coordinates:
        # Remove parentheses and split by comma
        coord = coord.replace('(', '').replace(')', '')
        coord = coord.replace('X=', '').replace('Y=', '')
        coord_split = coord.split(',')
        
        # Convert strings to numbers and store in arrays
        x.append(float(coord_split[0]))
        y.append(float(coord_split[1]))
    return x, y

# Function to read CSV file and store in arrays
def read_csv_to_arrays(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Convert DataFrame to list of arrays
    arrays = df.values.tolist()

    return arrays

# Function to read all CSV files in a folder
def read_all_csvs_in_folder(folder_path):
    # List to store data from all files
    all_data = []

    # Get all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    # Loop through each file and read its data
    for file in csv_files:
        print(f'Reading {file}...')
        data_arrays = read_csv_to_arrays(file)
        all_data.append(data_arrays)

    return all_data


# Read the first CSV file da
filename_da_first = 'results_first_row_da.csv' # replace with your actual file name
data_da_first = pd.read_csv(filename_da_first)

# Extract and process the Coordinates column from the first file
x_da_first, y_da_first = process_coordinates(data_da_first['Coordinates'])
actual_x_da_first,actual_y_da_first=actual_coordinate(x_da_first, y_da_first)


# Read the second CSV file da
filename_da_second = 'results_second_row_da.csv' # replace with your actual file name
data_da_second = pd.read_csv(filename_da_second)

# Extract and process the Coordinates column from the second file
x_da_second, y_da_second = process_coordinates(data_da_second['Coordinates'])
actual_x_da_second,actual_y_da_second=actual_coordinate(x_da_second, y_da_second)


# Read the first CSV file di
filename_di_first = 'results_first_row_di.csv' # replace with your actual file name
data_di_first = pd.read_csv(filename_di_first)

# Extract and process the Coordinates column from the first file
x_di_first, y_di_first = process_coordinates(data_di_first['Coordinates'])
actual_x_di_first,actual_y_di_first=actual_coordinate(x_di_first, y_di_first)


# Read the second CSV file di
filename_di_second = 'results_second_row_di.csv' # replace with your actual file name
data_di_second = pd.read_csv(filename_di_second)

# Extract and process the Coordinates column from the second file
x_di_second, y_di_second = process_coordinates(data_di_second['Coordinates'])
actual_x_di_second,actual_y_di_second=actual_coordinate(x_di_second, y_di_second)

actual_x_da=np.concatenate((actual_x_da_first,actual_x_da_second))
actual_y_da=np.concatenate((actual_y_da_first,actual_y_da_second))
actual_x_di=np.concatenate((actual_x_di_first,actual_x_di_second))
actual_y_di=np.concatenate((actual_y_di_first,actual_y_di_second))

da_range_x=[min(actual_x_da),max(actual_x_da)]
da_range_y=[min(actual_y_da),max(actual_y_da)]
di_range_x=[min(actual_x_di),max(actual_x_di)]
di_range_y=[min(actual_y_di),max(actual_y_di)]

polit_data=read_all_csvs_in_folder(pilot_study_folder_path)

