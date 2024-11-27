import boto3
import certifi
import os
import cleansweep.spinner as spinner
from botocore.exceptions import ClientError
import cleansweep.clean_terminal as clean


def get_all_regions():
    """
    Fetches all AWS regions using the EC2 client.
    """
    ec2_client = boto3.client('ec2', verify=certifi.where())
    return [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

def fetch_ec2_instances():
    """
    Fetches all running EC2 instances across all regions.
    Returns a list of dictionaries with instance details.
    """
    clean.clean()
    regions = get_all_regions()
    ec2_data = []
    spinner.spinner(0.50)
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region, verify=certifi.where())
        print(f"Fetching EC2 instances in {region}....")
        running_instances = [
            {"ResourceType": "EC2", "Region": region, "ResourceId": instance.id, "State": instance.state['Name']}
            for instance in ec2.instances.all()
            if instance.state['Name'] == 'running'
        ]
        ec2_data.extend(running_instances)
    return ec2_data

def fetch_ebs_volumes():
    """
    Fetches all EBS volumes across all regions.
    Returns a list of dictionaries with volume details.
    """
    clean.clean()
    regions = get_all_regions()
    ebs_data = []
    spinner.spinner(0.50)
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region, verify=certifi.where())
        print(f"Fetching EBS volumes in {region}....")
        volumes = [
            {"ResourceType": "EBS", "Region": region, "ResourceId": volume.id, "State": volume.state}
            for volume in ec2.volumes.all()
        ]
        ebs_data.extend(volumes)
    return ebs_data

def fetch_lambda_functions():
    clean.clean()
    regions = get_all_regions()
    lambda_data = []
    for region in regions:
        ec2 = boto3.client('lambda', region_name=region, verify=certifi.where())
        print(f"Fetching Lambda functions in {region}....")
        functions = [
            {"ResourceType": "Lambda", "Region": region, "ResourceId": function['FunctionName'], "State": "N/A"}
            for function in ec2.list_functions()['Functions']
        ]
        lambda_data.extend(functions)
    return lambda_data

def fetch_rds_instances():
    clean.clean()
    regions = get_all_regions()
    rds_data = []
    for region in regions:
        ec2 = boto3.client('rds', region_name=region, verify=certifi.where())
        print(f"Fetching RDS instances in {region}....")
        instances = [
            {"ResourceType": "RDS", "Region": region, "ResourceId": instance['DBInstanceIdentifier'], "State": instance['DBInstanceStatus']}
            for instance in ec2.describe_db_instances()['DBInstances']
        ]
        rds_data.extend(instances)
    return rds_data

def fetch_dynamodb_tables():
    clean.clean()
    regions = get_all_regions()
    dynamodb_data = []
    for region in regions:
        ec2 = boto3.client('dynamodb', region_name=region, verify=certifi.where())
        print(f"Fetching DynamoDB tables in {region}....")
        tables = [
            {"ResourceType": "DynamoDB", "Region": region, "ResourceId": table['TableName'], "State": table['TableStatus']}
            for table in ec2.list_tables()['TableNames']
        ]
        dynamodb_data.extend(tables)
    return dynamodb_data

def fetch_elastic_beanstalk_environments():
    clean.clean()
    regions = get_all_regions()
    elasticbeanstalk_data = []
    for region in regions:
        ec2 = boto3.client('elasticbeanstalk', region_name=region, verify=certifi.where())
        print(f"Fetching Elastic Beanstalk environments in {region}....")
        environments = [
            {"ResourceType": "Elastic Beanstalk", "Region": region, "ResourceId": environment['EnvironmentName'], "State": environment['Status']}
            for environment in ec2.describe_environments()['Environments']
        ]
        elasticbeanstalk_data.extend(environments)
    return elasticbeanstalk_data

def fetch_elastic_load_balancers():
    clean.clean()
    regions = get_all_regions()
    elb_data = []
    for region in regions:
        ec2 = boto3.client('elb', region_name=region, verify=certifi.where())
        print(f"Fetching Elastic Load Balancers in {region}....")
        load_balancers = [
            {"ResourceType": "ELB", "Region": region, "ResourceId": load_balancer['LoadBalancerName'], "State": load_balancer['State']}
            for load_balancer in ec2.describe_load_balancers()['LoadBalancerDescriptions']
        ]
        elb_data.extend(load_balancers)
    return elb_data 

