import boto3
import paramiko
import io
import os
from botocore.exceptions import ClientError
import cleansweep.clean_terminal as clean
import cleansweep.spinner as spinner



def key_pair(ec2_client):
    """
    Check for existing key pairs or create a new one. Offers options for saving as .pem or .ppk.
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

        # Ask where to save the key
        save_path = input("Enter the path to save the key file (e.g., /path/to/file): ")
        save_format = input("Save as PEM or PPK? (pem/ppk): ").lower()

        if save_format == 'pem':
            pem_path = f"{save_path}.pem"
            with open(pem_path, 'w') as pem_file:
                pem_file.write(private_key)
            os.chmod(pem_path, 0o400)  # Secure the file
            print(f"Key pair saved as .pem at {pem_path}")
            return key_name, pem_path

        elif save_format == 'ppk':
            ppk_path = f"{save_path}.ppk"
            rsa_key = paramiko.RSAKey(file_obj=io.StringIO(private_key))
            rsa_key.write_private_key_file(ppk_path)
            print(f"Key pair saved as .ppk at {ppk_path}")
            return key_name, ppk_path

        else:
            print("Invalid format choice. Key pair creation aborted.")
            return None, None

    except ClientError as e:
        print(f"Error fetching or creating key pairs: {e.response['Error']['Message']}")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None
    

        

# Example usage
def create_ec2_instance():
    clean.clean()
    spinner.spinner(0.5)
    """Launch EC2 instances with user-provided or newly generated key pair."""
    region = input("Enter the AWS region (e.g, ap-south-1): ")
    ec2_client = boto3.client('ec2', region_name=region)

    # Get or create key pair
    key_name, key_path = key_pair(ec2_client)
    if not key_name:
        print("Key pair setup failed. Exiting...")
        return
    instance_name = input("Enter the name for the instances (eg. MyEc2Instance): ")
    ami_id = input("Enter the AMI ID (e.g, ami-0614680123427b75e): ")
    instance_type = input("Enter the instance type (e.g, t2.micro): ")
    count = int(input("Enter the number of instances to launch: "))
    
    # user_data = input("Enter user-data script (leave empty for none): ")

     # Security Group Selection
    print("\nFetching available security groups...")
    try:
        security_groups = ec2_client.describe_security_groups()['SecurityGroups']
        if not security_groups:
            print("No security groups found. Please create one in the AWS Management Console.")
            return
        print("\nAvailable Security Groups:")
        for i, sg in enumerate(security_groups):
            print(f"{i + 1}. {sg['GroupName']} ({sg['GroupId']})")
        sg_index = int(input("Select a security group by number: ")) - 1
        security_group_id = security_groups[sg_index]['GroupId']
    except Exception as e:
        print(f"Error fetching security groups: {e}")
        return

    try:
        response = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=[security_group_id],
            MinCount=1,
            MaxCount=count,
        )
        instance_ids = [instance['InstanceId'] for instance in response['Instances']]
                # Add a tag with the Name key
        ec2_client.create_tags(
            Resources=instance_ids,
            Tags=[{'Key': 'Name', 'Value': instance_name}]
        )
        # Wait for the instances to be running and get their public IP
        waiter = ec2_client.get_waiter('instance_running')
        spinner.spinner(1.0) # Wait for the instances to be running
        waiter.wait(InstanceIds=instance_ids)
        instance_id = response['Instances'][0]['InstanceId']
        public_ip = response['Instances'][0]['PublicIpAddress']
        print(f"Successfully launched EC2 instance: {instance_id}")
        print(f"Public IP Address: {public_ip}")
        if key_path:
            print(f"Use the private key at {key_path} to connect.")
    except ClientError as e:
        print(f"EC2 instance: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"Unexpected error: {e}")


