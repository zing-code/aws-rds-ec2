import boto3
from datetime import datetime, timedelta, tzinfo

client = boto3.client('ec2',region_name='ap-southeast-1')
snapshots = client.describe_snapshots(OwnerIds=['673883514524'])
    
class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
        return self.name

UTC = Zone(5.30,False,'UTC')

#retention period of X days
retentionDate = datetime.now(UTC) - timedelta(days=0)

def lambda_handler(event,context):
    for snapshot in snapshots['Snapshots']:
        if snapshot['StartTime'] < retentionDate:
            id = snapshot['SnapshotId']
            #client.delete_snapshot(SnapshotId=id)
            
