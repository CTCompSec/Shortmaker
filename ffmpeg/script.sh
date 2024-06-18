#!/bin/bash

sleep 5

rm -rf /home/carlos/ShortMaker/ffmpeg/temp

rm -f /home/carlos/ShortMaker/ffmpeg/final_video.mp4

log_message "Temp video and final video cleared out"

# Set input, log, and temp file paths
input_file="/home/carlos/ShortMaker/ffmpeg/pexelsTemp.txt"
log_file="/home/carlos/ShortMaker/ffmpeg/log.txt"
temp_dir="/home/carlos/ShortMaker/ffmpeg/temp"

# Create temp directory if it doesn't exist
mkdir -p "$temp_dir"

# Function to log messages with timestamps
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$log_file"
}

# Read variables from input file
title=$(sed -n '1p' "$input_file")
totalSeconds=$(sed -n '2p' "$input_file")
totalVideos=$(sed -n '3p' "$input_file")

log_message "Title: $title"
log_message "Total Seconds: $totalSeconds"
log_message "Total Videos: $totalVideos"

# Paths
video_dir="/home/carlos/ShortMaker/pexels/assets/${title}"
audio_file="/home/carlos/ShortMaker/polly/pollyOutput/${title}.mp3"
output_video="/home/carlos/ShortMaker/ffmpeg/FINAL_${title}.mp4"

# Process each video
temp_files=()
counter=1
for video in "$video_dir"/*; do
    temp_video="${temp_dir}/temp_video_${counter}.mp4"
    temp_files+=("$temp_video")

    # Get original video dimensions
    width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$video")
    height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$video")

    # Calculate scaled dimensions
    if (( width < 640 || height < 360 )); then
        scale="scale='if(gt(iw\,640)\,iw\,640)':if(gt(ih\,360)\,ih\,360)"
    else
        scale="scale=640:360"
    fi

    # Scale, center/crop, and apply fade
    ffmpeg -y -i "$video" -vf "$scale,crop=640:360,setsar=1,fade=in:0:30,fade=out:114:30" \
        -t 4.5 -an -c:v libx264 -crf 23 -preset veryfast "$temp_video" < /dev/null

    log_message "Processed video: $video"
    counter=$((counter + 1))
done

node /home/carlos/ShortMaker/ffmpeg/concat.js
