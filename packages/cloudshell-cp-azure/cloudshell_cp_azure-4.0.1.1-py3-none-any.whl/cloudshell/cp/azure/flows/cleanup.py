import logging
import typing
from functools import partial
from http import HTTPStatus

from azure.mgmt.network import models as network_models
from msrestazure.azure_exceptions import CloudError

from cloudshell.cp.core.flows.cleanup_sandbox_infra import (
    AbstractCleanupSandboxInfraFlow,
)

from cloudshell.cp.azure.actions.network import NetworkActions
from cloudshell.cp.azure.actions.network_security_group import (
    NetworkSecurityGroupActions,
)
from cloudshell.cp.azure.actions.resource_group import ResourceGroupActions
from cloudshell.cp.azure.actions.ssh_key_pair import SSHKeyPairActions
from cloudshell.cp.azure.actions.storage_account import StorageAccountActions


class AzureCleanupSandboxInfraFlow(AbstractCleanupSandboxInfraFlow):
    def __init__(
        self,
        resource_config,
        azure_client,
        reservation_info,
        lock_manager,
        logger: logging.Logger,
    ):
        super().__init__(logger=logger)
        self._resource_config = resource_config
        self._azure_client = azure_client
        self._reservation_info = reservation_info
        self._lock_manager = lock_manager

    def _find_sandbox_subnets(
        self, resource_group_name: str, sandbox_vnet: network_models.VirtualNetwork
    ) -> typing.List[network_models.Subnet]:
        """Find the sandbox subnet in the vNet."""
        # todo: rework this using some special tags ?
        return [
            subnet
            for subnet in sandbox_vnet.subnets
            if subnet.name.startswith(resource_group_name)
        ]

    def cleanup_sandbox_infra(self, request_actions):
        """Cleanp Sandbox Infra.

        :param request_actions:
        :return:
        """
        resource_group_name = self._reservation_info.get_resource_group_name()
        nsg_name = self._reservation_info.get_network_security_group_name()
        storage_account_name = self._reservation_info.get_storage_account_name()

        network_actions = NetworkActions(
            azure_client=self._azure_client, logger=self._logger
        )
        resource_group_actions = ResourceGroupActions(
            azure_client=self._azure_client, logger=self._logger
        )
        nsg_actions = NetworkSecurityGroupActions(
            azure_client=self._azure_client, logger=self._logger
        )
        storage_actions = StorageAccountActions(
            azure_client=self._azure_client, logger=self._logger
        )
        ssh_key_actions = SSHKeyPairActions(
            azure_client=self._azure_client, logger=self._logger
        )

        self._lock_manager.remove_lock(nsg_name)

        sandbox_vnet = network_actions.get_sandbox_virtual_network(
            resource_group_name=self._resource_config.management_group_name,
            sandbox_vnet_name=self._resource_config.sandbox_vnet_name,
        )

        cleanup_commands = []

        for subnet in network_actions.get_sandbox_subnets(
            resource_group_name=resource_group_name,
            mgmt_resource_group_name=self._resource_config.management_group_name,
            sandbox_vnet_name=self._resource_config.sandbox_vnet_name,
        ):
            cleanup_commands.append(
                partial(
                    network_actions.delete_subnet,
                    subnet_name=subnet.name,
                    vnet_name=sandbox_vnet.name,
                    resource_group_name=self._resource_config.management_group_name,
                )
            )

        if nsg_actions.network_security_group_exists(
            nsg_name=nsg_name, resource_group_name=resource_group_name
        ):
            cleanup_commands.append(
                partial(
                    nsg_actions.delete_network_security_group,
                    nsg_name=nsg_name,
                    resource_group_name=resource_group_name,
                )
            )

        cleanup_commands.append(
            partial(
                ssh_key_actions.delete_ssh_public_key,
                public_key_name=self._reservation_info.reservation_id,
                resource_group_name=resource_group_name,
            )
        )

        cleanup_commands.append(
            partial(
                ssh_key_actions.delete_ssh_private_key,
                key_vault_name=self._resource_config.key_vault,
                private_key_name=self._reservation_info.reservation_id,
            )
        )

        cleanup_commands.append(
            partial(
                storage_actions.delete_storage_account,
                storage_account_name=storage_account_name,
                resource_group_name=resource_group_name,
            )
        )

        cleanup_commands.append(
            partial(
                resource_group_actions.delete_resource_group,
                resource_group_name=resource_group_name,
            )
        )

        for cleanup_command in cleanup_commands:
            try:
                cleanup_command()
            except CloudError as e:
                if e.status_code == HTTPStatus.NOT_FOUND:
                    self._logger.warning(
                        "Unable to find resource on Azure for deleting:", exc_info=True
                    )
                    continue
                raise
