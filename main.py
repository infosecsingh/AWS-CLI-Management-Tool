import os
import sys
import cleansweep.aws_resources as aws_resources
import cleansweep.spinner as spinner
import cleansweep.clean_terminal as clean

# Create a choice of options


def main_menu():   
    while True:
        clean.clean() 
        spinner.spinner(0.70)       
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
