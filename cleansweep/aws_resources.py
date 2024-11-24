import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import sys
from tabulate import tabulate
import itertools
import time
import sys
import os


def spinner(duration):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])
    end_time = time.time() + duration  # Run for the specified duration
    while time.time() < end_time:
        sys.stdout.write(f"\r{next(spinner_cycle)}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 20 + "\r")  # Clear the line

def clean():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def aws_collect():
    """
    Collect and display a summary of all running AWS resources in a table format.
    """
    try:
        # Get a list of all AWS regions
        ec2_client = boto3.client('ec2')
        regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
        print("\nCollecting AWS resources..")
        spinner(3)
        table_data = []  # Store rows for the table

        for region in regions:
            # EC2 Instances
            try:
                ec2 = boto3.resource('ec2', region_name=region)
                running_instances = [
                    {'InstanceId': instance.id, 'State': instance.state['Name']}
                    for instance in ec2.instances.all()
                    if instance.state['Name'] == 'running'
                ]
                print(f"Fetching EC2 instances in {region}..")
                for instance in running_instances:
                    table_data.append(['EC2', region, instance['InstanceId']])
                    
            except Exception as e:
                print(f"Error fetching EC2 instances in {region}: {e}")

        # S3 Buckets (Global)
        try:
            s3 = boto3.resource('s3')
            buckets = [bucket.name for bucket in s3.buckets.all()]
            spinner(3)
            for bucket in buckets:
                table_data.append(['S3', 'Global', bucket])
            print(f"Fetching S3 buckets..")
        except Exception as e:
            print(f"Error fetching S3 buckets: {e}")

        # Display the collected resources in a table
        if table_data:
            clean()
            print("\nSummary of Running Resources:")
            print(tabulate(table_data, headers=['Service', 'Region', 'Resource ID'], tablefmt='pretty'))
        else:
            print("\nNo running resources found.")

    except NoCredentialsError:
        print("AWS credentials not found. Please configure them.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials. Please check your configuration.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def aws_monitor():
    print("deleting resource")

def aws_create():
    print("deleting resource")