def fetch_api_gateways():
    clean.clean()
    regions = get_all_regions()
    apigateway_data = []
    for region in regions:
        ec2 = boto3.client('apigateway', region_name=region, verify=certifi.where())
        print(f"Fetching API Gateways in {region}....")
        gateways = [
            {"ResourceType": "API Gateway", "Region": region, "ResourceId": gateway['name'], "State": gateway['status']}
            for gateway in ec2.get_rest_apis()['items']
        ]
        apigateway_data.extend(gateways)
    return apigateway_data  

def fetch_ecs_clusters():
    clean.clean()
    regions = get_all_regions()
    ecs_data = []
    for region in regions:
        ec2 = boto3.client('ecs', region_name=region, verify=certifi.where())
        print(f"Fetching ECS Clusters in {region}....")
        clusters = [
            {"ResourceType": "ECS", "Region": region, "ResourceId": cluster['clusterName'], "State": cluster['status']}
            for cluster in ec2.list_clusters()['clusterArns']
        ]
        ecs_data.extend(clusters)
    return ecs_data 

def fetch_eks_clusters():
    clean.clean()
    regions = get_all_regions()
    eks_data = []
    for region in regions:
        ec2 = boto3.client('eks', region_name=region, verify=certifi.where())
        print(f"Fetching EKS Clusters in {region}....")
        clusters = [
            {"ResourceType": "EKS", "Region": region, "ResourceId": cluster['name'], "State": cluster['status']}
            for cluster in ec2.list_clusters()['clusters']
        ]
        eks_data.extend(clusters)
    return eks_data 

def fetch_redshift_clusters():
    clean.clean()
    regions = get_all_regions()
    redshift_data = []
    for region in regions:
        ec2 = boto3.client('redshift', region_name=region, verify=certifi.where())
        print(f"Fetching Redshift Clusters in {region}....")
        clusters = [
            {"ResourceType": "Redshift", "Region": region, "ResourceId": cluster['ClusterIdentifier'], "State": cluster['ClusterStatus']}
            for cluster in ec2.describe_clusters()['Clusters']
        ]
        redshift_data.extend(clusters)
    return redshift_data    

def fetch_emr_clusters():
    clean.clean()
    regions = get_all_regions()
    emr_data = []
    for region in regions:
        ec2 = boto3.client('emr', region_name=region, verify=certifi.where())
        print(f"Fetching EMR Clusters in {region}....")
        clusters = [
            {"ResourceType": "EMR", "Region": region, "ResourceId": cluster['Id'], "State": cluster['Status']['State']}
            for cluster in ec2.list_clusters()['Clusters']
        ]
        emr_data.extend(clusters)
    return emr_data 

def fetch_cloudwatch_alarms():
    clean.clean()
    regions = get_all_regions()
    cloudwatch_data = []
    for region in regions:
        ec2 = boto3.client('cloudwatch', region_name=region, verify=certifi.where())
        print(f"Fetching CloudWatch Alarms in {region}....")
        alarms = [
            {"ResourceType": "CloudWatch", "Region": region, "ResourceId": alarm['AlarmName'], "State": alarm['StateValue']}
            for alarm in ec2.describe_alarms()['MetricAlarms']
        ]
        cloudwatch_data.extend(alarms)
    return cloudwatch_data  

def fetch_s3_buckets():
    clean.clean()
    ec2 = boto3.client('s3', verify=certifi.where())
    print(f"Fetching S3 Buckets Globally....")
    spinner.spinner(0.50)
    buckets = [
            {"ResourceType": "S3", "Region": "Global", "ResourceId": bucket['Name'], "State": "N/A"}
            for bucket in ec2.list_buckets()['Buckets']  # Correct key is 'Buckets'
        ]
    return buckets  

def fetch_iam_roles():
    clean.clean()
    ec2 = boto3.client('iam', verify=certifi.where())
    print(f"Fetching IAM Roles Globally....")
    spinner.spinner(0.50)
    roles = [
        {"ResourceType": "IAM", "Region": "Global", "ResourceId": role['RoleName'], "State": "N/A"}
        for role in ec2.list_roles()['Roles']
    ]
    return roles    

def fetch_ses_identities():
    clean.clean()
    ec2 = boto3.client('ses', region_name='us-east-1', verify=certifi.where())
    print(f"Fetching SES Identities Globally....")
    spinner.spinner(0.50)
    identities = [
        {"ResourceType": "SES", "Region": "Global", "ResourceId": identity['IdentityName'], "State": "N/A"}
        for identity in ec2.list_identities()['Identities']
    ]
    return identities   

