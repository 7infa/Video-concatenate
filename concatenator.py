from pydub import AudioSegment
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timedelta
from tqdm import tqdm
import subprocess
import os

# Set input and output file paths
input_folder = 'Input'
output_folder = 'Output'
output_file = 'concatenated_output.mp3'
timestamps_file = 'timestamps.txt'

# Create an empty list to store audio segments
audio_segments = []

# Keep track of the total length of the concatenated audio
total_length = timedelta()

# Open the timestamps file for writing
with open(os.path.join(output_folder, timestamps_file), 'w') as f:
    # Iterate through all the mp3 files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.mp3'):
            # Load the audio file
            audio_file = os.path.join(input_folder, file_name)
            audio = AudioSegment.from_file(audio_file, format='mp3')

            # Calculate the start time of the current audio segment
            start_time = total_length
            start_time_str = datetime.utcfromtimestamp(start_time.total_seconds()).strftime("%H:%M:%S")

            # Write the start timestamp to the file
            f.write(f'{file_name} start: {start_time_str}\n')

            # Append the audio to the list of segments
            audio_segments.append(audio)

            # Add the duration of the current audio segment to the total length
            total_length += timedelta(seconds=audio.duration_seconds)

            # Append a one-second silence
            audio_segments.append(AudioSegment.silent(duration=1000))

            # Add the duration of the silence to the total length
            total_length += timedelta(seconds=1)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Find the image file
    image_file = None
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.jpg'):
            image_file = os.path.join(input_folder, file_name)
            break
    if not image_file:
        print("Error: no jpg image found in the input folder")
        exit()
# Create the output folder if it doesn't exist
output_folder = 'Output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    
# Set the input and output file paths
input_folder = 'Input'
output_mp3_file = os.path.join(output_folder, 'concatenated_output.mp3')
output_mp4_file = os.path.join(output_folder, 'output.mp4')
timestamps_file = os.path.join(output_folder, 'timestamps.txt')

# Find the image file
image_file = None
for file_name in os.listdir(input_folder):
    if file_name.endswith('.jpg'):
        image_file = os.path.join(input_folder, file_name)
        break

if image_file is None:
    raise Exception("No image file found in the input folder")

# Run the audio concatenation and video creation
final_audio = sum(audio_segments)
final_audio.export(output_mp3_file, format='mp3')
print(f'Successfully concatenated and exported to {output_mp3_file}')

# Create the video using ffmpeg
subprocess.run(['ffmpeg', '-loop', '1', '-i', image_file, '-r', '2', '-i', output_mp3_file, '-c:v', 'libx264', '-preset', 'fast', '-crf', '28', '-c:a', 'aac', '-b:a', '192k', '-vf', 'scale=1920:1080', '-shortest', output_mp4_file])

print(f'Successfully created video {output_mp4_file}')
