import boto3
import os
import re
import certifi
from botocore.exceptions import ClientError
import cleansweep.clean_terminal as clean
import cleansweep.spinner as spinner
from cleansweep.display_utils import save_to_json

# Common username mappings for popular AMIs
AMI_USERNAMES = {
    "amazon-linux": "ec2-user",
    "ubuntu": "ubuntu",
    "redhat": "ec2-user",
    "centos": "centos",
    "debian": "admin",
    "suse": "ec2-user",
}

def suggest_username(ami_id):
    """Suggests an SSH username based on the AMI type."""
    ami_lower = ami_id.lower()
    for key, username in AMI_USERNAMES.items():
        if key in ami_lower:
            return username
    return "ec2-user"  # Default username if no match

def key_pair(ec2_client):
    """
    Check for existing key pairs or create a new one. Ensures the PEM file has correct permissions.
    """
    try:
        # List existing key pairs
        key_pairs = ec2_client.describe_key_pairs()
        existing_keys = [kp['KeyName'] for kp in key_pairs['KeyPairs']]

        if existing_keys:
            print("\nExisting Key Pairs:")
            for idx, key in enumerate(existing_keys, 1):
                print(f"{idx}. {key}")
            choice = input("\nDo you want to use an existing key pair? (y/n): ").lower()
            if choice == 'y':
                key_choice = int(input("Select the key pair by number: "))
                if 1 <= key_choice <= len(existing_keys):
                    selected_key = existing_keys[key_choice - 1]
                    print(f"Using existing key pair: {selected_key}")
                    return selected_key, None
                else:
                    print("Invalid selection.")
                    return None, None

        # Generate a new key pair
        key_name = input("Enter the new key pair name: ")
        print("Creating a new key pair...")
        key_pair = ec2_client.create_key_pair(KeyName=key_name)
        private_key = key_pair['KeyMaterial']

        # Save the PEM file securely
        save_path = input("Enter the path to save the key file (e.g., /path/to/file.pem): ")
        pem_path = f"{save_path}.pem" if not save_path.endswith(".pem") else save_path
        with open(pem_path, 'w') as pem_file:
            pem_file.write(private_key)
        os.chmod(pem_path, 0o400)  # Secure the file with proper permissions

        print(f"Key pair saved securely at {pem_path}")
        return key_name, pem_path

    except ClientError as e:
        print(f"Error fetching or creating key pairs: {e.response['Error']['Message']}")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None