def all_services():
    clean.clean()
    spinner.spinner(0.50)
    ec2_data = fetch_ec2_instances()
    ebs_data = fetch_ebs_volumes()
    lambda_data = fetch_lambda_functions()
    rds_data = fetch_rds_instances()
    dynamodb_data = fetch_dynamodb_tables()
    elasticbeanstalk_data = fetch_elastic_beanstalk_environments()
    elb_data = fetch_elastic_load_balancers()
    apigateway_data = fetch_api_gateways()
    ecs_data = fetch_ecs_clusters()
    eks_data = fetch_eks_clusters()
    redshift_data = fetch_redshift_clusters()
    emr_data = fetch_emr_clusters()
    cloudwatch_data = fetch_cloudwatch_alarms()
    s3_data = fetch_s3_buckets()
    iam_data = fetch_iam_roles()
    ses_data = fetch_ses_identities()

    all_data = ec2_data + ebs_data + lambda_data + rds_data + dynamodb_data + elasticbeanstalk_data + elb_data + apigateway_data + ecs_data + eks_data + redshift_data + emr_data + cloudwatch_data + s3_data + iam_data + ses_data

    return all_data 



'''
---------------------------------------------------------------------------------------------------------------------
'''

#Delete AWS Resources Feature Functions Started from here


def delete_ec2_instances(instance_ids, region):
    """
    Deletes specified EC2 instances in a given region.
    
    Parameters:
        instance_ids (list): List of EC2 instance IDs to delete.
        region (str): AWS region where the instances are located.
    """
    ec2 = boto3.client('ec2', region_name=region, verify=certifi.where())
    try:
        print(f"Terminating EC2 instances: {', '.join(instance_ids)} in {region}...")
        response = ec2.terminate_instances(InstanceIds=instance_ids)
        print("Termination initiated. Current states:")
        for instance in response['TerminatingInstances']:
            print(f"Instance {instance['InstanceId']}: {instance['CurrentState']['Name']}")
    except Exception as e:
        print(f"Error terminating instances: {str(e)}")

