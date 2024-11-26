import sys
import cleansweep.aws_resources as aws_resources
import cleansweep.spinner as spinner
import cleansweep.clean_terminal as clean
import cleansweep.display_utils as display_utils

# Create a choice of options

def aws_fetch():
    while True:
        clean.clean()
        spinner.spinner(0.50)
        print("\033[1;34m----------------Check AWS Resources------------------\033[0m")
        print("[01] │ EC2 Instances         - Fetch From All Regions")
        print("[02] │ EBS Volumes           - Fetch From All Regions")
        print("[03] │ Lambda Functions      - Fetch From All Regions")        
        print("[04] │ RDS                   - Fetch From All Regions")
        print("[05] │ DynamoDB              - Fetch From All Regions")
        print("[06] │ Elastic Beanstalk     - Fetch From All Regions")
        print("[07] │ ELastic LoadBalancer  - Fetch From All Regions")        
        print("[08] │ API Gateways          - Fetch From All Regions")
        print("[09] │ ECS Clusters          - Fetch From All Regions")
        print("[10] │ EKS Clusters          - Fetch From All Regions")
        print("[11] │ Redshift Clusters     - Fetch From All Regions")
        print("[12] │ EMR Clusters          - Fetch From All Regions")
        print("[13] │ CloudWatch Alarms     - Fetch From All Regions")
        print("[14] │ S3 Buckets            - Fetch From Globally")
        print("[15] │ IAM Roles             - Fetch From Globally")
        print("[16] │ SES Identities        - Fetch From Globally")
        print("[17] │ Check ALL Running Services at once")
        print("\n")
        choice = input("Choose an option(1-17) or go to [M]ain Menu: ")
        if choice == '1':
            ec2_data = aws_resources.fetch_ec2_instances()
            display_utils.display_table(ec2_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(ec2_data, "ec2_instances.json")
                print("\nData saved to ec2_instances.json")
        elif choice == '2':
            ebs_data = aws_resources.fetch_ebs_volumes()
            display_utils.display_table(ebs_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(ebs_data, "ebs_volumes.json")
                print("\nData saved to ebs_volumes.json")
        elif choice == '3':
            lambda_data = aws_resources.fetch_lambda_functions()
            display_utils.display_table(lambda_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(lambda_data, "lambda_functions.json")
                print("\nData saved to lambda_functions.json")
        elif choice == '4':
            rds_data = aws_resources.fetch_rds_instances()
            display_utils.display_table(rds_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(rds_data, "rds_instances.json")
                print("\nData saved to rds_instances.json")
        elif choice == '5':
            dynamodb_data = aws_resources.fetch_dynamodb_tables()
            display_utils.display_table(dynamodb_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(dynamodb_data, "dynamodb_tables.json")
                print("\nData saved to dynamodb_tables.json")
        elif choice == '6':
            elasticbeanstalk_data = aws_resources.fetch_elastic_beanstalk_environments()
            display_utils.display_table(elasticbeanstalk_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(elasticbeanstalk_data, "elastic_beanstalk_environments.json")
                print("\nData saved to elastic_beanstalk_environments.json")    
        elif choice == '7':
            elb_data = aws_resources.fetch_elastic_load_balancers()
            display_utils.display_table(elb_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(elb_data, "elastic_load_balancers.json")
                print("\nData saved to elastic_load_balancers.json")    
        elif choice == '8':
            apigateway_data = aws_resources.fetch_api_gateways()
            display_utils.display_table(apigateway_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(apigateway_data, "api_gateways.json")
                print("\nData saved to api_gateways.json")  
        elif choice == '9':
            ecs_data = aws_resources.fetch_ecs_clusters()
            display_utils.display_table(ecs_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(ecs_data, "ecs_clusters.json")
                print("\nData saved to ecs_clusters.json")  
        elif choice == '10':
            eks_data = aws_resources.fetch_eks_clusters()
            display_utils.display_table(eks_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(eks_data, "eks_clusters.json")
                print("\nData saved to eks_clusters.json")  
        elif choice == '11':
            redshift_data = aws_resources.fetch_redshift_clusters()
            display_utils.display_table(redshift_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(redshift_data, "redshift_clusters.json")
                print("\nData saved to redshift_clusters.json") 
        elif choice == '12':
            emr_data = aws_resources.fetch_emr_clusters()
            display_utils.display_table(emr_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(emr_data, "emr_clusters.json")
                print("\nData saved to emr_clusters.json")  
        elif choice == '13':
            cloudwatch_data = aws_resources.fetch_cloudwatch_alarms()
            display_utils.display_table(cloudwatch_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(cloudwatch_data, "cloudwatch_alarms.json")
                print("\nData saved to cloudwatch_alarms.json") 
        elif choice == '14':
            s3_data = aws_resources.fetch_s3_buckets()
            display_utils.display_table(s3_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(s3_data, "s3_buckets.json")
                print("\nData saved to s3_buckets.json")    
        elif choice == '15':
            iam_data = aws_resources.fetch_iam_roles()
            display_utils.display_table(iam_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(iam_data, "iam_roles.json")
                print("\nData saved to iam_roles.json") 
        elif choice == '16':
            ses_data = aws_resources.fetch_ses_identities()
            display_utils.display_table(ses_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(ses_data, "ses_identities.json")
                print("\nData saved to ses_identities.json")    
        elif choice == '17':
            all_data = aws_resources.all_services()
            display_utils.display_table(all_data)
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(all_data, "all_services.json")
                print("\nData saved to all_services.json")  
        elif choice in ["M","m"]:
            main_menu()
        else:
            print("Invalid choice. Please try again.")
        input("\nPress Enter to return to the menu...")


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
        print("│   1    │ Check Running Resources                   │ Get All Services from Regions & Globaly│")
        print("├────────┼────────────────────────────────────────────────────────────────────────────────────┤")
        print("│   2    │ Delete Resources                          │ Delete/stop running services           │")
        print("├────────┼────────────────────────────────────────────────────────────────────────────────────┤")
        print("│   3    │ Create Resources                          │ Create Services like Ec2, S3, etc.     │")
        print("├────────┼────────────────────────────────────────────────────────────────────────────────────┤")
        print("│   4    │ Monitor Resources                         │ Monitor Resources with CloudWatch API  │")
        print("└────────┴────────────────────────────────────────────────────────────────────────────────────┘")
        choice = input("Choose an option (1-5) or e[X]it: ")
        if choice == "1":
            aws_fetch()
        elif choice == "2":
            print(0)
        elif choice == "3":
            print(0)
        elif choice == "4":
            print(0)
        elif choice in ["x", "X"]:
            clean.clean()
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")
        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main_menu()