'''
----------------------------------------------------------------------------------------------------------------------
'''
def create_ec2_instance():
    """
    Launches an EC2 instance interactively, sets up security groups, key pairs, 
    and provides connection details. Saves instance details to a JSON file.
    """
    clean.clean()
    spinner.spinner(0.5)
    print("\n")
    print("\033[1;35mLaunching EC2 instance...\033[0m")
    print("\033[1;35m--------------------------\033[0m")    
    # User inputs for instance creation
    region = input("Enter the AWS region (e.g., ap-south-1): ")
    ec2_client = boto3.client('ec2', region_name=region)

    key_name, key_path = key_pair(ec2_client)
    if not key_name:
        print("Key pair setup failed. Exiting...")
        return

    instance_name = input("Enter the name for the instance(s) (e.g., MyEc2Instance): ")
    ami_id = input("Enter the AMI ID (e.g., ami-0614680123427b75e): ")
    instance_type = input("Enter the instance type (e.g., t2.micro): ")
    count = int(input("Enter the number of instances to launch: "))
    ebs_volume_size = int(input("Enter the EBS volume size in GB (e.g., 8): "))

    # Security group selection
    try:
        print("\nFetching available security groups...")
        security_groups = ec2_client.describe_security_groups()['SecurityGroups']
        if not security_groups:
            print("No security groups found. Please create one in the AWS Management Console.")
            return
        print("\nAvailable Security Groups:")
        for i, sg in enumerate(security_groups):
            print(f"{i + 1}. {sg['GroupName']} ({sg['GroupId']})")
        sg_index = int(input("Select a security group by number: ")) - 1
        if sg_index < 0 or sg_index >= len(security_groups):
            print("Invalid security group selection. Exiting...")
            return
        security_group_id = security_groups[sg_index]['GroupId']
    except Exception as e:
        print(f"Error fetching security groups: {e}")
        return

    try:
        # Launch the instance
        response = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=[security_group_id],
            MinCount=1,
            MaxCount=count,
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/xvda',
                    'Ebs': {
                        'VolumeSize': ebs_volume_size,
                        'DeleteOnTermination': True,
                        'VolumeType': 'gp2'
                    }
                }
            ],
        )
        instance_ids = [instance['InstanceId'] for instance in response['Instances']]

        # Tag the instance(s) with unique names
        for i, instance_id in enumerate(instance_ids):
            instance_tag = f"{instance_name}-{i + 1}"  # Incremental tag names
            ec2_client.create_tags(
                Resources=[instance_id],
                Tags=[{'Key': 'Name', 'Value': instance_tag}]
            )
            print(f"Instance {instance_id} tagged as {instance_tag}")

        print(f"Launching EC2 instance(s): {', '.join(instance_ids)}")
        spinner.spinner(2)
        # Wait for the instances to be running
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=instance_ids)

        # Gather instance details for saving
        instance_details = []
        for instance_id in instance_ids:
            instance_info = ec2_client.describe_instances(InstanceIds=[instance_id])
            instance = instance_info['Reservations'][0]['Instances'][0]
            public_ip = instance.get('PublicIpAddress', "N/A")
            username = suggest_username(ami_id)
            tag_name = f"{instance_name}-{instance_ids.index(instance_id) + 1}"
            clean.clean()
            spinner.spinner(0.5)
            print("\033[1;29mEc2 Instance Created\033[0m")
            print(f"\033[1;35mInstance ID:\033[0m {instance_id}")
            print(f"\033[1;35mTag Name:\033[0m {tag_name}")
            print(f"\033[1;35mPublic IP Address:\033[0m {public_ip}")
            print(f"\033[1;35mSuggested Username:\033[0m {username}")
            if key_path:
                print(f"Use the private key at {key_path} to connect:")
                if public_ip != "N/A":
                    print("\n","\033[1;31mNOTE:\033[0m","\033[1;38m If you are getting a bad permission error while connecting,then please use --\033[0m","\033[1;32mGIT BASH Tool\033[0m")
                    print("\n",f"  ssh -i {key_path} {username}@{public_ip}")
                else:
                    print(f"  Instance does not have a public IP. Use a bastion host or private network to connect.")

            # Append details for JSON
            instance_details.append({
                "InstanceId": instance_id,
                "TagName": tag_name,
                "PublicIpAddress": public_ip,
                "Username": username,
                "KeyPath": key_path
            })
        save_option = input("\nDo you want to save instance details to a JSON file? (y/n): ").lower()
        if save_option == 'y':
            save_to_json(instance_details)
            return save_to_json
        return instance_ids
    except ClientError as e:
        print(f"EC2 instance creation error: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"Unexpected error: {e}")



'''
-----------------------------------------------------------------------------------------------------------
'''
def is_valid_bucket_name(bucket_name):
    """
    Validates the S3 bucket name.
    S3 bucket names must not contain underscores ('_').
    """
    if '_' in bucket_name:
        print("Bucket name contains invalid characters: _")
        return False
    return True

def is_valid_bucket_name(bucket_name):
    """
    Validates the S3 bucket name.
    Bucket name must be between 3 and 63 characters long and match specific regex.
    """
    # Regex pattern to validate bucket name
    bucket_name_pattern = r'^[a-z0-9.-]{3,63}$'

    # Check for invalid characters like underscores, parentheses, etc.
    if re.match(bucket_name_pattern, bucket_name):
        return True
    else:
        print(f"Invalid bucket name '{bucket_name}'. Bucket name must only contain lowercase letters, numbers, hyphens, and periods.")
        return False

def create_s3_bucket():
    """
    Creates an S3 bucket with options for region, versioning, logging, and Block Public Access.
    Ensures the bucket name is valid and unique globally.
    """
    print("\n\033[1;35mCreating an S3 Bucket...\033[0m")
    print("\033[1;35m-------------------------\033[0m")

    # Prompt user for a globally unique bucket name
    while True:
        bucket_name = input("Enter a globally unique name for the bucket: ").strip()
        if not bucket_name:
            print("Bucket name cannot be empty. Please provide a valid name.")
        elif not is_valid_bucket_name(bucket_name):
            continue  # Re-prompt if the name is invalid
        else:
            break  # Exit the loop if the bucket name is valid

    # Prompt for region, default to 'us-east-1' if empty
    region = input("Enter the AWS region for the bucket (leave empty for default 'us-east-1'): ").strip() or 'us-east-1'

    # Prompt to enable versioning
    enable_versioning = input("Enable versioning for the bucket? (y/n): ").strip().lower() == 'y'

    try:
        # Create the S3 client
        s3_client = boto3.client('s3', region_name=region, verify=certifi.where())

        # Handle bucket creation with location constraint only for regions other than 'us-east-1'
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

        print(f"\033[1;32mBucket '{bucket_name}' created successfully in region {region}.\033[0m")

        # Enable versioning if selected
        if enable_versioning:
            print("Enabling versioning for the bucket...")
            s3_client.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={'Status': 'Enabled'}
            )
            print("\033[1;32mVersioning enabled successfully.\033[0m")

        # Print bucket details
        print("\033[1;34mBucket Details:\033[0m")
        print(f"  Name: {bucket_name}")
        print(f"  Region: {region}")
        print(f"  Versioning: {'Enabled' if enable_versioning else 'Disabled'}")

        # Ask if they want to upload objects to the bucket
        upload_objects = input("Do you want to upload objects to this bucket? (y/n): ").strip().lower() == 'y'

        # Initialize data collection for uploaded files
        uploaded_files_data = []

        if upload_objects:
            # Ask for file(s) to upload
            files_input = input("Enter the local file path(s) to upload, separated by commas: ")

            # Process the input, stripping extra quotes and whitespace
            files = [file.strip().strip('"') for file in files_input.split(',')]

            for file in files:
                if file:  # Ensure the file path is not empty
                    try:
                        # Upload file to S3
                        print(f"Uploading {file} to bucket {bucket_name}...")
                        s3_client.upload_file(file, bucket_name, os.path.basename(file))
                        print(f"\033[1;32mFile '{file}' uploaded successfully.\033[0m")

                        # Collect details for JSON
                        uploaded_files_data.append({
                            "BucketName": bucket_name,
                            "FileName": os.path.basename(file),
                            "ARN": f"arn:aws:s3:::{bucket_name}/{os.path.basename(file)}"
                        })
                    except FileNotFoundError:
                        print(f"\033[1;31mFile '{file}' not found.\033[0m")
                    except ClientError as e:
                        print(f"\033[1;31mError uploading file '{file}': {e.response['Error']['Message']}\033[0m")
                    except Exception as e:
                        print(f"\033[1;31mUnexpected error uploading file '{file}': {e}\033[0m")

        # Ask to save details only if there are uploaded files
        if uploaded_files_data:
            save_option = input("\nDo you want to save details of uploaded files to a JSON file? (y/n): ").strip().lower()
            if save_option == 'y':
                try:
                    save_to_json(data=uploaded_files_data, filename="uploaded_files_details.json")
                    print("\033[1;32mDetails saved successfully to 'uploaded_files_details.json'.\033[0m")
                except Exception as e:
                    print(f"\033[1;31mError saving details to JSON: {e}\033[0m")

    except ClientError as e:
        print(f"\033[1;31mError creating bucket: {e.response['Error']['Message']}\033[0m")
    except Exception as e:
        print(f"\033[1;31mUnexpected error: {str(e)}\033[0m")



