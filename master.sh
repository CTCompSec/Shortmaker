#!/bin/bash


# Prompt the user for input
echo "Enter some text (press Enter twice to finish):"

# Initialize variable to store input
input_text=""

# Read input line by line until a blank line is entered
while IFS= read -r line; do
    # Append the line to input_text
    input_text+="$line"
    input_text+="\n"  # Add newline to maintain line breaks
    # Check if the line is empty (user pressed Enter without typing anything)
    if [ -z "$line" ]; then
        break
    fi
done

# Specify the file where the input will be saved
file_name="./zuki/zukiinput.txt"

# Echo the input to the file
echo -e "$input_text" > "$file_name"

# Notify the user that input has been saved
echo "Input has been saved to $file_name"

python3 /home/carlos/ShortMaker/zuki/zukicaller.py

sleep 8

python3 /home/carlos/ShortMaker/polly/callPolly.py

sleep 10

python3 /home/carlos/ShortMaker/pexels/callpexels.py

sleep 10


python3 /home/carlos/ShortMaker/ffmpeg/ffmpegPrep.py

sleep 5

bash /home/carlos/ShortMaker/ffmpeg/script.sh

sleep 100
