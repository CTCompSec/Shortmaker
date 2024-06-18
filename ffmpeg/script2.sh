#!/bin/bash

'''
input_file="/home/carlos/ShortMaker/ffmpeg/final_video.mp4"
output_file="/home/carlos/ShortMaker/ffmpeg/final_video2.mp4"

# Duration of the fades (in seconds)
fade_duration=0.5

# Temporary filename for intermediate step
temp_file="temp.mp4"

# Step 1: Add fade in from black
ffmpeg -y -i "$input_file" -filter_complex "fade=t=in:st=0:d=$fade_duration" "$temp_file"

# Step 2: Add fade out to black
ffmpeg -y -i "$temp_file" -filter_complex "fade=t=out:st=0:d=$fade_duration" "$output_file"

sleep 8

# Cleanup: Remove temporary file
rm "$temp_file"

echo "Fades added successfully. Output saved to $output_file"

'''

# Read variables from input file
input_file="/home/carlos/ShortMaker/ffmpeg/pexelsTemp.txt"  # Assuming your input file is named input.txt
title=$(sed -n '1p' "$input_file")

# Variables for file paths
audio_file="/home/carlos/ShortMaker/polly/pollyOutput/${title}.mp3"
video_file="/home/carlos/ShortMaker/ffmpeg/final_video.mp4"
output_file="/home/carlos/ShortMaker/ffmpeg/${title}_final.mp4"

max_attempts=20
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if [ -f "$video_file" ]; then
        echo "File found: $video_file"
        break
    else
        echo "File not found. Waiting 2 seconds and checking again..."
        sleep 2
        attempt=$((attempt + 1))
    fi
done

sleep 10

# Check if the audio file exists
if [ ! -f "$audio_file" ]; then
    echo "Audio file $audio_file does not exist!"
    exit 1
fi

# Run ffmpeg to overlay audio onto video
ffmpeg -i "$video_file" -i "$audio_file" -c:v copy -c:a aac -strict experimental "$output_file"

# Check if ffmpeg command was successful
if [ $? -eq 0 ]; then
    echo "Overlay successful. Output file saved as $output_file"
    ffplay "$output_file"
else
    echo "Error during overlay process."
fi
