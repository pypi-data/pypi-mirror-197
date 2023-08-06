import dataclasses
import ipaddress
from typing import Union

from anyscale.cli_logger import BlockLogger


@dataclasses.dataclass
class CapacityThreshold:
    min_network_size: Union[ipaddress.IPv4Network, ipaddress.IPv6Network]
    warn_network_size: Union[ipaddress.IPv4Network, ipaddress.IPv6Network]
    resource_type: str

    def verify_network_capacity(
        self, *, cidr_block_str: str, resource_name: str, logger: BlockLogger
    ) -> bool:
        cidr_block = ipaddress.ip_network(cidr_block_str, strict=False)

        min_hosts = self.min_network_size.num_addresses
        warn_hosts = self.warn_network_size.num_addresses

        if cidr_block.num_addresses < min_hosts:
            logger.error(
                f"The provided {self.resource_type} ({resource_name})'s CIDR block ({cidr_block}) is too"
                f" small. We want at least {min_hosts} addresses,"
                f" but this {self.resource_type} only has {cidr_block.num_addresses}. Please reach out to"
                f" support if this is an issue!"
            )
            return False
        elif cidr_block.num_addresses < warn_hosts:
            logger.warning(
                f"The provided {self.resource_type} ({resource_name})'s CIDR block ({cidr_block}) is probably"
                f" too small. We suggest at least {warn_hosts}"
                f" addresses, but this {self.resource_type} only supports up to"
                f" {cidr_block.num_addresses} addresses."
            )

        return True


AWS_VPC_CAPACITY = CapacityThreshold(
    min_network_size=ipaddress.ip_network("10.0.0.0/24"),
    warn_network_size=ipaddress.ip_network("10.0.0.0/20"),
    resource_type="VPC",
)

AWS_SUBNET_CAPACITY = CapacityThreshold(
    min_network_size=ipaddress.ip_network("10.0.0.0/28"),
    warn_network_size=ipaddress.ip_network("10.0.0.0/24"),
    resource_type="Subnet",
)

GCP_SUBNET_CAPACITY = dataclasses.replace(AWS_VPC_CAPACITY, resource_type="Subnet")
