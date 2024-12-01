import sys
import cleansweep.aws_resources as aws_resources
import cleansweep.spinner as spinner
import cleansweep.clean_terminal as clean
import cleansweep.display_utils as display_utils
import cleansweep.create_resources as create_resources

# Create a choice of options

sys.stdout.reconfigure(encoding='utf-8')

def aws_create():
    while True:
        clean.clean()
        print("\n")
        spinner.spinner(0.50)
        print("\033[1;35m----------------Create AWS Resources------------------\033[0m")
        print("[01] │ Create EC2 Instances")
        print("[02] │ Create S3 Buckets")
        print("[03] │ Create Lambda Functions")
        print("\n")
        choice = input("Choose an option (1-3) or go to [M]ain Menu: ")

        if choice == '1':
            create_resources.create_ec2_instance()
        elif choice == '2':
            create_resources.create_s3_bucket()
        elif choice == '3':
            create_resources.create_lambda()
        elif choice in ['M','m']:
            main_menu()
            break
        else:
            print("Invalid choice. Please try again.")
def aws_delete():
    while True:
        clean.clean()
        print("\n")
        spinner.spinner(0.50)
        print("\033[1;31m----------------Delete AWS Resources------------------\033[0m")
        print("[01] │ Delete EC2 Instances")
        print("[02] │ Delete EBS Volumes")
        print("[03] │ Delete Lambda Functions")        
        print("[04] │ Delete RDS Instance")
        print("[05] │ Delete DynamoDB Tables")
        print("[06] │ Delete Elastic Beanstalk")
        print("[07] │ Delete ELastic LoadBalancer")        
        print("[08] │ Delete API Gateways")
        print("[09] │ Delete ECS Clusters")
        print("[10] │ Delete EKS Clusters")
        print("[11] │ Delete Redshift Clusters")
        print("[12] │ Delete EMR Clusters")
        print("[13] │ Delete CloudWatch Alarms")
        print("[14] │ Delete S3 Buckets")
        print("[15] │ Delete SES Identities")
        print("\n")
        choice = input("Choose an option (1-15) or go to [M]ain Menu: ")
        
        if choice == '1':
            ec2_data = aws_resources.fetch_ec2_instances()
            display_utils.display_table(ec2_data)
            if not ec2_data:
                return
            instance_ids = input("Enter EC2 instance IDs to delete (comma-separated): ").split(',')
            region = input("Enter the AWS region of these instances: ")
            aws_resources.delete_ec2_instances(instance_ids, region) 
        elif choice == '2':
            ebs_data = aws_resources.fetch_ebs_volumes()
            display_utils.display_table(ebs_data)
            if not ebs_data:
                return
            volume_ids = input("Enter EBS volume IDs to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these volumes: ")
            aws_resources.delete_ebs_volumes(volume_ids, region)
        elif choice == '3':
            lambda_data = aws_resources.fetch_lambda_functions()
            display_utils.display_table(lambda_data)
            if not lambda_data:
                return
            function_names = input("Enter Lambda function names to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these functions: ")
            aws_resources.delete_lambda_functions(function_names, region)
        elif choice == '4':
            rds_data = aws_resources.fetch_rds_instances()
            display_utils.display_table(rds_data)
            if not rds_data:
                return
            instance_ids = input("Enter RDS instance IDs to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these instances: ")
            aws_resources.delete_rds_instances(instance_ids, region)    
        elif choice == '5':
            dynamodb_data = aws_resources.fetch_dynamodb_tables()
            display_utils.display_table(dynamodb_data)
            if not dynamodb_data:
                return
            table_names = input("Enter DynamoDB table names to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these tables: ")
            aws_resources.delete_dynamodb_tables(table_names, region)
        elif choice == '6':
            elasticbeanstalk_data = aws_resources.fetch_elastic_beanstalk_environments()
            display_utils.display_table(elasticbeanstalk_data)
            if not elasticbeanstalk_data:
                return
            environment_names = input("Enter Elastic Beanstalk environment names to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these environments: ")
            aws_resources.delete_elastic_beanstalk_environments(environment_names, region)  
        elif choice == '7':
            elb_data = aws_resources.fetch_elastic_load_balancers()
            display_utils.display_table(elb_data)
            if not elb_data:
                return
            load_balancer_names = input("Enter Elastic Load Balancer names to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these load balancers: ")
            aws_resources.delete_elastic_load_balancers(load_balancer_names, region)    
        elif choice == '8':
            apigateway_data = aws_resources.fetch_api_gateways()
            display_utils.display_table(apigateway_data)
            if not apigateway_data:
                return
            api_names = input("Enter API Gateway names to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these APIs: ")
            aws_resources.delete_api_gateways(api_names, region)    
        elif choice == '9':
            ecs_data = aws_resources.fetch_ecs_clusters()
            display_utils.display_table(ecs_data)
            if not ecs_data:
                return
            cluster_names = input("Enter ECS cluster names to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these clusters: ")
            aws_resources.delete_ecs_clusters(cluster_names, region)    
        elif choice == '10':
            eks_data = aws_resources.fetch_eks_clusters()
            display_utils.display_table(eks_data)
            if not eks_data:
                return
            cluster_names = input("Enter EKS cluster names to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these clusters: ")
            aws_resources.delete_eks_clusters(cluster_names, region)    
        elif choice == '11':
            redshift_data = aws_resources.fetch_redshift_clusters()
            display_utils.display_table(redshift_data)
            if not redshift_data:
                return
            cluster_ids = input("Enter Redshift cluster IDs to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these clusters: ")
            aws_resources.delete_redshift_clusters(cluster_ids, region)
        elif choice == '12':
            emr_data = aws_resources.fetch_emr_clusters()
            display_utils.display_table(emr_data)
            if not emr_data:
                return
            cluster_ids = input("Enter EMR cluster IDs to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these clusters: ")
            aws_resources.delete_emr_clusters(cluster_ids, region)  
        elif choice == '13':
            cloudwatch_data = aws_resources.fetch_cloudwatch_alarms()
            display_utils.display_table(cloudwatch_data)
            if not cloudwatch_data:
                return
            alarm_names = input("Enter CloudWatch alarm names to delete (comma-separated): ").split(', ')
            region = input("Enter the AWS region of these alarms: ")
            aws_resources.delete_cloudwatch_alarms(alarm_names, region) 
        elif choice == '14':
            s3_data = aws_resources.fetch_s3_buckets()
            display_utils.display_table(s3_data)
            if not s3_data:
                return
            bucket_names_input = input("Enter S3 bucket names to delete (comma-separated): ").split(',')
            bucket_names_input = [name.strip() for name in bucket_names_input]  # Strip extra spaces
            aws_resources.delete_s3_buckets(bucket_names_input)
        elif choice == '15':
            ses_data = aws_resources.fetch_ses_identities()
            display_utils.display_table(ses_data)
            if not ses_data:
                return
            identity_names = input("Enter SES identity names to delete (comma-separated): ").split(', ')
            aws_resources.delete_ses_identities(identity_names)  
        elif choice == '16':
            aws_resources.delete_api_gateways()
               
        elif choice in ["M","m"]:
            main_menu()
        else:
            print("Invalid choice. Please try again.")
        input("\nPress Enter to return to the menu...")



