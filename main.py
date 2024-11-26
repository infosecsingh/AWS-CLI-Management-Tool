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
        print("┌─────────────────────────────────────────────────────────────────────────────────────────────┐")
        print("│                           \033[1mAWS Clean Sweep CLI Tool\033[0m                                          │")
        print("│                          developed by: infosecsingh                                         │")
        print("├────────┬────────────────────────────────────────────────────────────────────────────────────┤")
        print("│ \033[1;34mOption\033[0m │                          \033[1;34mDescription\033[0m                                               │")
        print("├────────┼────────────────────────────────────────────────────────────────────────────────────┤")
        print("│   1    │ Check All Resources                       │ Get All Running Services from Multi-AZ │")
        print("├────────┼────────────────────────────────────────────────────────────────────────────────────┤")
        print("│   2    │ Delete Resources                          │ Delete/stop running services           │")
        print("├────────┼────────────────────────────────────────────────────────────────────────────────────┤")
        print("│   3    │ Create Resources                          │ Create Services like Ec2, S3, etc.     │")
        print("├────────┼────────────────────────────────────────────────────────────────────────────────────┤")
        print("│   4    │ Monitor Resources                         │ Monitor Resources with CloudWatch API  │")
        print("└────────┴────────────────────────────────────────────────────────────────────────────────────┘")
        choice = input("Choose an option (1-5) or e[X]it: ")
        if choice == "1":
            aws_resources.aws_collect()
        elif choice == "2":
            aws_resources.aws_delete()
        elif choice == "3":
            aws_resources.aws_monitor()
        elif choice == "4":
            aws_resources.aws_create()
        elif choice == "X":
            clean.clean()
            print("Exiting...")
            sys.exit(0)
        elif choice == "x":
            clean.clean()
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")
        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main_menu()
