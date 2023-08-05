import time

from boto3 import session
import logging
from aws_cost_optimization_3.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

__author__ = "Dheeraj Banodha"
__version__ = '0.1.6'


class aws_client:
    def __init__(self, **kwargs):
        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            self.session = session.Session(
                aws_access_key_id=kwargs['aws_access_key_id'],
                aws_secret_access_key=kwargs['aws_secret_access_key'],
            )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])

        self.regions = get_regions(self.session)
        self.aws_region_map = {
            'ca-central-1': 'Canada (Central)',
            'ap-northeast-3': 'Asia Pacific (Osaka-Local)',
            'us-east-1': 'US East (N. Virginia)',
            'ap-northeast-2': 'Asia Pacific (Seoul)',
            'us-gov-west-1': 'AWS GovCloud (US)',
            'us-east-2': 'US East (Ohio)',
            'ap-northeast-1': 'Asia Pacific (Tokyo)',
            'ap-south-1': 'Asia Pacific (Mumbai)',
            'ap-southeast-2': 'Asia Pacific (Sydney)',
            'ap-southeast-1': 'Asia Pacific (Singapore)',
            'sa-east-1': 'South America (Sao Paulo)',
            'us-west-2': 'US West (Oregon)',
            'eu-west-1': 'EU (Ireland)',
            'eu-west-3': 'EU (Paris)',
            'eu-west-2': 'EU (London)',
            'us-west-1': 'US West (N. California)',
            'eu-central-1': 'EU (Frankfurt)',
            'eu-north-1': 'EU (Stockholm)'
        }

    def gp2_to_gp3(self, data: dict) -> dict:
        """
        :return: list of cost saving recommendations
        """
        logger.info(" ---Inside aws_client :: gp2_to_gp3()--- ")

        region = data['Metadata']['Region']
        resolved_region = self.aws_region_map[region]

        Filters = [
            {'Type': 'TERM_MATCH', 'Field': 'volumeType', 'Value': 'General Purpose'},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
        ]
        price = get_pricing(self.session, region, 'AmazonEC2', Filters=Filters, service_name='volume')

        client = self.session.client('ec2', region_name=region)
        response = client.describe_volumes(
            VolumeIds=[
                data['Id']
            ]
        )
        size = 1
        for volume in response['Volumes']:
            if volume['VolumeId'] == data['Id']:
                size = volume['Size']

        current_cost = float(price['gp2']) * float(size)
        effective_cost = float(price['gp3']) * float(size)
        recommendation = {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': current_cost - effective_cost,
            'Savings %': ((current_cost - effective_cost)/current_cost)*100
        }

        return recommendation

    def rds_upgrades(self) -> list:
        """
        :return: list of cost saving recommendations
        """
        logger.info(" ---Inside aws_client :: rds_upgrades()--- ")

        recommendations = []

        rds_instances = list_rds_instances(self.session, self.regions)

        for region, rds_list in rds_instances.items():
            resolved_region = self.aws_region_map[region]
            for instance in rds_list:
                instance_type = instance['DBInstanceClass']
                instance_family = instance_type.split('.')[1]

                Filters = [
                    {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
                    {'Type': 'TERM_MATCH', 'Field': 'databaseEngine', 'Value': instance['Engine']},
                    {'Type': 'TERM_MATCH', 'Field': 'deploymentOption', 'Value': 'Single-AZ' if instance['MultiAZ'] else 'Multi-AZ'},
                    {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Database Instance'},
                    {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
                ]

                def evaluate(frm: str, to: str):
                    price_from = get_pricing(
                        self.session, region, 'AmazonRDS',
                        Filters,
                        service_name='instanceType'
                    )
                    print(price_from)
                    Filters[0]['Value'] = instance_type.replace(frm, to)
                    price_to = get_pricing(
                        self.session, region, 'AmazonRDS', Filters,
                        service_name='rds'
                    )
                    print(price_to)
                    current_cost = float(price_from[instance_type]) * 730
                    effective_cost = float(price_to[instance_type.replace(frm, to)]) * 730

                    recommendation = {
                        'Region': region,
                        'Instance Id': instance['DBInstanceIdentifier'],
                        'Instance Type': instance_type,
                        'Upgrade To': instance_type.replace(frm, to),
                        'Current Cost': current_cost,
                        'Effective Cost': effective_cost,
                        'Savings': current_cost - effective_cost,
                        'Savings %': ((current_cost - effective_cost) / current_cost) * 100
                    }
                    return recommendation

                match instance_family:
                    case 'm3':
                        recommendations.append(evaluate('m3', 'm5'))
                    case 'r3':
                        recommendations.append(evaluate('r3', 'r5'))
                    case 'm1':
                        recommendations.append(evaluate('m1', 't2'))

        return recommendations

    # InComplete ******************************************
    # returns the recommendations for ec2_upgrades
    # def ec2_upgrades(self) -> list:
    #     """
    #     :return:
    #     """
    #     logger.info(" ---Inside aws_client :: rds_upgrades()--- ")
    #
    #     recommendations = []
    #
    #     ec2_instances = list_ec2_instances(self.session, self.regions)
    #
    #     for region, reservations in ec2_instances.items():
    #         resolved_region = self.aws_region_map[region]
    #         for reservation in reservations:
    #             for instance in reservation['Instances']:
    #                 instance_type = instance['InstanceType']
    #                 instance_family = instance_type.split('.')[0]
    #                 print(instance['InstanceId'])
    #                 print(instance_type)
    #
    #                 Filters = [
    #                     {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
    #                     {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region},
    #                     {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Red Hat Enterprise Linux with HA'},
    #                     {'Type': 'TERM_MATCH', 'Field': 'marketoption', 'Value': 'OnDemand'}
    #                 ]
    #                 print(get_pricing(
    #                     self.session, region, 'AmazonEC2', Filters ,
    #                         service_name = 'ec2_instance
    #                 ))
    #
    #     return recommendations

    def unallocated_eip(self, data) -> dict:
        """
        :return: this list the potential savings
        """
        logger.info(" ---Inside aws_client :: unallocated_eip()--- ")

        region = data['Metadata']['Region']

        resolved_region = self.aws_region_map[region]

        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'IP Address'},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region},
            {'Type': 'TERM_MATCH', 'Field': 'usagetype', 'Value': 'APS3-ElasticIP:IdleAddress'}
        ]
        price = get_pricing(self.session, region, 'AmazonEC2', filters, service_name='eip')
        current_cost = float(price['APS3-ElasticIP:IdleAddress']) * 730
        effective_cost = 0
        recommendation = {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': current_cost - effective_cost,
            'Savings %': ((current_cost - effective_cost) / current_cost) * 100
        }

        return recommendation

