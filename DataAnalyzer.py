import pandas as pd
import json


txt_path = 'preferences.txt'

def get_excel_file_details(file_path):
    try:
        df = pd.read_excel(file_path)
        
        if not df.empty:
            # Extract details
            num_rows, num_columns = df.shape
            num_na_values = df.isna().sum().sum()

            # Get column names
            column_names = df.columns.tolist()

            details = {
                'NumRows': num_rows,
                'NumColumns': num_columns,
                'NumNAValues': num_na_values,
                'ColumnNames': column_names
            }

            return details, 'File details retrieved successfully.'
        else:
            return None, 'The Excel file is empty or not in the expected format.'

    except FileNotFoundError:
        return None, 'File not found. Please check the file path.'
    
def readtxt():
    result = []  # Initialize an empty list to store the lines

    try:
        with open('preferences.txt', 'r') as file:
            # Read each line in the file and add it to the list
            for line in file:
                result.append(line.strip())
    except FileNotFoundError:
        print("Error: File 'preferences.txt' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return result


def writeTotxt(inputFromUser):
    try:
        data = str(inputFromUser)

        with open('preferences.txt', 'a') as file:
            file.write(data + '\n')  # Adding a newline character for better formatting

        print("Data written to 'preferences.txt' successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def clearTxtFile():
    try:
        with open('preferences.txt', 'w') as file:
            # This will open the file in write mode and truncate its content, effectively clearing it
            pass  # The 'pass' statement does nothing; it's a placeholder to satisfy the syntax

        print("File 'preferences.txt' has been cleared.")
    except Exception as e:
        print(f"An error occurred: {e}")