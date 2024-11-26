import json
from tabulate import tabulate

def display_table(data):
    """
    Displays the resource data in a tabular format.
    """
    if not data:
        print("\nNo resources found.")
    else:
        print(tabulate(data, headers="keys", tablefmt="pretty"))

def save_to_json(data, filename):
    """
    Saves the resource data to a JSON file.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\nData successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")
