import numpy as np
from scipy.ndimage import zoom
import os
from skimage.transform import resize

def my_read_bin(cur_inp_file, data_type, input_shape):
  A = np.fromfile(cur_inp_file, dtype = data_type)
  A[np.isnan(A)] = 0
  A = np.reshape(A, input_shape)
  #A = np.transpose(A, [2, 1, 0])
  return A

def my_write_bin(cur_out_file, data_type, data):
  #data = np.transpose(data, [2, 1, 0])
  data.astype(data_type).tofile(cur_out_file)
  return


# Function to process a single file
def process_file(input_filepath, output_filepath):
    # Open and read the binary file
    
        # Read the binary image file into a matrix
    data = my_read_bin(input_filepath, np.float32, [30, 128, 128])
    
    # Write the subsampled image matrix to the output file
    #data= np.transpose(data, [0, 2, 1])
    
    
    
    # Rotate the x, y dimensions of each slice by 90 degrees clockwise
    #data = np.rot90(data, k=-1, axes=(1, 2))
    
    # Compress the data to the new dimensions (64, 64, 30)
    compression_factor = (1, 64 / 128, 64 / 128)
    compressed_data = zoom(data, compression_factor, order=1)
    #compressed_data = resize(data, (30, 64, 64), order=1, preserve_range=True, anti_aliasing=True)
    compressed_data=compressed_data*4
    # Save the compressed data back to a binary file
    
    compressed_data.tofile(output_filepath)
    #my_write_bin(compressed_data, np.float32, data)
    print(f"Compressed data saved to {output_filepath}")

# Define the input and output directories
input_directory = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/hl'
output_directory = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/processed_hl'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Process each .a00 file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.a00'):
        input_filepath = os.path.join(input_directory, filename)
        output_filepath = os.path.join(output_directory, filename)
        process_file(input_filepath, output_filepath)