def delete_ebs_volumes(volume_ids, region):
    """
    Deletes specified EBS volumes in a given region.

    Parameters:
        volume_ids (list): List of EBS volume IDs to delete.
        region (str): AWS region where the volumes are located.
    """
    ec2 = boto3.resource('ec2', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting EBS volumes: {', '.join(volume_ids)} in {region}...")
        for volume_id in volume_ids:
            volume = ec2.Volume(volume_id)
            volume.delete()
            print(f"Volume {volume_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting volumes: {str(e)}")

def delete_lambda_functions(function_names, region):
    """
    Deletes specified Lambda functions in a given region.

    Parameters:
        function_names (list): List of Lambda function names to delete.
        region (str): AWS region where the functions are located.
    """
    lambda_client = boto3.client('lambda', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting Lambda functions: {', '.join(function_names)} in {region}...")
        for function_name in function_names:
            lambda_client.delete_function(FunctionName=function_name)
            print(f"Function {function_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting functions: {str(e)}")    

def delete_rds_instances(instance_ids, region):
    """
    Deletes specified RDS instances in a given region.

    Parameters:
        instance_ids (list): List of RDS instance IDs to delete.
        region (str): AWS region where the instances are located.
    """
    rds_client = boto3.client('rds', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting RDS instances: {', '.join(instance_ids)} in {region}...")
        for instance_id in instance_ids:
            rds_client.delete_db_instance(DBInstanceIdentifier=instance_id, SkipFinalSnapshot=True)
            print(f"Instance {instance_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting instances: {str(e)}")    

def delete_dynamodb_tables(table_names, region):
    """
    Deletes specified DynamoDB tables in a given region.

    Parameters:
        table_names (list): List of DynamoDB table names to delete.
        region (str): AWS region where the tables are located.
    """
    dynamodb = boto3.client('dynamodb', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting DynamoDB tables: {', '.join(table_names)} in {region}...")
        for table_name in table_names:
            dynamodb.delete_table(TableName=table_name)
            print(f"Table {table_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting tables: {str(e)}")   

def delete_elastic_beanstalk_environments(environment_names, region):
    """
    Deletes specified Elastic Beanstalk environments in a given region.

    Parameters:
        environment_names (list): List of Elastic Beanstalk environment names to delete.
        region (str): AWS region where the environments are located.
    """
    eb_client = boto3.client('elasticbeanstalk', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting Elastic Beanstalk environments: {', '.join(environment_names)} in {region}...")
        for environment_name in environment_names:
            eb_client.terminate_environment(EnvironmentName=environment_name)
            print(f"Environment {environment_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting environments: {str(e)}") 

def delete_elastic_load_balancers(load_balancer_names, region):
    """
    Deletes specified Elastic Load Balancers in a given region.

    Parameters:
        load_balancer_names (list): List of Elastic Load Balancer names to delete.
        region (str): AWS region where the load balancers are located.
    """
    elb_client = boto3.client('elbv2', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting Elastic Load Balancers: {', '.join(load_balancer_names)} in {region}...")
        for load_balancer_name in load_balancer_names:
            elb_client.delete_load_balancer(LoadBalancerArn=load_balancer_name)
            print(f"Load Balancer {load_balancer_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting load balancers: {str(e)}")   

def delete_api_gateways(api_gateway_names, region):
    """
    Deletes specified API Gateways in a given region.

    Parameters:
        api_gateway_names (list): List of API Gateway names to delete.
        region (str): AWS region where the API Gateways are located.
    """
    apigateway_client = boto3.client('apigateway', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting API Gateways: {', '.join(api_gateway_names)} in {region}...")
        for api_gateway_name in api_gateway_names:
            apigateway_client.delete_rest_api(restApiId=api_gateway_name)
            print(f"API Gateway {api_gateway_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting API Gateways: {str(e)}") 

def delete_ecs_clusters(cluster_arns, region):
    """
    Deletes specified ECS clusters in a given region.

    Parameters:
        cluster_arns (list): List of ECS cluster ARNs to delete.
        region (str): AWS region where the clusters are located.
    """
    ecs_client = boto3.client('ecs', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting ECS clusters: {', '.join(cluster_arns)} in {region}...")
        for cluster_arn in cluster_arns:
            ecs_client.delete_cluster(cluster=cluster_arn)
            print(f"Cluster {cluster_arn} deleted successfully.")
    except Exception as e:
        print(f"Error deleting ECS clusters: {str(e)}")
    
def delete_eks_clusters(cluster_names, region):
    """
    Deletes specified EKS clusters in a given region.

    Parameters:
        cluster_names (list): List of EKS cluster names to delete.
        region (str): AWS region where the clusters are located.
    """
    eks_client = boto3.client('eks', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting EKS clusters: {', '.join(cluster_names)} in {region}...")
        for cluster_name in cluster_names:
            eks_client.delete_cluster(name=cluster_name)
            print(f"Cluster {cluster_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting EKS clusters: {str(e)}")

def delete_redshift_clusters(cluster_ids, region):
    """
    Deletes specified Redshift clusters in a given region.

    Parameters:
        cluster_ids (list): List of Redshift cluster IDs to delete.
        region (str): AWS region where the clusters are located.
    """
    redshift_client = boto3.client('redshift', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting Redshift clusters: {', '.join(cluster_ids)} in {region}...")
        for cluster_id in cluster_ids:
            redshift_client.delete_cluster(ClusterIdentifier=cluster_id, SkipFinalClusterSnapshot=True)
            print(f"Cluster {cluster_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting Redshift clusters: {str(e)}")    

def delete_emr_clusters(cluster_ids, region):
    """
    Deletes specified EMR clusters in a given region.

    Parameters:
        cluster_ids (list): List of EMR cluster IDs to delete.
        region (str): AWS region where the clusters are located.
    """
    emr_client = boto3.client('emr', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting EMR clusters: {', '.join(cluster_ids)} in {region}...")
        for cluster_id in cluster_ids:
            emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
            print(f"Cluster {cluster_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting EMR clusters: {str(e)}") 

def delete_s3_buckets(bucket_names):
    """
    Deletes specified S3 buckets.

    Parameters:
        bucket_names (list): List of S3 bucket names to delete.
    """
    s3 = boto3.resource('s3', verify=certifi.where())
    try:
        print(f"Deleting S3 buckets: {', '.join(bucket_names)}...")
        for bucket_name in bucket_names:
            bucket = s3.Bucket(bucket_name)
            bucket.objects.delete()
            bucket.delete()
            print(f"Bucket {bucket_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting buckets: {str(e)}")  

def delete_ses_identities(identity_names):
    """
    Deletes specified SES identities.

    Parameters:
        identity_names (list): List of SES identity names to delete.
    """
    ses = boto3.client('ses', verify=certifi.where())
    try:
        print(f"Deleting SES identities: {', '.join(identity_names)}...")
        for identity_name in identity_names:
            ses.delete_identity(Identity=identity_name)
            print(f"Identity {identity_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting identities: {str(e)}")   

def delete_cloudwatch_alarms(alarm_names, region):
    """
    Deletes specified CloudWatch alarms in a given region.

    Parameters:
        alarm_names (list): List of CloudWatch alarm names to delete.
        region (str): AWS region where the alarms are located.
    """
    cloudwatch = boto3.client('cloudwatch', region_name=region, verify=certifi.where())
    try:
        print(f"Deleting CloudWatch alarms: {', '.join(alarm_names)} in {region}...")
        for alarm_name in alarm_names:
            cloudwatch.delete_alarms(AlarmNames=[alarm_name])
            print(f"Alarm {alarm_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting alarms: {str(e)}")   


'''
-------------------------------------------------------------------------------------------------------------
'''

#Create AWS Resources. 

def create_ec2_instance():
    """Launch EC2 instances with user data, IP retrieval, and dynamic key pair handling."""
    region = input("Enter the region (eg. ap-south-1): ")
    instance_name = input("Enter the name for the instances (eg. MyEc2Instance): ")
    ami_id = input("Enter the AMI ID (eg.  ami-0614680123427b75e): ")
    instance_type = input("Enter the instance type (e.g., t2.micro): ")
    count = int(input("Enter the number of instances to launch: "))
    use_existing_key = input("Use an existing key pair? (y/n): ").lower() == 'y'

    ec2_client = boto3.client('ec2', region_name=region)

    # Key Pair Handling
    if use_existing_key:
        print("\nFetching available key pairs...")
        try:
            key_pairs = ec2_client.describe_key_pairs()['KeyPairs']
            if not key_pairs:
                print("No key pairs found. Please create one in the AWS Management Console.")
                return
            print("\nAvailable Key Pairs:")
            for i, kp in enumerate(key_pairs):
                print(f"{i + 1}. {kp['KeyName']}")
            key_index = int(input("Select a key pair by number: ")) - 1
            key_name = key_pairs[key_index]['KeyName']

            # Warn if the private key file isn't available locally
            pem_file = f"{key_name}.pem"
            if not os.path.exists(pem_file):
                print(f"WARNING: Private key file '{pem_file}' not found locally. Connection might fail.")
        except Exception as e:
            print(f"Error fetching key pairs: {e}")
            return
    else:
        # Create a new key pair dynamically
        key_name = input("Enter a name for the new key pair: ")
        key_save_path = input("Enter the path where you want to save the key pair: ").strip()

        # Validate the directory
        if not os.path.exists(key_save_path):
            print(f"Directory '{key_save_path}' does not exist.")
            create_dir = input("Do you want to create this directory? (y/n): ").lower()
            if create_dir == 'y':
                try:
                    os.makedirs(key_save_path)
                    print(f"Directory '{key_save_path}' created.")
                except Exception as e:
                    print(f"Error creating directory: {e}")
                    return
            else:
                print("Operation canceled.")
                return

        try:
            key_pair = ec2_client.create_key_pair(KeyName=key_name)
            pem_file_path = os.path.join(key_save_path, f"{key_name}.pem")
            with open(pem_file_path, "w") as file:
                file.write(key_pair['KeyMaterial'])
            os.chmod(pem_file_path, 0o400)  # Set appropriate permissions for the key file
            print(f"Key pair '{key_name}' created and saved as '{pem_file_path}'.")
        except Exception as e:
            print(f"Error creating key pair: {e}")
            return

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

    # Optional User Data

    # Launch the instance(s)
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

        # Fetch public IP addresses
        print("\nFetching instance details...")
        reservations = ec2_client.describe_instances(InstanceIds=instance_ids)['Reservations']
        for reservation in reservations:
            for instance in reservation['Instances']:
                public_ip = instance.get('PublicIpAddress', 'N/A')
                print(f"Instance ID: {instance['InstanceId']}, Public IP: {public_ip}")
    except ClientError as e:
        print(f"Error launching EC2 instances: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"Unexpected error: {e}")
