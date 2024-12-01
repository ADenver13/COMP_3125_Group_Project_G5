import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime
from meteostat import Daily, Point, Hourly

#This script consolidates the output from parse_txt_files into a single .csv file, grabbing weather data from meteostat

def process_csv(input_file):
    # File paths
    master_table_output_file = 'master_table_output.csv'
    amtrak_station_csv = 'List_of_Amtrak_stations_combined.csv'

    geolocator = Nominatim(user_agent="geoapiWeatherDSGroupProj") #Need unqiue project identifier or else don't work

    # Read the input files
    input_df = pd.read_csv(input_file)
    amtrak_station_df = pd.read_csv(amtrak_station_csv)

    # Determine the first index with a valid station code, sometimes they're a little messed up
    first_index = None
    for index, row in input_df.iterrows():
        if len(str(row['Station Code'])) >= 3:
            first_index = index
            break

    if first_index is None:
        raise ValueError("No valid 'Station Code' found in the input file.")

    middle_index = int(((len(input_df) - first_index) / 2) + first_index)

    # Extract route number and station weather information. We want to get weather for the middle station
    route_number = input_file.split("_")[-2]
    route_number = route_number.split('\\')[-1]
    station_weather = input_df.iloc[middle_index]['Station Code']
    weather_date = pd.to_datetime(input_df.iloc[middle_index]['Schedule Departure Time (24-hour)'])

    print(input_file)
    print(route_number)

    # Lookup city and state weather info
    result = amtrak_station_df[amtrak_station_df['Station code'] == station_weather]
    if not result.empty:
        city_weather = result.iloc[0]['Location']
        state_weather = result.iloc[0]['State or province']
    else:
        city_weather = 'Unknown'
        state_weather = 'Unknown'

    location = geolocator.geocode(f"{city_weather}, {state_weather}")

    # Define the date
    start = datetime(weather_date.year, weather_date.month, weather_date.day, 0)
    end = datetime(weather_date.year, weather_date.month, weather_date.day, 23)

    if location:
        point = Point(location.latitude, location.longitude)

        data = Hourly(point, start=start, end=end)
        data = data.fetch()

        # Check if weather data is available
        if not data.empty:
            weather_category = data.loc[data['coco'].first_valid_index(), 'coco']
        else:
            weather_category = 'Unknown'

    # Lookup arrival station information
    arrival_station_code = input_df.iloc[-1]['Station Code']
    arrival_result = amtrak_station_df[amtrak_station_df['Station code'] == arrival_station_code]

    if not arrival_result.empty:
        arrival_station = arrival_result.iloc[0]['Station code']
        arrival_city = arrival_result.iloc[0]['Location']
        arrival_state = arrival_result.iloc[0]['State or province']
        date_opened_arrival = arrival_result.iloc[0]['Opened']
    else:
        arrival_station = 'Unknown'
        arrival_city = 'Unknown'
        arrival_state = 'Unknown'
        date_opened_arrival = 'Unknown'

    # Calculate total trip time
    try:
        total_trip_time = (
            pd.to_datetime(input_df.iloc[-1]['Actual Arrival Time (24-hour)']) -
            pd.to_datetime(input_df.iloc[first_index]['Schedule Departure Time (24-hour)'])
        ).total_seconds() / 3600  # Convert to hours
    except Exception:
        total_trip_time = 'Invalid Time'

    # Calculate total delay
    try:
        total_delay = int(input_df.iloc[-1].get('Comments', 0))
    except ValueError:
        total_delay = 0

    # Create the row to append
    row_to_append = [
        weather_date,
        route_number,
        arrival_station,
        arrival_city,
        arrival_state,
        date_opened_arrival,
        total_trip_time,
        total_delay,
        weather_category,
        city_weather,
        state_weather
    ]

    # Append the row to the output CSV file
    row_df = pd.DataFrame([row_to_append], columns=[
        'Date', 'Route Number', 'Arrival Station', 'Arrival City', 'Arrival State', 
        'Date Opened (Arrival)', 'Total Trip Time (hrs)', 'Total Delay (min)', 
        'Weather Category', 'City Weather', 'State Weather'
    ])

    try:
        master_table_df = pd.read_csv(master_table_output_file)
        master_table_df = pd.concat([master_table_df, row_df], ignore_index=True)
    except FileNotFoundError:
        # If the file doesn't exist, create it
        master_table_df = row_df

    # Save the updated DataFrame
    master_table_df.to_csv(master_table_output_file, index=False)

    print(f"Row successfully appended to {master_table_output_file}.")

import os

def process_all_csvs(base_directory):
    # List to keep track of files that could not be processed
    failed_files = []

    # Walk through the directory structure
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                try:
                    # Call the process_csv function for each CSV file
                    process_csv(file_path)
                except Exception as e:
                    # Add the file to the failed files list and print an error
                    print(f"Could not process: {file_path}. Error: {e}")
                    failed_files.append(file_path)

    # Output the failed files at the end
    if failed_files:
        print("\nThe following files could not be processed:")
        for failed_file in failed_files:
            print(failed_file)
    else:
        print("\nAll files were processed successfully.")

base_directory = "C:\\Users\\histo\\3125_group_project\\COMP_3125_Group_Project_G5\\2023_TEST"
process_all_csvs(base_directory)
