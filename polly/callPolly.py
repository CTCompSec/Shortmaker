"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from datetime import datetime
import re

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
import boto3

# Define the path to the input file
input_file_path = "/home/carlos/ShortMaker/zuki/zukioutput.txt"

# Read the content of the file
with open(input_file_path, "r") as file:
    content = file.read()

# Use regular expressions to find the text wrapped in [SCRIPT]...[/SCRIPT] tags and [TITLE]...[/TITLE] tags
script_match = re.search(r'\[SCRIPT\](.*?)\[/SCRIPT\]', content, re.DOTALL)
title_match = re.search(r'\[TITLE\](.*?)\[/TITLE\]', content, re.DOTALL)

# Extract the script content if found
if script_match:
    script_content = script_match.group(1)
else:
    script_content = None
    print("No [SCRIPT] tags found in the file.")

# Extract the title content if found
if title_match:
    title_content = title_match.group(1)
else:
    title_content = None
    print("No [TITLE] tags found in the file.")

title = title_content

inputMessage = script_content

print(title)


session = Session(profile_name="default")
polly = session.client("polly")

output_dir = "/home/carlos/ShortMaker/polly/pollyOutput"
log_file = "/home/carlos/ShortMaker/polly/pollylog.txt"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def log_response(message):
    """Logs messages to the log file with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as log:
        log.write(f"{timestamp} - {message}\n")

try:
    # Request speech synthesis
    response = polly.synthesize_speech(Text=str({inputMessage}), OutputFormat="mp3", VoiceId="Joanna")
except (BotoCoreError, ClientError) as error:
    # Log the error and exit
    log_response(f"Error: {error}")
    print(error)
    sys.exit(-1)

# Access the audio stream from the response
if "AudioStream" in response:
    title_str = str(title_content).strip()
    output = os.path.join(output_dir, f"{title_str}.mp3")
    try:
        # Open a file for writing the output as a binary stream
        with closing(response["AudioStream"]) as stream:
            with open(output, "wb") as file:
                file.write(stream.read())
        # Log the successful response
        log_response(f"Audio file saved to {output}")
    except IOError as error:
        # Log the error and exit
        log_response(f"IOError: {error}")
        print(error)
        sys.exit(-1)
else:
    # The response didn't contain audio data, log and exit
    log_response("Could not stream audio")
    print("Could not stream audio")
    sys.exit(-1)







