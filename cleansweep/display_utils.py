import json
from tabulate import tabulate
import os
def display_table(data):
    """
    Displays the resource data in a tabular format.
    """
    if not data:
        print("\nNo resources found.")
    else:
        print(tabulate(data, headers="keys", tablefmt="pretty"))


def save_to_json(data, filename="data.json"):
    """
    Saves the resource data to a JSON file at a user-specified location.
    """
    try:
        # Ask the user for a save path
        save_path = input(f"Enter the path to save the file (default: {filename}): ").strip()

        # Use default filename if the user does not provide a path
        if not save_path:
            save_path = filename

        # Ensure the file has a .json extension
        if not save_path.endswith(".json"):
            save_path += ".json"

        # Get the directory path and validate it
        directory = os.path.dirname(save_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)  # Create directory if it doesn't exist

        # Save the JSON data
        with open(save_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\nData successfully saved to {os.path.abspath(save_path)}")
        return
    except Exception as e:
        print(f"Error saving data: {e}")