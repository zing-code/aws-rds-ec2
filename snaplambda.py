import json
import boto3
from datetime import datetime, timedelta, tzinfo

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
retentionDate = datetime.now(UTC) - timedelta(days=1)


def lambda_handler(event, context):
    rds = boto3.setup_default_session(region_name='ap-southeast-1')
    client = boto3.client('rds')
    snapshots = client.describe_db_snapshots(SnapshotType='manual')
    for snapshot in snapshots['DBSnapshots']:
        if snapshot['SnapshotCreateTime'] < retentionDate:
            print (snapshot['DBSnapshotIdentifier'])
            client.delete_db_snapshot(DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier'])
              
