import pandas as pd
from tabula import read_pdf
import re
import json


def pdf_data_extraction(pdf_file_path):
    # Function to write JSON data to a file
    def write_json_to_file(data, filename):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    # Read tables from the PDF file
    tables = read_pdf(pdf_file_path, pages='all', multiple_tables=True)

    # Check if there are at least 3 tables
    if len(tables) >= 3:
        # Concatenate table 2 and table 3 (index 1 and 2 in Python)
        concatenated_table = pd.concat([tables[1], tables[2]], ignore_index=True)

        # Rename columns
        concatenated_table.rename(columns={
            'Unnamed: 0': 'Activity',
            'Unnamed: 1': 'No of People',
            'Unnamed: 2': 'Square Footage'
        }, inplace=True)

        # Remove variations of '/ 24 hour' from the 'Junk Supply Company' column
        concatenated_table['Junk Supply Company'] = concatenated_table['Junk Supply Company'].str.replace(
            r'/?\s*24\s*(hour|hr)', '', regex=True
        )

        # Create a new column 'Day' based on day names found in 'Junk Supply Company' column
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Initialize the new 'Day' column with empty strings
        concatenated_table['Day'] = ''

        # Iterate over the rows and check if any day is present in the 'Junk Supply Company' column
        for i in range(len(concatenated_table) - 1):
            if any(day in str(concatenated_table.loc[i, 'Junk Supply Company']) for day in days):
                # Assign the found day to the next row in the 'Day' column
                concatenated_table.loc[i + 1, 'Day'] = concatenated_table.loc[i, 'Junk Supply Company']

        # Drop the first 3 rows (indices 0, 1, 2)
        concatenated_table = concatenated_table.drop([0, 1, 2], axis=0).reset_index(drop=True)

        # Drop the 'Unnamed: 3' column if it exists
        if 'Unnamed: 3' in concatenated_table.columns:
            concatenated_table = concatenated_table.drop('Unnamed: 3', axis=1)

        # Drop rows where all elements are blank
        concatenated_table = concatenated_table.dropna(how='all')

        # Filter out rows that contain any day in the 'Junk Supply Company' column
        concatenated_table = concatenated_table[~concatenated_table['Junk Supply Company'].str.contains('|'.join(days), case=False, na=False)]

        # Split the 'Junk Supply Company' column into 'Start Time' and 'End Time' if a hyphen is present
        concatenated_table[['Start Time', 'End Time']] = concatenated_table['Junk Supply Company'].str.split('-', expand=True)

        # If 'End Time' is NaN (no hyphen), it means the value should be in 'Start Time'
        concatenated_table['Start Time'].fillna(concatenated_table['Junk Supply Company'], inplace=True)

        # Drop the original 'Junk Supply Company' column
        concatenated_table = concatenated_table.drop('Junk Supply Company', axis=1)

        # Replace NaN values with empty strings
        concatenated_table.fillna('', inplace=True)

        # Create a JSON structure for the events
        events = []
        for _, row in concatenated_table.iterrows():
            start_date = ''  # You may want to set a specific date or logic to derive it
            day_of_week = row['Day']
            repeat_count = ''  # Default value
            start_time = row['Start Time']
            end_time = row['End Time']
            event_type = row['Activity']
            setup_style = ''  # Default value
            number_of_people = row['No of People']
            additional_comments = ''  # Default value

            event = [
                start_date,
                day_of_week,
                [
                    [repeat_count, start_time, end_time, event_type, setup_style, number_of_people, additional_comments]
                ]
            ]
            events.append(event)

        # Create the final JSON structure
        final_output = {"events": events}

        # Specify the output filename
        output_filename = "output/extracted_events.json"
        
        # Write JSON data to a file
        write_json_to_file(final_output, output_filename)
        print(f"\n\nData written to {output_filename}")
    else:
        print("Not enough tables found in the PDF.")

# Define the PDF file path
# pdf_file_path = "RFP1.pdf"
# pdf_data_extraction(pdf_file_path)