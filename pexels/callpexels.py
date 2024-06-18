import requests
import datetime
import re

import os
import math

from mutagen.mp3 import MP3

import json

def get_mp3_duration(file_path):
    try:
        audio = MP3(file_path)
        audio_info = audio.info
        duration_in_seconds = int(audio_info.length)
        return duration_in_seconds
    except Exception as e:
        print(f"Error: {e}")
        return None

# Placeholder for searchResults array
searchResults = []

# Function to search videos (currently empty)
def searchVideos(query):
    # Define the endpoint and headers
    url = "https://api.pexels.com/videos/search"
    headers = {
        "Authorization": ""
    }

    params = {
        "query": {query},
        "orientation": "landscape"
    }

    # Function to log messages
    def log_message(message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("/home/carlos/ShortMaker/pexels/pexelslog.txt", "a") as log_file:
            log_file.write(f"{timestamp} - {message}\n")

    try:
        # Make the GET request
        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the response to a text filey
            searchResults.append(response.text)
            log_message(f"Query: {query} - Response saved successfully.")
        else:
            error_message = f"Query: {query} - Failed to retrieve data {response.status_code}"
            log_message(error_message)
            print(error_message)

    except Exception as e:
        error_message = f"Query: {query} - An error occurred: {str(e)}"
        log_message(error_message)
        print(error_message)

# Path to zukioutput.txt and pollyOutput directory
zuki_output_file = '/home/carlos/ShortMaker/zuki/zukioutput.txt'
polly_output_directory = '/home/carlos/ShortMaker/polly/pollyOutput/'


# Read the file content
with open(zuki_output_file, 'r') as file:
    content = file.read()

# Extract content between [KEYWORDS] and [/KEYWORDS] tags
keywords_pattern = re.search(r'\[KEYWORDS\](.*?)\[/KEYWORDS\]', content, re.DOTALL)
if keywords_pattern:
    keywords_content = keywords_pattern.group(1)
    # Split the content by commas and strip any extra whitespace
    keyWords = [keyword.strip() for keyword in keywords_content.split(',')]
else:
    keyWords = []

print(f"Keywords {keyWords}")

# Read the zukioutput.txt file to get videoTitle
with open(zuki_output_file, 'r') as file:
    content = file.read()

# Extract content between [TITLE] and [/TITLE] tags
title_pattern = re.search(r'\[TITLE\](.*?)\[/TITLE\]', content, re.DOTALL)
if title_pattern:
    audioTitle = title_pattern.group(1).strip()
else:
    audioTitle = "default_title"  # Default if no title found

# Construct filename for the mp3 file
mp3_filename = f"{audioTitle}.mp3"
mp3_file_path = os.path.join(polly_output_directory, mp3_filename)

# Get the length of the video in seconds (simulation)
audio_length_seconds = get_mp3_duration(mp3_file_path)

# Calculate numVideosNeeded
numVideosNeeded = math.floor(audio_length_seconds / 3)
if numVideosNeeded == 0:
    numVideosNeeded = 1










#uncomment this later, use pexelstemp for now



# Check if numVideosNeeded is smaller than length of keyWords array
if numVideosNeeded < len(keyWords):
    # Call searchVideos() passing in the first numVideosNeeded entries in keyWords
    for i in range(numVideosNeeded):
        searchVideos(keyWords[i])
else:
    # Otherwise, search each entry in keyWords using searchVideos()
    for keyword in keyWords:
        searchVideos(keyword)










# Log the searchResults array
#print("Search results:", searchResults)



# Write searchResults to pexelstemp.txt
output_file_path = '/home/carlos/ShortMaker/pexels/pexelstemp.txt'
with open(output_file_path, 'w') as file:
    for result in searchResults:
        file.write(f"{result}\n")

















'''
#this section is for debugging from temp file
# Assuming pexelstemp.txt is in the current working directory

file_path = './pexelstemp.txt'
searchResults = []

try:
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Attempt to parse each line as JSON
                entry = json.loads(line)
                searchResults.append(entry)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from line: {e}")
                continue

    print("Contents of searchResults:")
    print(searchResults)

except FileNotFoundError:
    print(f"File '{file_path}' not found.")

'''



# Assume searchResults is populated with JSON objects like the example provided

# Initialize arrays
doNotUseIDs = []

# Initialize index for looping through searchResults
index = 0
videosDownloaded = 0


def downloadVideo(url):
    url = url
    headers = {
        "Authorization": "TyWPkfEHN97ZdT19Sd668oUyNRb958kWpxUejouXemhpPMNPFxgYg2H7"
    }
    save_dir = f"/home/carlos/ShortMaker/pexels/assets/{audioTitle}"
    os.makedirs(save_dir, exist_ok=True)

    # Send GET request with headers
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Save the video content to a file
        save_path = os.path.join(save_dir, f"{audioTitle}_{video_file_id}.mp4")
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Video downloaded successfully and saved to {save_path}.")

    else:
        print(f"Failed to download video. Status code: {response.status_code}")




def find_valid_video_file(video_files, min_width=400, max_width=800):
    for video_file in video_files:
        if min_width <= video_file['width'] <= max_width:
            return video_file
    return None


while videosDownloaded < numVideosNeeded:

    print(f"Videos downloaded: {videosDownloaded}")

    # Get current searchResult using modulo to wrap around if needed
    result = searchResults[index % len(searchResults)]
    print(f"This is the search result array num: {index % len(searchResults)}")
    print(f"Type of result: {type(result)}")

    # Check if result is a string and needs to be parsed as JSON

    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}. Skipping this result.")
            index += 1
            continue

    try:

        videos = result['videos']
        print("check2")

        for video in videos:
            valid_video_file = find_valid_video_file(video['video_files'])

            if valid_video_file:
                video_file_id = valid_video_file['id']

                if video_file_id not in doNotUseIDs:
                    url = valid_video_file['link']


                    downloadVideo(url)

                    # Add all video_file ids to the doNotUseIDs list
                    for vf in video['video_files']:
                        doNotUseIDs.append(vf['id'])  # Add video_file_id to do not use list

                    videosDownloaded += 1
                    break  # Exit the loop for this search result

    except KeyError as e:
        print(f"KeyError: {e}. This result may not contain the expected keys.")
    except Exception as e:
        print(f"An error occurred: {e}")

    index += 1  # Move to the next search result

print("Finished downloading videos.")





