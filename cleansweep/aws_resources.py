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
        
        # Lambda Functions (Global)
        try:
            lambda_client = boto3.client('lambda', verify=certifi.where())
            functions = lambda_client.list_functions()['Functions']
            spinner(3)
            for function in functions:
                table_data.append(['Lambda', 'Global', function['FunctionName']])
            print(f"Fetching Lambda functions..")
        except Exception as e:
            print(f"Error fetching Lambda functions: {e}")
        
        # RDS Instances (Global)
        try:
            rds_client = boto3.client('rds', verify=certifi.where())
            instances = rds_client.describe_db_instances()['DBInstances']
            spinner(3)
            for instance in instances:
                table_data.append(['RDS', 'Global', instance['DBInstanceIdentifier']])
            print(f"Fetching RDS instances..")
        except Exception as e:
            print(f"Error fetching RDS instances: {e}")
        
        # DynamoDB Tables (Global)
        try:
            dynamodb = boto3.resource('dynamodb', verify=certifi.where())
            tables = dynamodb.tables.all()
            spinner(3)
            for table in tables:
                table_data.append(['DynamoDB', 'Global', table.name])
            print(f"Fetching DynamoDB tables..")    
        except Exception as e:
            print(f"Error fetching DynamoDB tables: {e}")

        # Elastic Beanstalk Environments (Global)
        try:
            eb_client = boto3.client('elasticbeanstalk', verify=certifi.where())
            environments = eb_client.describe_environments()['Environments']
            spinner(3)
            for environment in environments:
                table_data.append(['Elastic Beanstalk', 'Global', environment['EnvironmentName']])
            print(f"Fetching Elastic Beanstalk environments..")

        except Exception as e:
            print(f"Error fetching Elastic Beanstalk environments: {e}")

        #ELB Load Balancers (Global)
        try:
            elb_client = boto3.client('elb', verify=certifi.where())
            load_balancers = elb_client.describe_load_balancers()['LoadBalancerDescriptions']
            spinner(3)
            for load_balancer in load_balancers:
                table_data.append(['ELB', 'Global', load_balancer['LoadBalancerName']])
            print(f"Fetching ELB load balancers..")

        except Exception as e:
            print(f"Error fetching ELB load balancers: {e}")
        
        # VPCs (Global)
        try:
            ec2 = boto3.resource('ec2', verify=certifi.where())
            vpcs = list(ec2.vpcs.all())
            spinner(3)
            for vpc in vpcs:
                table_data.append(['VPC', 'Global', vpc.id])
            print(f"Fetching VPCs..")
        except Exception as e:
            print(f"Error fetching VPCs: {e}")

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
    

        # API Gateway APIs (Global)
        try:
            apigateway = boto3.client('apigateway', verify=certifi.where())
            apis = apigateway.get_rest_apis()['items']
            spinner(3)
            for api in apis:
                table_data.append(['API Gateway', 'Global', api['name']])
            print(f"Fetching API Gateway APIs..")

        except Exception as e:
            print(f"Error fetching API Gateway APIs: {e}")
        
        # ECS Clusters (Global)
        try:
            ecs = boto3.client('ecs', verify=certifi.where())
            clusters = ecs.list_clusters()['clusterArns']
            spinner(3)
            for cluster in clusters:
                table_data.append(['ECS Cluster', 'Global', cluster])
            print(f"Fetching ECS clusters..")   
        except Exception as e:
            print(f"Error fetching ECS clusters: {e}")

        # EKS Clusters (Global)
        try:
            eks = boto3.client('eks', verify=certifi.where())
            clusters = eks.list_clusters()['clusters']
            spinner(3)
            for cluster in clusters:
                table_data.append(['EKS Cluster', 'Global', cluster])
            print(f"Fetching EKS clusters..")
        except Exception as e:
            print(f"Error fetching EKS clusters: {e}")
        
        # Redshift Clusters (Global)
        try:
            redshift = boto3.client('redshift', verify=certifi.where())
            clusters = redshift.describe_clusters()['Clusters']
            spinner(3)
            for cluster in clusters:
                table_data.append(['Redshift Cluster', 'Global', cluster['ClusterIdentifier']])
            print(f"Fetching Redshift clusters..")  
        except Exception as e:
            print(f"Error fetching Redshift clusters: {e}")
        
        # EMR Clusters (Global)
        try:
            emr = boto3.client('emr', verify=certifi.where())
            clusters = emr.list_clusters()['Clusters']
            spinner(3)
            for cluster in clusters:
                table_data.append(['EMR Cluster', 'Global', cluster['Id']])
            print(f"Fetching EMR clusters..")   
        except Exception as e:
            print(f"Error fetching EMR clusters: {e}")
        
        # SES Identities (Global)
        try:
            ses = boto3.client('ses', verify=certifi.where())
            identities = ses.list_identities()['Identities']
            spinner(3)
            for identity in identities:
                table_data.append(['SES Identity', 'Global', identity])
            print(f"Fetching SES identities..") 
        except Exception as e:
            print(f"Error fetching SES identities: {e}")
        
        # CloudWatch Alarms (Global)
        try:
            cloudwatch = boto3.client('cloudwatch', verify=certifi.where())
            alarms = cloudwatch.describe_alarms()['MetricAlarms']
            spinner(3)
            for alarm in alarms:
                table_data.append(['CloudWatch Alarm', 'Global', alarm['AlarmName']])
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