'''
----------------------------------------------------------------------------------------------------------------------
'''

# LAMBDA FUNCTION - Create Lambda

def create_lambda():
    
    clean.clean()
     # Prompt for Lambda function name
    function_name = input("Enter the name for the Lambda function: ")
    # Prompt for runtime
    runtime = input("Enter the runtime for the Lambda function (e.g., 'python3.8'): ")
    # Prompt for handler
    handler = input("Enter the handler for the Lambda function (e.g., 'lambda_function.lambda_handler'): ")
    # Prompt for IAM role ARN
    role_arn = input("Enter the IAM role ARN for the Lambda function: ")
    # Prompt for ZIP file path
    zip_file_path = input("Enter the path to the ZIP file containing the Lambda function code: ")
    # Prompt for environment variables
    env_vars = {}

    while True:
        key = input("Enter environment variable key (or press Enter to finish): ")
        if not key:
            break
        value = input(f"Enter value for {key}: ")
        env_vars[key] = value
        print(f"Environment variable {key} added.")
    
    # Create Lambda function
    lambda_client = boto3.client('lambda', verify=certifi.where())
    try:
        with open(zip_file_path, 'rb') as zip_file:
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime=runtime,
                Role=role_arn,
                Handler=handler,
                Code={'ZipFile': zip_file.read()},
                Environment={'Variables': env_vars}
            )
        print(f"Lambda function '{function_name}' created successfully.")
        print(f"ARN: {response['FunctionArn']}")
        print(f"Last Modified: {response['LastModified']}")
        print(f"Description: {response['Description']}")

    
    # Ask to save details
        save_option = input("\nDo you want to save details to a JSON file? (y/n): ").strip().lower()
        if save_option == 'y':
            try:
                save_to_json(data=response, filename="lambda_details.json")
                print("\033[1;32mDetails saved successfully to 'lambda_details.json'.\033[0m")
            except Exception as e:
                print(f"\033[1;31mError saving details to JSON: {e}\033[0m")    
    
    except ClientError as e:
        print(f"Error creating Lambda function: {e.response['Error']['Message']}")
