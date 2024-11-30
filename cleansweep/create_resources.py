import boto3
import os
import io
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

        # Wait for the instances to be running
        waiter = ec2_client.get_waiter('instance_running')
        spinner.spinner(1.0)
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
                    print(f"  ssh -i {key_path} {username}@{public_ip}")
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

        # Save instance details to JSON
        save_to_json(instance_details)

        return instance_ids
    except ClientError as e:
        print(f"EC2 instance creation error: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"Unexpected error: {e}")
