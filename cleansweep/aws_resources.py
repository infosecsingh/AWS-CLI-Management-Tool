import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from tabulate import tabulate
import certifi
from cleansweep.spinner import spinner
from cleansweep.clean_terminal import clean


#Collect and display a summary of all running AWS resources in a table format.    

def aws_collect():
    clean()
    print("\033[1;34m Collecting All Resources from Multi-AZ and Globally\033[0m")
    try:
        # Get a list of all AWS regions
        ec2_client = boto3.client('ec2', verify=certifi.where())  # Use certifi bundle for SSL
        regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
        print("\nCollecting Information......")
        spinner(3)
        table_data = []  # Store rows for the table

        for region in regions:
            # EC2 Instances
            try:
                ec2 = boto3.resource('ec2', region_name=region, verify=certifi.where())
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
        
        #EBS Volumes (Region)
        try:
                for region in regions:                   
                    ec2 = boto3.resource('ec2', region_name=region, verify=certifi.where())
                    volumes = ec2.volumes.all()
                    for volume in volumes:
                        table_data.append(['EBS', region, volume.id])
                print(f"Fetching EBS volumes..")        
        except Exception as e:
            print(f"Error fetching EBS volumes: {e}")

        # S3 Buckets (Global)
        try:
            s3 = boto3.resource('s3', verify=certifi.where())
            buckets = [bucket.name for bucket in s3.buckets.all()]
            spinner(3)
            for bucket in buckets:
                table_data.append(['S3', 'Global', bucket])
            print(f"Fetching S3 buckets..")
        except Exception as e:
            print(f"Error fetching S3 buckets: {e}")
        
        # Lambda Functions (Region based)
        try:
            for region in regions:
                lambda_client = boto3.client('lambda', region_name=region, verify=certifi.where())
                functions = lambda_client.list_functions()['Functions']             
                for function in functions:
                    table_data.append(['Lambda', region, function['FunctionName']])
            spinner(3)
            print(f"Fetching Lambda functions..")
        except Exception as e:
            print(f"Error fetching Lambda functions: {e}")
        
        # RDS Instances (Region based)
        try:
            for region in regions:
                rds_client = boto3.client('rds', region_name=region, verify=certifi.where())
                instances = rds_client.describe_db_instances()['DBInstances']
                for instance in instances:
                    table_data.append(['RDS', region, instance['DBInstanceIdentifier']])
            spinner(3)
            print(f"Fetching RDS instances..")
        except Exception as e:
            print(f"Error fetching RDS instances: {e}")
        
        # DynamoDB Tables (Region based)
        try:
            for region in regions:
                dynamodb = boto3.resource('dynamodb', region_name=region, verify=certifi.where())
                tables = dynamodb.tables.all()
                for table in tables:
                  table_data.append(['DynamoDB', region, table.name])
            spinner(3)
            print(f"Fetching DynamoDB tables..")    
        except Exception as e:
            print(f"Error fetching DynamoDB tables: {e}")

        # Elastic Beanstalk Environments (Region based)
        try:
            for region in regions:
                eb_client = boto3.client('elasticbeanstalk', region_name=region, verify=certifi.where())
                tables = eb_client.describe_environments()['Environments']
                for table in tables:
                    table_data.append(['Elastic Beanstalk', region, table['EnvironmentName']])
            spinner(3)
            print(f"Fetching Elastic Beanstalk environments..")
        except Exception as e:
            print(f"Error fetching Elastic Beanstalk environments: {e}")

        #ELB Load Balancers (Region Based)
        try:
            for region in regions:
                elb_client = boto3.client('elb', region_name=region, verify=certifi.where())
                load_balancers = elb_client.describe_load_balancers()['LoadBalancerDescriptions']
                for load_balancer in load_balancers:
                    table_data.append(['ELB', region, load_balancer['LoadBalancerName']])
            spinner(3)
            print(f"Fetching ELB load balancers..")
        except Exception as e:
            print(f"Error fetching ELB load balancers: {e}")
        
        # IAM Roles (Global)
        try:
            iam = boto3.resource('iam', verify=certifi.where())
            roles = list(iam.roles.all())
            spinner(3)
            for role in roles:
                table_data.append(['IAM Role', 'Global', role.name])
            print(f"Fetching IAM roles..")  

        except Exception as e:
            print(f"Error fetching IAM roles: {e}")
    

        # API Gateway APIs (Region based)
        try:
            for region in regions:
                apigateway = boto3.client('apigateway', region_name=region, verify=certifi.where())
                apis = apigateway.get_rest_apis()['items']
                for api in apis:
                    table_data.append(['API Gateway', region, api['name']])
            spinner(3)
            print(f"Fetching API Gateway APIs..")
        except Exception as e:
            print(f"Error fetching API Gateway APIs: {e}")
        
        # ECS Clusters (Region based)
        try:
            for region in regions:
                ecs = boto3.client('ecs', region_name=region, verify=certifi.where())
                clusters = ecs.list_clusters()['clusterArns']
                for cluster in clusters:
                    table_data.append(['ECS Cluster', region, cluster])
            spinner(3)
            print(f"Fetching ECS clusters..")
        except Exception as e:
            print(f"Error fetching ECS clusters: {e}")

        # EKS Clusters (Region Based)
        try:
            for region in regions:
                eks = boto3.client('eks', region_name=region, verify=certifi.where())
                clusters = eks.list_clusters()['clusters']
                for cluster in clusters:
                    table_data.append(['EKS Cluster', region, cluster])
            spinner(3)
            print(f"Fetching EKS clusters..")
        except Exception as e:
            print(f"Error fetching EKS clusters: {e}")

        # Redshift Clusters (Region Based)
        try:
            for region in regions:
                redshift = boto3.client('redshift', region_name=region, verify=certifi.where())
                clusters = redshift.describe_clusters()['Clusters']
                for cluster in clusters:
                    table_data.append(['Redshift Cluster', region, cluster['ClusterIdentifier']])
            spinner(3)
            print(f"Fetching Redshift clusters..")
        except Exception as e:
            print(f"Error fetching Redshift clusters: {e}")
        
        # EMR Clusters (Region Based)
        try:
            for region in regions:
                emr = boto3.client('emr', region_name=region, verify=certifi.where())
                clusters = emr.list_clusters()['Clusters']
                for cluster in clusters:
                    table_data.append(['EMR Cluster', region, cluster['Id']])
            spinner(3)
            print(f"Fetching EMR clusters..") 
        except Exception as e:
            print(f"Error fetching EMR clusters: {e}")
        
        # SES Identities (Global)
        try:
            ses = boto3.client('ses', verify=certifi.where())
            identities = ses.list_identities()['Identities']
            for identity in identities:
                table_data.append(['SES Identity', 'Global', identity])
            spinner(3)
            print(f"Fetching SES identities..") 
        except Exception as e:
            print(f"Error fetching SES identities: {e}")
        
        # CloudWatch Alarms (Region Based)
        try:
            for region in regions:
                cloudwatch = boto3.client('cloudwatch', region_name=region, verify=certifi.where())
                alarms = cloudwatch.describe_alarms()['MetricAlarms']
                for alarm in alarms:
                    table_data.append(['CloudWatch Alarm', region, alarm['AlarmName']])
            spinner(3)    
            print(f"Fetching CloudWatch alarms..")
        except Exception as e:
            print(f"Error fetching CloudWatch alarms: {e}")

        # Display the collected resources in a table
        if table_data:
            clean()
            print("\033[1;34mSummary of Running Resources:\033[0m")
            print(tabulate(table_data, headers=['Service', 'Region', 'Resource ID'], tablefmt='pretty'))
        else:
            print("\nNo running resources found.")

    except NoCredentialsError:
        print("AWS credentials not found. Please configure them.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials. Please check your configuration.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def aws_delete():
    print("null")
def aws_monitor():
    print("null")
def aws_create():
    print("null")