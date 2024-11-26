import boto3
import certifi
import cleansweep.spinner as spinner
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