def aws_fetch():
    while True:
        clean.clean()
        print("\n")
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
            if not ec2_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(ec2_data, "ec2_instances.json")
                print("\nData saved to ec2_instances.json")
        elif choice == '2':
            ebs_data = aws_resources.fetch_ebs_volumes()
            display_utils.display_table(ebs_data)
            if not ebs_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(ebs_data, "ebs_volumes.json")
                print("\nData saved to ebs_volumes.json")
        elif choice == '3':
            lambda_data = aws_resources.fetch_lambda_functions()
            display_utils.display_table(lambda_data)
            if not lambda_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(lambda_data, "lambda_functions.json")
                print("\nData saved to lambda_functions.json")
        elif choice == '4':
            rds_data = aws_resources.fetch_rds_instances()
            display_utils.display_table(rds_data)
            if not rds_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(rds_data, "rds_instances.json")
                print("\nData saved to rds_instances.json")
        elif choice == '5':
            dynamodb_data = aws_resources.fetch_dynamodb_tables()
            display_utils.display_table(dynamodb_data)
            if not dynamodb_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(dynamodb_data, "dynamodb_tables.json")
                print("\nData saved to dynamodb_tables.json")
        elif choice == '6':
            elasticbeanstalk_data = aws_resources.fetch_elastic_beanstalk_environments()
            display_utils.display_table(elasticbeanstalk_data)
            if not elasticbeanstalk_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(elasticbeanstalk_data, "elastic_beanstalk_environments.json")
                print("\nData saved to elastic_beanstalk_environments.json")    
        elif choice == '7':
            elb_data = aws_resources.fetch_elastic_load_balancers()
            display_utils.display_table(elb_data)
            if not elb_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(elb_data, "elastic_load_balancers.json")
                print("\nData saved to elastic_load_balancers.json")    
        elif choice == '8':
            apigateway_data = aws_resources.fetch_api_gateways()
            display_utils.display_table(apigateway_data)
            if not apigateway_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(apigateway_data, "api_gateways.json")
                print("\nData saved to api_gateways.json")  
        elif choice == '9':
            ecs_data = aws_resources.fetch_ecs_clusters()
            display_utils.display_table(ecs_data)
            if not ecs_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(ecs_data, "ecs_clusters.json")
                print("\nData saved to ecs_clusters.json")  
        elif choice == '10':
            eks_data = aws_resources.fetch_eks_clusters()
            display_utils.display_table(eks_data)
            if not eks_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(eks_data, "eks_clusters.json")
                print("\nData saved to eks_clusters.json")  
        elif choice == '11':
            redshift_data = aws_resources.fetch_redshift_clusters()
            display_utils.display_table(redshift_data)
            if not redshift_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(redshift_data, "redshift_clusters.json")
                print("\nData saved to redshift_clusters.json") 
        elif choice == '12':
            emr_data = aws_resources.fetch_emr_clusters()
            display_utils.display_table(emr_data)
            if not emr_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(emr_data, "emr_clusters.json")
                print("\nData saved to emr_clusters.json")  
        elif choice == '13':
            cloudwatch_data = aws_resources.fetch_cloudwatch_alarms()
            display_utils.display_table(cloudwatch_data)
            if not cloudwatch_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(cloudwatch_data, "cloudwatch_alarms.json")
                print("\nData saved to cloudwatch_alarms.json") 
        elif choice == '14':
            s3_data = aws_resources.fetch_s3_buckets()
            display_utils.display_table(s3_data)
            if not s3_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(s3_data, "s3_buckets.json")
                print("\nData saved to s3_buckets.json")    
        elif choice == '15':
            iam_data = aws_resources.fetch_iam_roles()
            display_utils.display_table(iam_data)
            if not iam_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(iam_data, "iam_roles.json")
                print("\nData saved to iam_roles.json") 
        elif choice == '16':
            ses_data = aws_resources.fetch_ses_identities()
            display_utils.display_table(ses_data)
            if not ses_data:
                return
            save_option = input("\nSave to JSON? (y/n): ")
            if save_option.lower() == 'y':
                display_utils.save_to_json(ses_data, "ses_identities.json")
                print("\nData saved to ses_identities.json")    
        elif choice == '17':
            all_data = aws_resources.all_services()
            display_utils.display_table(all_data)
            if not all_data:
                return
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
        print("│                           \033[1;36mAWS CLI MANAGEMENT TOOL\033[0m                                           │")
        print("│                          developed by: infosecsingh                                         │")
        print("├────────┬────────────────────────────────────────────────────────────────────────────────────┤")
        print("│ \033[1;34mOption\033[0m │                          \033[1;34mDescription\033[0m                                               │")
        print("├────────┼────────────────────────────────────────────────────────────────────────────────────┤")
        print("│   1    │ Check Running Resources                   │ Get All Services from Regions & Globaly│")
        print("├────────┼────────────────────────────────────────────────────────────────────────────────────┤")
        print("│   2    │ Delete Resources                          │ Delete running services                │")
        print("├────────┼────────────────────────────────────────────────────────────────────────────────────┤")
        print("│   3    │ Create Resources                          │ Create Services like Ec2, S3, etc.     │")
        print("├────────┼────────────────────────────────────────────────────────────────────────────────────┤")
        print("│   4    │ Monitor Resources                         │ Monitor Resources with CloudWatch API  │")
        print("└────────┴────────────────────────────────────────────────────────────────────────────────────┘")
        choice = input("Choose an option (1-4) or e[X]it: ")
        if choice == "1":
            aws_fetch()
        elif choice == "2":
            aws_delete()
        elif choice == "3":
            aws_create()
        elif choice == "4":
            print("Work in progress... this feature is not available at this moment.")
        elif choice in ["x", "X"]:
            clean.clean()
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")
        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main_menu()
