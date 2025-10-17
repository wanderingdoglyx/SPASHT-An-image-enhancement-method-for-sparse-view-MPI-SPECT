#!/bin/bash

# Directory containing the MATLAB files (same directory as the script)
DIR="$(dirname "$0")"

# File containing the list of specific MATLAB files to run
FILES_LIST="files_to_run.txt"

# Check if the file containing the list exists
if [ ! -f "$FILES_LIST" ]; then
    echo "File $FILES_LIST does not exist."
    exit 1
fi

# Read the list of files and run each in the background
while IFS= read -r FILE
do
    FILE_PATH="$DIR/$FILE"
    if [ -f "$FILE_PATH" ]; then
        # Extract the base name of the file (without the extension)
        BASENAME=$(basename "$FILE_PATH" .m)
        
        # Run the MATLAB file in the background
        nohup matlab -nodisplay -nosplash -nodesktop -r "run('$FILE_PATH'); exit;" > "$DIR/$BASENAME.log" 2>&1 &
        echo "Started $FILE in the background."
    else
        echo "File $FILE_PATH does not exist."
    fi
done < "$FILES_LIST"

echo "Started all specified MATLAB scripts in the background."