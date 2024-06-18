import os
import re
from mutagen.mp3 import MP3
import subprocess
import time

time.sleep(10)

# Path to the zukioutput.txt file
zuki_output_path = '/home/carlos/ShortMaker/zuki/zukioutput.txt'

# Function to extract video title from the zukioutput.txt file
def extract_video_title(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
        match = re.search(r'\[TITLE\](.*?)\[/TITLE\]', content, re.DOTALL)
        if match:
            return match.group(1).strip()
    return None

# Function to get the length of the audio file in seconds
def get_audio_length(audio_filepath):
    audio = MP3(audio_filepath)
    return int(audio.info.length)

# Function to count the number of files in a directory
def count_files_in_directory(directory):
    if os.path.isdir(directory):
        return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    return 0

# Extract video title
videoTitle = extract_video_title(zuki_output_path)

if videoTitle:
    # Path to the audio file
    audio_file_path = f'/home/carlos/ShortMaker/polly/pollyOutput/{videoTitle}.mp3'

    # Get the audio length in seconds
    audioLength = get_audio_length(audio_file_path)

    # Path to the directory containing video files
    video_files_directory = f'/home/carlos/ShortMaker/pexels/assets/{videoTitle}'

    # Count the number of files in the directory
    numVideoFiles = count_files_in_directory(video_files_directory)

    # Path to the output file
    output_file_path = '/home/carlos/ShortMaker/ffmpeg/pexelsTemp.txt'

    # Write the results to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(f'{videoTitle}\n{audioLength}\n{numVideoFiles}\n')

    print(f'Successfully written to {output_file_path}')
else:
    print('No video title found in the specified file.')

'''

import subprocess

def run_bash_script():
    try:
        # Execute the bash script
        result = subprocess.run(['bash', '/home/carlos/ShortMaker/ffmpeg/script.sh'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Print the output and error (if any)
        print("Output:")
        print(result.stdout.decode('utf-8'))
        print("Error (if any):")
        print(result.stderr.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the script: {e}")

if __name__ == "__main__":
    run_bash_script()

'''
