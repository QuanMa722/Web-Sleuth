# -*- coding: utf-8 -*-

import json
import os

# Root directory where your folders (2015, 2016, ..., 2025) are located
root_directory = '../data'  # Replace this with the actual path

# Function to check each file in the directory
def check_json_files():
    issue_count = 0  # Counter for files with issues

    # Iterate through each year folder (2015, 2016, ..., 2025)
    for year in range(2015, 2026):
        year_folder = os.path.join(root_directory, str(year))

        # Skip the year folder if it doesn't exist
        if not os.path.isdir(year_folder):
            continue

        # Check each month folder under the year folder
        for month in os.listdir(year_folder):
            month_folder = os.path.join(year_folder, month)

            # Skip if it's not a directory
            if not os.path.isdir(month_folder):
                continue

            # Iterate through each day folder in the month folder
            for day_folder in os.listdir(month_folder):

                day_folder_path = os.path.join(month_folder, day_folder)

                # Check if the path is a valid file (i.e., not a directory)
                if os.path.isdir(day_folder_path):
                    continue

                # Try to open and load the JSON file
                try:
                    with open(day_folder_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                        # Check each item in the loaded data
                        for item in data:
                            # Check for 'title' length and empty 'content'
                            if len(item.get('title', '')) <= 3 or not item.get('content'):
                                print(f'File has issues: {day_folder}')
                                issue_count += 1
                                break  # Skip further checking for this file

                except json.JSONDecodeError:
                    print(f'Error decoding JSON in file: {day_folder_path}')

    # Print total number of files with issues
    print(f'Total files with issues: {issue_count}')

# Call the function to check JSON files
check_json_files()