#   Provided cost details for recommendation unused_ebs
    def unused_ebs_costing(self, data: dict) -> dict:
        """
        :param data:
        :return:
        """
        logger.info(" ---Inside aws_client :: unused_ebs_costing()--- ")

        region = data['Metadata']['Region']

        if data['Metadata']['Instance Type'].startswith('gp'):
            volume_type = 'General Purpose'
        else:
            volume_type = "Provisioned IOPS"

        resolved_region = self.aws_region_map[region]
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'volumeType', 'Value': volume_type},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
        ]

        price = get_pricing(self.session, data['Metadata']['Region'], 'AmazonEC2', filters, service_name='volume')

        client = self.session.client('ec2', region_name=region)
        response = client.describe_volumes(
            VolumeIds=[
                data['Id']
            ]
        )
        size = 1
        for volume in response['Volumes']:
            if volume['VolumeId'] == data['Id']:
                size = volume['Size']

        current_cost = float(price['gp2']) * float(size)
        effective_cost = 0
        recommendation = {
            'Current Cost': current_cost,
            'Effective Cost': effective_cost,
            'Savings': current_cost - effective_cost,
            'Savings %': ((current_cost - effective_cost) / current_cost) * 100
        }

        return recommendation

    # returns the cost details of recommendations
    def cost_details(self, data: dict) -> dict:
        """
        :param data:
        :return:
        """
        available_cost_details = {
            'Delete idle EBS volume': self.unused_ebs_costing,
            'Associate the EIP with a running active instance, or release the unassociated EIP': self.unallocated_eip,
            'Migrate GP2 volume to GP3': self.gp2_to_gp3,
            'Remove unused EBS volume': self.unused_ebs_costing,
            'Purge unattached volume': self.unused_ebs_costing,
            # 'Purge 8 week older snapshot': None,
            # 'Remove AMI': None,
            # 'Remove Unused ELB': None,
            # 'Remove Customer Master Key': None,
            # 'Delete idle rds instance': None,
            # 'Consider shutting down the cluster and taking a final snapshot, or downsizing the cluster': None,
        }
        if data['Recommendation'] in available_cost_details.keys():
            response = available_cost_details[data['Recommendation']](data)
        else:
            response = {
                'Current Cost': None,
                'Effective Cost': None,
                'Savings': None,
                'Savings %': None
            }

        return response
