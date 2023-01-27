import subprocess
import os

# Get the YouTube link from the user
youtube_link = input("Enter the YouTube link: ")

# Set the output folder
output_folder = 'Input'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Download the audio in mp3 format using youtube-dl
subprocess.run(['youtube-dl', '--extract-audio', '--audio-format', 'mp3', '-o', os.path.join(output_folder, '%(title)s.%(ext)s'), '--no-check-certificate', '--ignore-errors', youtube_link])
