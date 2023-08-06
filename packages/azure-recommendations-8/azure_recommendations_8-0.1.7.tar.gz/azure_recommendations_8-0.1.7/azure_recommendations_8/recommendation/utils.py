"""
Contains all utility functions
"""
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
import requests
import json

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class utils:
    def __init__(self, credentials: ClientSecretCredential, authorization_token: str):
        """
        :param credentials:  ClientSecretCredential object
        """
        self.credentials = credentials
        self.authorization_token = authorization_token

    def list_subscriptions(self) -> list:
        """
        :param self:
        :return: list of Azure subscriptions
        """
        logger.info(" ---Inside utils :: list_subscriptions()--- ")

        subs_client = SubscriptionClient(credential=self.credentials)

        subs_list = subs_client.subscriptions.list()
        response = []
        for subs in subs_list:
            sid = subs.id
            response.append(sid.split('/')[-1])

        return response

    def list_vms(self, subscriptions: list) -> dict:
        """
        :param subscriptions: list of subscriptions
        :return: dictionary containing the list VMs
        """
        logger.info(" ---Inside utils :: list_vms()--- ")

        response = {}

        for subscription in subscriptions:
            compute_client = ComputeManagementClient(credential=self.credentials, subscription_id=subscription)
            vm_list = compute_client.virtual_machines.list_all()

            for vm in vm_list:
                response.setdefault(subscription, []).append(vm)

        return response

    # returns the list of disks across all the subscriptions
    def list_disks(self, subscriptions: list) -> dict:
        """
        :param subscriptions: list of subscriptions
        :return:
        """
        logger.info(" ---Inside utils :: list_disks()--- ")
        response = {}

        for subscription in subscriptions:
            compute_client = ComputeManagementClient(credential=self.credentials, subscription_id=subscription)
            disk_lst = compute_client.disks.list()

            for disk in disk_lst:
                response.setdefault(subscription, []).append(disk)

        return response

    # returns the list of snapshots
    def list_snapshots(self, subscriptions: list) -> dict:
        """
        :param subscriptions: list of azure subscriptions
        :return: list of snapshots
        """
        logger.info(" ---Inside utils :: list_snapshots()--- ")
        response = {}

        for subscription in subscriptions:
            compute_client = ComputeManagementClient(credential=self.credentials, subscription_id=subscription)
            snapshot_list = compute_client.snapshots.list()

            for snapshot in snapshot_list:
                response.setdefault(subscription, []).append(snapshot)

        return response

    '''***********************Incomplete'''
    # returns the list of load balancers across all subscriptions
    def list_load_balancers(self, subscriptions: list) -> dict:
        """
        :param subscriptions: list of subscription in an azure account
        :return: dictionary containing list of load balancers
        """
        logger.info(" ---Inside utils :: list_load_balancers()--- ")

        response = {}

        for subscription in subscriptions:
            client = NetworkManagementClient(credential=self.credentials, subscription_id=subscription)
            lb_list = client.load_balancers.list_all()
            for lb in lb_list:
                print(lb)

        return response

    # returns the list of NSG
    def list_nsg(self, subscriptions: list) -> dict:
        """
        :param subscriptions: list of subscriptions
        :return: dictionary containing list of nsg
        """
        logger.info(" ---Inside utils :: list_nsg()--- ")

        response = {}

        for subscription in subscriptions:
            client = NetworkManagementClient(credential=self.credentials, subscription_id=subscription)
            nsg_list = client.network_security_groups.list_all()

            for nsg in nsg_list:
                response.setdefault(subscription, []).append(nsg)

        return response

    # returns the pricing of the particular resource
    def get_price(self, resource, subscription_id: str) -> dict:
        """
        :param subscription_id:
        :param resource:
        :return:
        """
        logger.info(" ---Inside utils :: get_price()--- ")

        # print(vm)
        # arm_sku_name = vm.hardware_profile.vm_size
        # arm_region_name = vm.location
        # print(vm.hardware_profile)
        # print(vm.storage_profile)
        # print(vm.storage_profile.image_reference)
        # print(vm.storage_profile.os_disk)
        # print(vm.os_profile)
        # print(vm.os_profile.linux_configuration)
        # print(vm.network_profile)
        # print(vm.network_profile.network_interfaces)
        # print(vm.diagnostics_profile)
        # print(vm.diagnostics_profile.boot_diagnostics)
        #
        # compute_client = ComputeManagementClient(credential=self.credentials, subscription_id=subscription_id)

        # resource_group_name = 'NewResourceGroup'
        # volume_name = 'newdisk'
        #
        # volume_sku = compute_client.disks.get(
        #     resource_group_name=resource_group_name,
        #     disk_name=volume_name
        # )
        # print(volume_sku.sku)


        #
        # vm_sizes = compute_client.virtual_machine_sizes.list(location='eastus')
        #
        # print("vm sizes **********************")
        # for vm_size in vm_sizes:
        #     print(vm_size)
        # print("**********************")

        # Usage details API
        usage_start = datetime.datetime.now().date() - relativedelta(months=6)
        # print(usage_start)
        usage_end = datetime.datetime.now().date()

        url = "https://management.azure.com/subscriptions/{}/providers/Microsoft" \
              ".Consumption/usageDetails?api-version=2019-10-01&$filter=properties/usageStart ge '{}' and " \
              "properties/usageEnd lt '{}'".format(subscription_id, str(usage_start), str(usage_end))

        payload = {}

        headers = {
            'Authorization': 'Bearer '+self.authorization_token
        }
        # print('Authorization: '+ self.authorization_token)

        response = requests.request("GET", url, headers=headers, data=payload)

        response_json_obj = json.loads(response.text)
        # print(response_json_obj)
        meter_id = None
        if 'value' not in response_json_obj:
            logger.info('Resource not found in billing data')
            return {
                'unitOfMeasure': None,
                'retail_price': 0
            }

        for item in response_json_obj['value']:
            # print(item)
            resource_id = item['properties']['resourceId']

            if resource.id == resource_id:
                meter_id = item['properties']['meterId']
                break

        ################################################################
        if meter_id is None:
            logger.info('Resource not found in billing data')
            return {
                'unitOfMeasure': None,
                'retail_price': 0
            }
        else:
            url = "https://prices.azure.com/api/retail/prices"
            params = {
                '$filter': "meterId eq '{}' and armRegionName eq '{}' and currencyCode eq 'USD'".format(meter_id, resource.location),
                '$skip': 0
            }
            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload, params=params).text
            json_obj = json.loads(response)

            # print('*******************')
            # print(resource)
            res = {
                'unitOfMeasure': None,
                'retail_price': 0
            }
            for obj in json_obj['Items']:
                if 'reservationTerm' in obj:
                    if obj['reservationTerm'] == '':
                        # print(json.dumps(obj, indent=4))
                        res['unitOfMeasure'] = obj['unitOfMeasure']
                        res['retail_price'] = obj['retailPrice']
                        break
                else:
                    # print(json.dumps(obj, indent=4))
                    res['unitOfMeasure'] = obj['unitOfMeasure']
                    res['retail_price'] = obj['retailPrice']
                    break

            # res = {
            #     'unitOfMeasure': json_obj['Items'][0]['unitOfMeasure'],
            #     'retail_price': json_obj['Items'][0]['retailPrice']
            # }
            return res

        # if 'Items' in json_obj:
        #     count += len(json_obj['Items'])
            # for item in json_obj['Items']:
            #     if str(item['armSkuName']) == 'Standard_D64s_v5':
            #         print(str(item['armSkuName'])+": "+str(item['unitPrice']))
            #         print(json.dumps(item, indent=4))



        # volume_resource = resource_client.resources.get(
        #     resource_group_name=resource_group_name,
        #     resource_provider_namespace='Microsoft.Compute',
        #     parent_resource_path='virtualMachines',
        #     resource_type='disks',
        #     resource_name=volume_name,
        #     api_version='2021-10-01'
        # )
        # print(volume_resource)


        # meter_id = compute_client.resource_skus.get_by_resource_and_sku(
        #     resource_id='/subscriptions/9de2c37b-d047-486b-abf9-86152a039672/resourceGroups/NewResourceGroup/providers/Microsoft.Compute/disks/newdisk',
        #     sku=volume_sku
        # ).meter_details[0].meter_id
        # print(meter_id)



        # skip = 0
        #
        # while True:
        #     service_name_list = set()
        #     url = "https://prices.azure.com/api/retail/prices"
        #     params = {
        #         '$filter': "location eq 'CA East' and currencyCode eq 'USD'",
        #         '$skip': skip
        #     }
        #     response = requests.request("GET", url, params=params).text
        #     json_obj = json.loads(response)
        #     # print(json.dumps(json_obj, indent=4))
        #
        #     if len(json_obj['Items']) > 0:
        #         for item in json_obj['Items']:
        #             service_name_list.add(item['serviceName'])
        #     else:
        #         print(skip)
        #         break
        #     skip += 100
        #     print(skip)
        #
        #     for name in service_name_list:
        #         print(name)

    # returns the list of resource groups
    def list_resource_groups(self, subscriptions: list) -> dict:
        """
        :param subscriptions:
        :return:
        """
        logger.info(" ---Inside utils :: list_resource_groups()--- ")

        rg_list = {}

        for subscription_id in subscriptions:
            url = "https://management.azure.com/subscriptions/{}/resourcegroups?api-version=2021-04-01".format(subscription_id)

            payload = {}
            headers = {
                'Authorization': 'Bearer '+self.authorization_token
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            data = json.loads(response.text)

            for item in data['value']:
                rg_list.setdefault(subscription_id, []).append(item['name'])

        return rg_list





