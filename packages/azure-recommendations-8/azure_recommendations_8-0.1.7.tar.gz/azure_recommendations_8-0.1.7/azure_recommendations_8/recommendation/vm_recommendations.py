import json
from datetime import datetime, timedelta
import re
import pytz
import requests
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient

import logging

from azure_recommendations_8.recommendation import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class vm_recommendations:
    def __init__(self, credentials: ClientSecretCredential, authorization_token: str):
        """
        :param credentials: ClientSecretCredential
        """
        super().__init__(credentials)
        self.credentials = credentials
        self.authorization_token = authorization_token

    # provides the recommendation to use ssh authentication type
    def check_for_ssh_authentication_type(self, vm_list: dict) -> list:
        """
        :param vm_list: list of the virtual machine across all the subscriptions
        :return: list of recommendations
        """
        logger.info(" ---Inside vm_recommendations :: disk_encryption_for_boot_disk_volumes()--- ")

        response = []

        for subs, vms in vm_list.items():
            for vm in vms:
                # print(vm)
                # print(vm.storage_profile.os_disk)
                # print(vm.storage_profile.os_disk.managed_disk)
                try:
                    if vm.os_profile.linux_configuration is not None:
                        if not vm.os_profile.linux_configuration.disable_password_authentication:
                            temp = {
                                'recommendation': 'Use SSH authentication type',
                                'description': 'the SSH authentication type for the selected Microsoft Azure '
                                               'virtual machine is password-based, therefore the SSH authentication '
                                               'method configured for the specified VM is not secure',
                                'resource': 'Virtual Machine',
                                'subscription_id': subs,
                                'resource_id': vm.id,
                                'metadata': {
                                    'name': vm.name,
                                    'tags': vm.tags
                                },
                                'current cost': 0,
                                'effective cost': 0,
                                'savings': 0,
                                'savings %': 0,
                                'source': 'Klera'
                            }
                            response.append(temp)
                except AttributeError:
                    continue

        return response

    # Provides recommendations for removing unattached virtual machine disk volumes
    def remove_unattached_disk_volume(self, disk_list: dict) -> list:
        """
        :param disk_list: list of disks across all the subscriptions
        :return: list of recommendations
        """
        logger.info(" ---Inside vm_recommendations :: remove_unattached_disk_volumes()--- ")

        utils_obj = utils(self.credentials, self.authorization_token)
        response = []

        for subscription, disks in disk_list.items():
            for disk in disks:
                # print(disk)
                if disk.disk_state == 'Unattached':
                    prices = utils_obj.get_price(subscription_id=subscription, resource=disk)
                    # print('*******************')
                    # print(prices)
                    current_price = 0
                    if prices['unitOfMeasure'] == '1 GB':
                        current_price = disk.disk_size_gb * prices['retail_price']
                    elif prices['unitOfMeasure'] == '1/Month':
                        current_price = prices['retail_price']

                    effective_price = 0
                    savings = current_price - effective_price
                    try:
                        savings_p = ((current_price - effective_price) / current_price) * 100
                    except ZeroDivisionError:
                        savings_p = 0

                    temp = {
                        'recommendation': 'Remove unattached disk',
                        'description': 'disk volume is not attached to a Microsoft Azure virtual machine, remove it to optimize the cost',
                        'resource': 'Virtual Machine',
                        'subscription_id': subscription,
                        'resource_id': disk.id,
                        'metadata': {
                            'name': disk.name,
                            'tags': disk.tags
                        },
                        'current cost': current_price,
                        'effective cost': effective_price,
                        'savings': savings,
                        'savings %': savings_p,
                        'source': 'Klera'
                    }
                    response.append(temp)

        return response

    # Provides the recommendation for Remove Old Virtual Machine Disk Snapshots
    def remove_old_vm_disk_snapshot(self, snapshot_list: dict) -> list:
        """
        :param snapshot_list: list of snapshots across all subscriptions
        :return: list of recommendations
        """
        logger.info(" ---Inside vm_recommendations :: remove_old_vm_disk_snapshot()--- ")

        response = []
        utils_obj = utils(self.credentials, self.authorization_token)

        time_30_days_ago = datetime.now() - timedelta(days=30)
        timezone = pytz.timezone("UTC")
        time_30_days_ago = timezone.localize(time_30_days_ago)

        for subscription, snapshots in snapshot_list.items():
            for snapshot in snapshots:
                time_created = snapshot.time_created
                if time_30_days_ago > time_created:
                    prices = utils_obj.get_price(subscription_id=subscription, resource=snapshot)
                    # print(prices)
                    current_price = 0
                    if prices['unitOfMeasure'] == '1 GB/Month':
                        current_price = snapshot.disk_size_gb * prices['retail_price']

                    effective_price = 0
                    savings = current_price - effective_price
                    try:
                        savings_p = ((current_price - effective_price) / current_price) * 100
                    except ZeroDivisionError:
                        savings_p = 0

                    temp = {
                        'recommendation': 'Remove 30 days older vm disk snapshot',
                        'description': 'virtual machine disk snapshot is 30 days old and can be safely removed '
                                       'from your Azure cloud account',
                        'resource': 'Virtual Machine',
                        'subscription_id': subscription,
                        'resource_id': snapshot.id,
                        'metadata': {
                            'name': snapshot.name,
                            'tags': snapshot.tags
                        },
                        'current cost': current_price,
                        'effective cost': effective_price,
                        'savings': savings,
                        'savings %': savings_p,
                        'source': 'Klera'
                    }
                    response.append(temp)

        return response

    # Provides the recommendation for disable premium ssd
    def disable_premium_ssd(self, vm_list: dict) -> list:
        """
        :param vm_list: list of Azure Virtual Machines
        :return: list of recommendations
        """
        logger.info(" ---Inside vm_recommendations :: disable_premium_ssd()--- ")

        response = []

        for subscription, vms in vm_list.items():
            for vm in vms:
                os_disk_type = vm.storage_profile.os_disk.managed_disk.storage_account_type
                try:
                    data_disk_type = vm.storage_profile.data_disks.managed_disk.storage_account_type
                    if os_disk_type == 'Premium_LRS' or data_disk_type == 'Premium_LRS':
                        temp = {
                            'recommendation': 'Disable premium SSD',
                            'description': 'Microsoft Azure virtual machines (VMs) are using Premium SSD '
                                           'volumes, use Standard SSD disk volumes for cost-effective storage '
                                           'that fits a broad range of workloads',
                            'resource': 'Virtual Machine',
                            'subscription_id': subscription,
                            'resource_id': vm.id,
                            'metadata': {
                                'name': vm.name,
                                'tags': vm.tags
                            },
                            'current cost': 0,
                            'effective cost': 0,
                            'savings': 0,
                            'savings %': 0,
                            'source': 'Klera'
                        }
                        response.append(temp)
                except AttributeError:
                    if os_disk_type == 'Premium_LRS':
                        temp = {
                            'recommendation': 'Disable premium SSD',
                            'description': 'Microsoft Azure virtual machines (VMs) are using Premium SSD '
                                           'volumes, use Standard SSD disk volumes for cost-effective storage '
                                           'that fits a broad range of workloads',
                            'resource': 'Virtual Machine',
                            'subscription_id': subscription,
                            'resource_id': vm.id,
                            'metadata': {
                                'name': vm.name,
                                'tags': vm.tags
                            },
                            'current cost': 0,
                            'effective cost': 0,
                            'savings': 0,
                            'savings %': 0,
                            'source': 'Klera'
                        }
                        response.append(temp)

        return response

    # Provides the recommendation for enable auto-shutdown
    def enable_auto_shutdown(self, vm_list: dict) -> list:
        """
        :param vm_list: list of azure virtual machines
        :return: list of recommendation
        """
        logger.info(" ---vm_recommendations :: enable_auto_shutdown()--- ")

        response = []
        utils_obj = utils(self.credentials, self.authorization_token)

        for subscription, vms in vm_list.items():
            resource_client = ResourceManagementClient(credential=self.credentials, subscription_id=subscription)
            for vm in vms:
                auto_shutdown_status = resource_client.resources.get_by_id(vm.id, '2022-11-01'). \
                    properties.get('autoShutdownSettings')
                if auto_shutdown_status is None or auto_shutdown_status == 'Disabled':
                    price = utils_obj.get_price(vm, subscription_id=subscription)
                    # print(price)
                    temp = {
                        'recommendation': 'Enable Auto Shutdown',
                        'description': 'Enable Auto Shutdown feature on Microsoft Azure virtual machines (VMs) in '
                                       'order to minimize waste and control VM costs',
                        'resource': 'Virtual Machine',
                        'subscription_id': subscription,
                        'resource_id': vm.id,
                        'metadata': {
                            'name': vm.name,
                            'tags': vm.tags
                        },
                        'current cost': 0,
                        'effective cost': 0,
                        'savings': 0,
                        'savings %': 0,
                        'source': 'Klera'
                    }
                    response.append(temp)

        return response

    # Provides the recommendation for unused load balancers
    def unused_load_balancers(self, lb_list: dict) -> list:
        """
        :param lb_list: list of load balancers across all subscriptions
        :return: list of recommendations
        """
        logger.info(" ---Inside vm_recommendation :: unused_load_balancers()--- ")

        response = []

        return response

    # Provides the recommendations for reservations
    def get_reservation_recommendations(self, resource_groups: dict) -> list:
        """
        :param resource_groups:
        :return: list of recommendations
        """
        logger.info(" ---Inside vm_recommendations :: get_reservation_recommendations() ---")

        recommendations = []

        for subscription, rg_list in resource_groups.items():
            for rg in rg_list:
                url = "https://management.azure.com//subscriptions/{}/resourceGroups/{}/providers/Microsoft.Consumption/reservationRecommendations?api-version=2021-10-01".format(subscription, rg)

                payload = {}
                headers = {
                    'Authorization': 'Bearer '+self.authorization_token
                }

                response = requests.request("GET", url, headers=headers, data=payload)

                data = json.loads(response.text)
                # print(rg)
                # print(json.dumps(data))
                for item in data['value']:
                    lookback_period = item['properties']['lookBackPeriod']
                    x = re.findall('^Last.Days$', lookback_period)

                    current_cost = item['properties']['costWithNoReservedInstances']

                    effective_cost = item['properties']['totalCostWithReservedInstances']

                    # print('current cost')
                    # print(current_cost)
                    # print('effective cost')
                    # print(effective_cost)

                    if x:
                        if '7' in lookback_period:
                            current_cost = (current_cost / (7*24))*730
                            effective_cost = (effective_cost / (7*24))*730

                    temp = {
                        'Subscription Id': subscription,
                        'Resource Group': rg,
                        'Number of Instances': item['properties']['recommendedQuantity'],
                        'Current Cost': current_cost,
                        'Effective cost': effective_cost,
                        'Net Savings': current_cost - effective_cost,
                        'Savings %': ((current_cost - effective_cost)/current_cost)*100,
                        'Instance Flexibility Group': item['properties']['instanceFlexibilityGroup'],
                        'location': item['location'],
                        'Term': item['properties']['term'],
                        'source': 'Azure'
                    }
                    recommendations.append(temp)

        return recommendations

