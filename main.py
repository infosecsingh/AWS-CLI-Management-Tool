import os
import sys
import itertools
import time
import cleansweep.aws_resources as aws_resources


# Clean terminal Function for different OS based 
def clean_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

#Spinner for Animation 
def spinner(duration):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])
    end_time = time.time() + duration  # Run for the specified duration
    while time.time() < end_time:
        sys.stdout.write(f"\rLoading {next(spinner_cycle)}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 20 + "\r")  # Clear the line

# Create a choice of options
def main_menu():   
    while True:
        clean_terminal() 
        spinner(0.10)       
        print("\n AWS Management tool")
        print("[1] List and delete resources")
        print("[2] Monitor Resources")
        print("[3] Create Resources")
        print("[4] Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            aws_resources.aws_delete()
        elif choice == "2":
            aws_resources.aws_monitor()
        elif choice == "3":
            aws_resources.aws_create()
        elif choice == "4":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")
        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main_menu()
