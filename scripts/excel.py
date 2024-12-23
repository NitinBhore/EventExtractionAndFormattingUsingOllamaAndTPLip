import pandas as pd
import json

# Function to extract events from the Excel file
def extract_events_from_excel(excel_file):
    # Read the Excel file using openpyxl engine for .xlsx files
    df = pd.read_excel(excel_file, engine='openpyxl')

    # Print the column names to check what is available
    # print("Columns in the Excel file:", df.columns.tolist())

    # Initialize the events list
    events = []

    # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():
        # Loop through each day of the week
        for day in ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            if pd.notna(row[day]):  # Check if there is a value for the day
                start_time = row[day] if isinstance(row[day], str) else row[day].strftime("%I:%M %p").strip()  # Convert time to string
                end_time = ""  # Leave end time blank by default
                
                # Check if there's a range in the time
                if ' - ' in start_time:
                    start_time, end_time = start_time.split(' - ')
                else:
                    end_time = ""  # Keep it blank if not available

                # Use .get to avoid KeyError and check if the column exists
                event = [
                    "",  # Start date (leave blank)
                    day,  # Day of the week
                    [
                        [
                            "",  # Repeat count (leave blank)
                            start_time,  # Start time
                            end_time,  # End time
                            row.get('Room Request', ""),  # Event type
                            row.get('Setup Style', ""),  # Setup style
                            row.get('Number of Pax', ""),  # Number of people
                            ""  # Additional comments (leave blank)
                        ]
                    ]
                ]
                events.append(event)

    return {"events": events}

# Function to write the output to a JSON file
def write_json_to_file(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

# Main function to run the extraction and save to JSON
def excel_data_extraction(excel_file):
    # print(f"Data extraction started")
    events = extract_events_from_excel(excel_file)
    output_filename = "output/extracted_events.json"  # Specify your desired output filename
    write_json_to_file(events, output_filename)
    print(f"\n\nData written to {output_filename}")

# Usage
# excel_file = 'RFP2.xlsx'  # Replace with your Excel file path
# excel_data_extraction(excel_file)
