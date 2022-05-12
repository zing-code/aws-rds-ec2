import boto3
import datetime
ls=[]

region = 'ap-southeast-1'
purposes = ['WEB','TEST','VOLUME','NONE'] #State the purpose
ec2_stop = boto3.client('ec2', region_name=region)
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    
    date_filter = (datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d")
    for purpose in purposes:
        filters = [
            {'Name':'launch-time', 'Values':[date_filter+'*']},
            {'Name':'instance-state-name', 'Values':['running']},
            {'Name':'tag:Purpose', 'Values':[purpose]},
        
        ]
    
        instances = ec2.instances.filter(Filters=filters)

        for instance in instances:
            ls.append(instance.id)
    ec2_stop.stop_instances(InstanceIds=ls)
    print(ls)
    
