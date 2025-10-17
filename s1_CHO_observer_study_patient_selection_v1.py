import os
import random

def list_subfolders(directory):
    """
    List all subfolders in a given directory.

    Parameters:
    directory (str): The path to the directory.

    Returns:
    List[str]: A list of subfolder names.
    """
    try:
        #subfolders = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
        subfolders = [name for name in os.listdir(directory) 
                  if os.path.isdir(os.path.join(directory, name)) and 'hl' not in name]
        return subfolders
    except FileNotFoundError:
        raise Exception(f"The directory {directory} does not exist.")
    except PermissionError:
        raise Exception(f"Permission denied for accessing the directory {directory}.")

def select_subfolders(subfolders, num_to_select, seed):
    """
    Randomly select a given number of subfolders.

    Parameters:
    subfolders (List[str]): A list of subfolder names.
    num_to_select (int): The number of subfolders to select.
    seed (int): The seed for random selection.

    Returns:
    List[str]: A list of selected subfolder names.
    """
    random.seed(seed)
    return random.sample(subfolders, num_to_select)

def select_subsubfolder(subfolder_path, seed):
    """
    Randomly select a sub-subfolder from a given subfolder.

    Parameters:
    subfolder_path (str): The path to the subfolder.
    seed (int): The seed for random selection.

    Returns:
    str: The name of the selected sub-subfolder.
    """
    subsubfolders = list_subfolders(subfolder_path)
    
    #random.seed(seed)
    return random.choice(subsubfolders) if subsubfolders else None
    #return random.sample(subsubfolders, 1)

def main(base_folder, N, M, seed, output_file):
    """
    Main function to execute the selection process and save the results to a text file.

    Parameters:
    folder1 (str): The path to the first folder.
    folder2 (str): The path to the second folder.
    N (int): Number of subfolders to select from the first folder.
    M (int): Number of subfolders to select from the second folder.
    seed (int): The seed for random selection.
    output_file (str): The path to the output text file.
    """
    # List subfolders
    patient_total=list_subfolders(base_folder)
    #subfolders1 = list_subfolders(folder1)
    #subfolders2 = list_subfolders(folder2)

    # Select subfolders from the first folder
    selected1 = select_subfolders(patient_total, N, seed)

    # Select sub-subfolders from the selected subfolders in the first folder
    selected_subsubfolders1 = []
    for subfolder in selected1:
        
        subfolder_path = os.path.join(base_folder,subfolder)
        subsubfolder = select_subsubfolder(subfolder_path, seed)
        if subsubfolder:
            
            #selected_subsubfolders1.append(os.path.join(subfolder, subsubfolder))
            selected_subsubfolders1.append([subfolder +' '+subsubfolder])
   
    #print(selected_subsubfolders1)
    # Select subfolders from the second folder, ensuring no overlap with the first folder selections
    #selected1_base = [os.path.basename(path.split(os.sep)[0]) for path in selected_subsubfolders1]
    available_subfolders2 = [subfolder for subfolder in patient_total if subfolder not in selected1]
    selected2 = select_subfolders(available_subfolders2, M, seed)

    # Record selections to a text file
    with open(output_file, 'w') as file:
        file.write("Selected diseased patients:\n")
        for index, line in enumerate(selected_subsubfolders1):
            
            characters="\n".join(str(character) for character in line)
            #print(characters)
            file.write(characters+'\n')
            
        file.write("\n\nSelected healthy patients:\n")
        file.write("\n".join(selected2))

    print(f"Selection recorded in {output_file}")
    

# Example usage


base_folder = f'/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/testing'

#diseased_folder = "/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/diseased"
#healthy_folder = "/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/healthy"

diseased_patient_number = 96
healthy_patient_number = 96

AC_arr = ['CTAC']

seed = 47
#seed = 49
output_file = "patient_selection.txt"

for ac in AC_arr:
    main(base_folder, diseased_patient_number, healthy_patient_number, seed, output_file)
