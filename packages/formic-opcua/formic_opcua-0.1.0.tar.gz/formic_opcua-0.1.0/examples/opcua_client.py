# Copyright Formic Technologies 2023
import logging
import sys

from formic_opcua import OpcuaClient

# Configure asyncua library log level
asyncua_logger = logging.getLogger('asyncua')
asyncua_logger.setLevel(logging.CRITICAL)


# Basic handler for opcua library
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(funcName)s:%(lineno)d | %(message)s',
)


def main() -> None:
    config_file_name = '../examples/example_configs/opcua_config_1.yaml'
    with OpcuaClient(server_config_file=config_file_name) as client:
        for i in range(10):
            # client.write(
            #     path='formic/device_type/PLC/device/SYS1_PLC1/connection/connection_status',
            #     value=i,
            # )
            client.write(
                path='formic/device_type/PLC/device/SYS1_PLC1/states/critical_system_statuses/level_1_errors',
                value=i,
            )
            client.read(
                path='formic/device_type/PLC/device/SYS1_PLC1/states/critical_system_statuses/level_1_errors',
            )
            all_variables = client.read_all()
            print(all_variables)
            print(i)


if __name__ == '__main__':
    main()
