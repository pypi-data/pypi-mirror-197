from typing import Dict

from cloudshell.cp.core.flows.prepare_sandbox_infra import (
    AbstractPrepareSandboxInfraFlow,
)

from cloudshell.cp.azure.actions.network import NetworkActions
from cloudshell.cp.azure.actions.network_security_group import (
    NetworkSecurityGroupActions,
)
from cloudshell.cp.azure.actions.resource_group import ResourceGroupActions
from cloudshell.cp.azure.actions.ssh_key_pair import SSHKeyPairActions
from cloudshell.cp.azure.actions.storage_account import StorageAccountActions
from cloudshell.cp.azure.constants import (
    SUBNET_SERVICE_NAME_ATTRIBUTE,
    VNET_SERVICE_NAME_ATTRIBUTE,
)
from cloudshell.cp.azure.exceptions import InvalidAttrException
from cloudshell.cp.azure.flows.prepare_sandbox_infra import commands
from cloudshell.cp.azure.utils.nsg_rules_priority_generator import (
    NSGRulesPriorityGenerator,
)
from cloudshell.cp.azure.utils.rollback import RollbackCommandsManager
from cloudshell.cp.azure.utils.tags import AzureTagsManager


class AzurePrepareSandboxInfraFlow(AbstractPrepareSandboxInfraFlow):
    def __init__(
        self,
        resource_config,
        azure_client,
        reservation_info,
        cancellation_manager,
        logger,
    ):
        """Init command.

        :param resource_config:
        :param azure_client:
        :param reservation_info:
        :param cancellation_manager:
        :param logger:
        """
        super().__init__(logger=logger)
        self._resource_config = resource_config
        self._azure_client = azure_client
        self._reservation_info = reservation_info
        self._cancellation_manager = cancellation_manager
        self._rollback_manager = RollbackCommandsManager(logger=self._logger)
        self._tags_manager = AzureTagsManager(
            reservation_info=self._reservation_info, resource_config=resource_config
        )

    def prepare_cloud_infra(self, request_actions):
        pass

    def prepare_common_objects(self, request_actions):
        """Prepare common objects.

        :param request_actions:
        :return:
        """
        tags = self._tags_manager.get_reservation_tags()
        resource_group_name = self._reservation_info.get_resource_group_name()
        resource_group_actions = ResourceGroupActions(
            azure_client=self._azure_client, logger=self._logger
        )

        with self._rollback_manager:
            self._create_resource_group(
                resource_group_actions=resource_group_actions,
                resource_group_name=resource_group_name,
                tags=tags,
            )

    def prepare_subnets(self, request_actions):
        """Prepare subnets.

        :param request_actions:
        :return:
        """
        resource_group_name = self._reservation_info.get_resource_group_name()
        nsg_name = self._reservation_info.get_network_security_group_name()
        tags = self._tags_manager.get_reservation_tags()
        nsg = None
        all_subnets_are_predefined = all(
            [
                subnet_action.get_attribute(name=SUBNET_SERVICE_NAME_ATTRIBUTE)
                for subnet_action in request_actions.prepare_subnets
            ]
        )

        with self._rollback_manager:
            if not all_subnets_are_predefined:
                nsg = self._create_nsg(
                    nsg_name=nsg_name,
                    resource_group_name=resource_group_name,
                    tags=tags,
                )

                self._create_nsg_rules(
                    request_actions=request_actions,
                    resource_group_name=resource_group_name,
                    nsg_name=nsg_name,
                )

            return self._create_subnets(
                request_actions=request_actions,
                resource_group_name=resource_group_name,
                network_security_group=nsg,
            )

    def create_ssh_keys(self, request_actions):
        """Create SSH public and private keys.

        :param request_actions:
        :return: SSH Access key
        :rtype: str
        """
        resource_group_name = self._reservation_info.get_resource_group_name()
        tags = self._tags_manager.get_reservation_tags()

        with self._rollback_manager:
            ssh_actions = SSHKeyPairActions(
                azure_client=self._azure_client, logger=self._logger
            )

            private_key, public_key = ssh_actions.create_ssh_key_pair()

            self._create_ssh_public_key(
                public_key=public_key,
                resource_group_name=resource_group_name,
                tags=tags,
            )

            if self._resource_config.key_vault:
                self._create_ssh_private_key(
                    key_vault_name=self._resource_config.key_vault,
                    private_key=private_key,
                    tags=tags,
                )

            return private_key

    def _create_resource_group(self, resource_group_actions, resource_group_name, tags):
        """Create Resource Group.

        :param resource_group_actions:
        :param str resource_group_name:
        :param dict[str, str] tags:
        :return:
        """
        commands.CreateResourceGroupCommand(
            rollback_manager=self._rollback_manager,
            cancellation_manager=self._cancellation_manager,
            resource_group_actions=resource_group_actions,
            resource_group_name=resource_group_name,
            region=self._resource_config.region,
            tags=tags,
        ).execute()

    def _create_nsg(self, nsg_name, resource_group_name, tags):
        """Create Network Security Group.

        :param str nsg_name:
        :param str resource_group_name:
        :param dict[str, str] tags:
        :return:
        """
        nsg_actions = NetworkSecurityGroupActions(
            azure_client=self._azure_client, logger=self._logger
        )

        return commands.CreateNSGCommand(
            rollback_manager=self._rollback_manager,
            cancellation_manager=self._cancellation_manager,
            nsg_actions=nsg_actions,
            nsg_name=nsg_name,
            resource_group_name=resource_group_name,
            region=self._resource_config.region,
            tags=tags,
        ).execute()

    def _create_nsg_allow_sandbox_traffic_to_subnet_rules(
        self, request_actions, nsg_name, resource_group_name, rules_priority_generator
    ):
        """Create NSG allow Sandbox traffic to subnet rules.

        :param request_actions:
        :param str nsg_name:
        :param str resource_group_name:
        :return:
        """
        nsg_actions = NetworkSecurityGroupActions(
            azure_client=self._azure_client, logger=self._logger
        )

        for action in request_actions.prepare_subnets:
            commands.CreateAllowSandboxTrafficToSubnetRuleCommand(
                rollback_manager=self._rollback_manager,
                cancellation_manager=self._cancellation_manager,
                nsg_actions=nsg_actions,
                nsg_name=nsg_name,
                resource_group_name=resource_group_name,
                sandbox_cidr=request_actions.sandbox_cidr,
                subnet_cidr=action.get_cidr(),
                rules_priority_generator=rules_priority_generator,
            ).execute()

    def _create_nsg_deny_access_to_private_subnet_rules(
        self, request_actions, nsg_name, resource_group_name, rules_priority_generator
    ):
        """Create NSG deny access to private subnet rules.

        :param request_actions:
        :param str nsg_name:
        :param str resource_group_name:
        :return:
        """
        nsg_actions = NetworkSecurityGroupActions(
            azure_client=self._azure_client, logger=self._logger
        )

        for action in request_actions.prepare_private_subnets:
            commands.CreateDenyAccessToPrivateSubnetRuleCommand(
                rollback_manager=self._rollback_manager,
                cancellation_manager=self._cancellation_manager,
                nsg_actions=nsg_actions,
                nsg_name=nsg_name,
                resource_group_name=resource_group_name,
                sandbox_cidr=request_actions.sandbox_cidr,
                subnet_cidr=action.get_cidr(),
                rules_priority_generator=rules_priority_generator,
            ).execute()

    def _create_nsg_additional_mgmt_networks_rules(
        self, request_actions, nsg_name, resource_group_name, rules_priority_generator
    ):
        """Create NSG rules for the additional MGMT networks.

        :param request_actions:
        :param str nsg_name:
        :param str resource_group_name:
        :return:
        """
        nsg_actions = NetworkSecurityGroupActions(
            azure_client=self._azure_client, logger=self._logger
        )

        for mgmt_network in self._resource_config.additional_mgmt_networks:
            commands.CreateAdditionalMGMTNetworkRuleCommand(
                rollback_manager=self._rollback_manager,
                cancellation_manager=self._cancellation_manager,
                nsg_actions=nsg_actions,
                nsg_name=nsg_name,
                resource_group_name=resource_group_name,
                mgmt_network=mgmt_network,
                sandbox_cidr=request_actions.sandbox_cidr,
                rules_priority_generator=rules_priority_generator,
            ).execute()

    def _create_nsg_allow_mgmt_vnet_rule(
        self, request_actions, nsg_name, resource_group_name, rules_priority_generator
    ):
        """Create NSG allow MGMT vNET rule.

        :param request_actions:
        :param str nsg_name:
        :param str resource_group_name:
        :return:
        """
        nsg_actions = NetworkSecurityGroupActions(
            azure_client=self._azure_client, logger=self._logger
        )
        network_actions = NetworkActions(
            azure_client=self._azure_client, logger=self._logger
        )

        if network_actions.mgmt_virtual_network_exists(
            self._resource_config.management_group_name
        ):
            commands.CreateAllowMGMTVnetRuleCommand(
                rollback_manager=self._rollback_manager,
                cancellation_manager=self._cancellation_manager,
                mgmt_resource_group_name=self._resource_config.management_group_name,
                resource_group_name=resource_group_name,
                network_actions=network_actions,
                nsg_actions=nsg_actions,
                nsg_name=nsg_name,
                sandbox_cidr=request_actions.sandbox_cidr,
                rules_priority_generator=rules_priority_generator,
            ).execute()

    def _create_nsg_deny_traffic_from_other_sandboxes_rule(
        self, request_actions, nsg_name, resource_group_name, rules_priority_generator
    ):
        """Create NSG deny traffic from other sandboxes rule.

        :param request_actions:
        :param str nsg_name:
        :param str resource_group_name:
        :return:
        """
        nsg_actions = NetworkSecurityGroupActions(
            azure_client=self._azure_client, logger=self._logger
        )
        network_actions = NetworkActions(
            azure_client=self._azure_client, logger=self._logger
        )

        commands.CreateDenyTrafficFromOtherSandboxesRuleCommand(
            rollback_manager=self._rollback_manager,
            cancellation_manager=self._cancellation_manager,
            mgmt_resource_group_name=self._resource_config.management_group_name,
            sandbox_vnet_name=self._resource_config.sandbox_vnet_name,
            resource_group_name=resource_group_name,
            network_actions=network_actions,
            nsg_actions=nsg_actions,
            sandbox_cidr=request_actions.sandbox_cidr,
            nsg_name=nsg_name,
            rules_priority_generator=rules_priority_generator,
        ).execute()

    def _create_nsg_rules(self, request_actions, resource_group_name, nsg_name):
        """Create all required NSG rules.

        :param request_actions:
        :param str resource_group_name:
        :param str nsg_name:
        :return:
        """
        rules_priority_generator = NSGRulesPriorityGenerator(
            nsg_name=nsg_name, resource_group_name=resource_group_name
        )

        self._create_nsg_allow_sandbox_traffic_to_subnet_rules(
            request_actions=request_actions,
            nsg_name=nsg_name,
            resource_group_name=resource_group_name,
            rules_priority_generator=rules_priority_generator,
        )

        self._create_nsg_deny_access_to_private_subnet_rules(
            request_actions=request_actions,
            nsg_name=nsg_name,
            resource_group_name=resource_group_name,
            rules_priority_generator=rules_priority_generator,
        )

        self._create_nsg_additional_mgmt_networks_rules(
            request_actions=request_actions,
            nsg_name=nsg_name,
            resource_group_name=resource_group_name,
            rules_priority_generator=rules_priority_generator,
        )

        self._create_nsg_allow_mgmt_vnet_rule(
            request_actions=request_actions,
            nsg_name=nsg_name,
            resource_group_name=resource_group_name,
            rules_priority_generator=rules_priority_generator,
        )

        self._create_nsg_deny_traffic_from_other_sandboxes_rule(
            request_actions=request_actions,
            nsg_name=nsg_name,
            resource_group_name=resource_group_name,
            rules_priority_generator=rules_priority_generator,
        )

    def _create_subnets(
        self, request_actions, resource_group_name, network_security_group=None
    ):
        """Create additional subnets requested by server.

        :param request_actions:
        :param str resource_group_name:
        :param network_security_group:
        :return:
        """
        network_actions = NetworkActions(
            azure_client=self._azure_client, logger=self._logger
        )
        subnet_result = {}

        with self._cancellation_manager:
            sandbox_vnet = network_actions.get_sandbox_virtual_network(
                resource_group_name=self._resource_config.management_group_name,
                sandbox_vnet_name=self._resource_config.sandbox_vnet_name,
            )

        for subnet_action in request_actions.prepare_subnets:
            predefined_subnet_name = subnet_action.get_attribute(
                name=SUBNET_SERVICE_NAME_ATTRIBUTE
            )
            subnet_vnet = sandbox_vnet
            resource_group = self._resource_config.management_group_name

            vnet = subnet_action.get_attribute(name=VNET_SERVICE_NAME_ATTRIBUTE)
            if vnet:
                if not predefined_subnet_name:
                    raise InvalidAttrException(
                        f"Custom VNet could be used only with predefined subnet. "
                        f"Please populate '{SUBNET_SERVICE_NAME_ATTRIBUTE}' "
                        f"attribute on Subnet service "
                        f"with an appropriate value."
                    )
                if "/" in vnet:
                    resource_group, vnet = vnet.split("/")
                subnet_vnet = network_actions.get_sandbox_virtual_network(
                    resource_group_name=resource_group,
                    sandbox_vnet_name=vnet,
                )
            self._logger.info(
                f"Adding Subnet {predefined_subnet_name or subnet_action.get_cidr()} "
                f"in vnet {subnet_vnet.name} in resource group {resource_group}"
            )
            if predefined_subnet_name:
                subnet = network_actions.find_sandbox_subnet_by_name(
                    sandbox_subnets=subnet_vnet.subnets,
                    name_reqexp=predefined_subnet_name,
                    resource_group_name=resource_group,
                )
            else:
                subnet = commands.CreateSubnetCommand(
                    rollback_manager=self._rollback_manager,
                    cancellation_manager=self._cancellation_manager,
                    network_actions=network_actions,
                    cidr=subnet_action.get_cidr(),
                    vnet=subnet_vnet,
                    resource_group_name=resource_group_name,
                    mgmt_resource_group_name=resource_group,  # noqa E501
                    network_security_group=network_security_group,
                ).execute()

            subnet_result[subnet_action.actionId] = subnet.name

        return subnet_result

    def _create_storage_account(self, storage_account_name, resource_group_name, tags):
        """Create Storage Account.

        :param str storage_account_name:
        :param str resource_group_name:
        :param dict[str, str] tags:
        :return:
        """
        storage_actions = StorageAccountActions(
            azure_client=self._azure_client, logger=self._logger
        )

        commands.CreateSandboxStorageAccountCommand(
            rollback_manager=self._rollback_manager,
            cancellation_manager=self._cancellation_manager,
            storage_actions=storage_actions,
            storage_account_name=storage_account_name,
            resource_group_name=resource_group_name,
            region=self._resource_config.region,
            tags=tags,
        ).execute()

    def _create_ssh_public_key(
        self,
        public_key: str,
        resource_group_name: str,
        tags: Dict[str, str],
    ):
        """Save SSH public key on the Azure."""
        ssh_actions = SSHKeyPairActions(
            azure_client=self._azure_client, logger=self._logger
        )

        commands.SaveSSHPublicKeyCommand(
            rollback_manager=self._rollback_manager,
            cancellation_manager=self._cancellation_manager,
            resource_group_name=resource_group_name,
            public_key_name=self._reservation_info.reservation_id,
            public_key=public_key,
            ssh_actions=ssh_actions,
            region=self._resource_config.region,
            tags=tags,
        ).execute()

    def _create_ssh_private_key(
        self,
        key_vault_name: str,
        private_key: str,
        tags: Dict[str, str],
    ):
        """Save SSH private key on the Azure."""
        ssh_actions = SSHKeyPairActions(
            azure_client=self._azure_client, logger=self._logger
        )

        commands.SaveSSHPrivateKeyCommand(
            rollback_manager=self._rollback_manager,
            cancellation_manager=self._cancellation_manager,
            ssh_actions=ssh_actions,
            key_vault_name=key_vault_name,
            private_key_name=self._reservation_info.reservation_id,
            private_key=private_key,
            tags=tags,
        ).execute()
