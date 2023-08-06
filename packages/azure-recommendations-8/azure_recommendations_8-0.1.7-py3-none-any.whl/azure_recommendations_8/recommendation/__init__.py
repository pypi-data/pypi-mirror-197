import json

import requests
from azure.identity import ClientSecretCredential

from azure_recommendations_8.recommendation.network_recommendations import network_recommendations
from azure_recommendations_8.recommendation.utils import utils
from azure_recommendations_8.recommendation.vm_recommendations import vm_recommendations
from azure_recommendations_8.recommendation.advisor_recommendations import advisor_recommendations

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class recommendation(utils, vm_recommendations, advisor_recommendations, network_recommendations):
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        """
        :param tenant_id: tenant Id from Azure
        :param client_id: Access ID
        :param client_secret: Secret Access ID
        """

        self.credentials = ClientSecretCredential(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id
        )
        self.authorization_token = get_token(tenant_id, client_id, client_secret)
        super().__init__(self.credentials, self.authorization_token)

    def get_recommendations(self) -> (list, list):
        """
        :return: list of recommendations
        """
        logger.info(" ---Inside recommendation :: get_recommendations()--- ")

        response = []

        subscriptions = self.list_subscriptions()
        print('subscriptions')
        print(subscriptions)

        vm_list = self.list_vms(subscriptions)
        # print("vm_list")
        # print(vm_list)
        # response.extend(self.check_for_ssh_authentication_type(vm_list))
        # response.extend(self.disable_premium_ssd(vm_list))
        response.extend(self.enable_auto_shutdown(vm_list))

        disk_list = self.list_disks(subscriptions)
        # print('disk list')
        # for s, disks in disk_list.items():
        #     for disk in disks:
        #         print(disk)
        response.extend(self.remove_unattached_disk_volume(disk_list))
        #
        snapshot_list = self.list_snapshots(subscriptions)
        # print('snapshot list')
        # for subscription, snapshots in snapshot_list.items():
        #     for snapshot in snapshots:
        #         print(snapshot)
        response.extend(self.remove_old_vm_disk_snapshot(snapshot_list))
        #
        response.extend(self.azure_advisor_recommendations(subscriptions))

        nsg_list = self.list_nsg(subscriptions)
        # print('nsg list')
        # print(nsg_list)
        response.extend(self.unrestricted_access(nsg_list))

        resource_groups = self.list_resource_groups(subscriptions)
        reservation_recommendations = self.get_reservation_recommendations(resource_groups)

        return response, reservation_recommendations


def get_token(tenant_id, client_id, client_secret) -> str:
    url = "https://login.microsoftonline.com/{}/oauth2/token".format(tenant_id)

    payload = 'grant_type=client_credentials&client_id={}&client_secret={}&resource=https%3A%2F%2Fmanagement.azure.com%2F'.format(client_id, client_secret)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'esctx=PAQABAAEAAAD--DLA3VO7QrddgJg7WevrsyLaTCnWBlfoOEwgEXsbqS6Vk56KJ3f98q4z6wNlD--zONSvPVI_ibZKS8_wcOAqwZYLHwKN1GlMFbChMq1wm9rcpBVNHewxS2ycllzLyDHDniE5l2CFhq88TdEeXS_8JEtBzZT5M2tx9yGb8xOGq4QKBbhOcX6b5Ry-grf0N4yPcxz-dNbt4yri8DshwtoeVuFOeuOvXLRLsk-MVITGzmuMMNbZrNq8JZv_VVzyatwgAA; fpc=Ai2uF3w6uI5OvoKy3lAO3CE6T-WgAQAAAPonotsOAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)

    return data['access_token']
