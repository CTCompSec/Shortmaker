url = "https://zukijourney.xyzbot.net/v1/chat/completions"
headers = {"Authorization": "Bearer redacted"}

import requests
import os
from datetime import datetime

# Define the paths
input_file_path = '/home/carlos/ShortMaker/zuki/zukiinput.txt'
output_file_path = '/home/carlos/ShortMaker/zuki/zukioutput.txt'
log_file_path = '/home/carlos/ShortMaker/zuki/zukilog.txt'


def main():
    try:
        # Read the input file content
        with open(input_file_path, 'r') as file:
            input_content = file.read().strip()

        # Prepare the message for the API request
        api_input_message = f"Your name is Zuki and you are a professional copywriter who attended a top American University where you studied information technology, European art, and dog training.[ASSIGNMENT] You will generate a script, title, and keywords for a Youtube short based on a prompt. You will wrap each of these in tags like this: [/ASSIGNMENT][TITLE]Did President Roosevelt visit the white house more after his presidency or before?[/TITLE] [KEYWORDS]President, Roosevelt, history, government, white house, united states[/KEYWORDS] [SCRIPT]It's been said many times that Roosevelt was one of our greatest and most memorable presidents.  But is it true that he had a lasting presence in our main building of federal governement even after he officially left office?  It's well known that he visited the white house numerous times throughout his later years.  Perhaps his influence on the world of presidental politics was greater than we had imagined.[/SCRIPT] Here is your prompt: [PROMPT] {input_content} [/PROMPT]"

        # Prepare the data for the API request in the required format
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": api_input_message},
            ]
        }

        # Send the request to the API
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        # Get the output message from the API response
        if response.status_code == 200:
            api_output_message = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            api_output_message = f"Error: {response.status_code} - {response_data.get('error', 'Unknown error')}"

        # Write the output message to the output file
        with open(output_file_path, 'w') as file:
            file.write(api_output_message)


        # Prepare the log entry
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = (
            f"Timestamp: {timestamp}\n"
            f"Input Message: {api_input_message}\n"
            f"Output Message: {api_output_message}\n"
            f"Status Code: {response.status_code}\n\n\n"
        )

        # Append the log entry to the log file
        with open(log_file_path, 'a') as file:
            file.write(log_entry)

    except Exception as e:
        # Handle any exceptions that occur
        with open(log_file_path, 'a') as file:
            error_message = f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            error_message += f"Error: {str(e)}\n\n\n"
            file.write(error_message)

if __name__ == "__main__":
    main()



