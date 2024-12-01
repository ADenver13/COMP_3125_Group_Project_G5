import csv
from datetime import datetime
import os
import zipfile
import shutil

# This program parses the file format provided by https://dixielandsoftware.net/Amtrak/status/StatusPages/index.html.
# First, download the year in the lower left corner, then unzip the parent folder. Provide the file path to the program and it will parse it.

headers = [
    "Station Code",
    "Schedule Arrival Day",
    "Schedule Arrival Time (24-hour)",
    "Schedule Departure Day",
    "Schedule Departure Time (24-hour)",
    "Actual Arrival Time (24-hour)",
    "Actual Departure Time (24-hour)",
    "Comments"
]

# Function to convert weird 12-hour format to 24-hour format
# EX: 840A -> 08:40, EX: 920P -> 21:20. Also includes date from .txt title
def convert_time(time_str, input_file_date):
    if not time_str or time_str == "*":  # Handle empty or placeholder times
        return ""
    try:
        time_str = time_str.upper()
        hour = int(time_str[:-3])  # Extract the hour part
        minute = int(time_str[-3:-1])  # Extract the minute part
        if time_str.endswith("P") and hour != 12:  # Convert PM to 24-hour
            hour += 12
        elif time_str.endswith("A") and hour == 12:  # Handle 12 AM case
            hour = 0
        return datetime.strptime(f"{input_file_date} {hour:02}:{minute:02}", "%Y%m%d %H:%M")
    except ValueError:
        return ""

# Parse a line into structured data
def parse_line(line, is_last_line, input_file_date):
    parts = line.split()
    station_code = parts[0]
    sched_arrival_day = parts[1] if len(parts) > 1 else ""
    sched_arrival_time = convert_time(parts[2], input_file_date) if len(parts) > 2 else ""
    sched_departure_day = parts[3] if len(parts) > 3 else ""
    sched_departure_time = convert_time(parts[4], input_file_date) if len(parts) > 4 else ""
    actual_arrival_time = convert_time(parts[5], input_file_date) if len(parts) > 5 else ""
    actual_departure_time = convert_time(parts[6], input_file_date) if len(parts) > 6 else ""

    # Calculate delays in minutes
    comments = ""
    if sched_departure_time and actual_departure_time:
        comments = (sched_departure_time - actual_departure_time).total_seconds() / 60
    elif sched_arrival_time and actual_arrival_time:
        comments = (sched_arrival_time - actual_arrival_time).total_seconds() / 60

    return [
        station_code,
        sched_arrival_day,
        sched_arrival_time,
        sched_departure_day,
        sched_departure_time,
        actual_arrival_time,
        actual_departure_time,
        comments,
    ]

# Function to process a single text file
def process_text_file(input_file, output_file):
    input_file_date = input_file[-12:-4]  # Extract date from filename
    try:
        with open(input_file, "r") as infile, open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

            lines = infile.readlines()
            total_lines = len(lines)

            for i, line in enumerate(lines, start=1):
                if i <= 10:  # Skip the first 10 lines - header
                    continue
                line = line.strip()
                if line.startswith("*"):
                    line = line[1:].strip()
                is_last_line = i == total_lines
                writer.writerow(parse_line(line, is_last_line, input_file_date))

        print(f"Processed: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Failed to process file {input_file}: {e}")
        return False
    return True

# Function to process a folder of files
def process_folder(input_folder, output_folder):
    failed_files = []  # List to store failed file paths
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".zip"):
                zip_path = os.path.join(root, file)
                # Most are zipped, manually unzipping would be a pain
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    # Create a new folder to extract files temporarily
                    temp_extract_folder = os.path.join(root, f"temp_extracted_{os.path.splitext(file)[0]}")
                    os.makedirs(temp_extract_folder, exist_ok=True)
                    
                    # Extract files into the new temporary folder
                    zip_ref.extractall(temp_extract_folder)

                    # Process all the extracted files
                    for sub_root, _, sub_files in os.walk(temp_extract_folder):
                        for sub_file in sub_files:
                            if sub_file.endswith(".txt"):
                                txt_file_path = os.path.join(sub_root, sub_file)
                                relative_path = os.path.relpath(sub_root, input_folder)
                                output_sub_folder = os.path.join(output_folder, relative_path)
                                os.makedirs(output_sub_folder, exist_ok=True)
                                output_file = os.path.join(output_sub_folder, sub_file.replace(".txt", ".csv"))

                                if not process_text_file(txt_file_path, output_file):
                                    failed_files.append(txt_file_path)

                    # Delete the temporary folder after processing
                    shutil.rmtree(temp_extract_folder)

    # Print failed files at the end
    if failed_files:
        print("\nThe following files failed to process:")
        for failed_file in failed_files:
            print(failed_file)
    else:
        print("All files processed successfully.")

input_folder = "2023/2023"
output_folder = "2023_TEST/2023"

process_folder(input_folder, output_folder)
