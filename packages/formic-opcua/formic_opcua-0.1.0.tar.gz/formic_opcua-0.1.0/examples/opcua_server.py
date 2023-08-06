# Copyright Formic Technologies 2023
import asyncio
import logging
import sys

from formic_opcua import OpcuaServer

asyncua_logger = logging.getLogger('asyncua')
asyncua_logger.setLevel(logging.ERROR)

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(funcName)s:%(lineno)d | %(message)s',
)


def main():
    config_file_path = '../examples/example_configs/opcua_config_1.yaml'
    server = OpcuaServer(server_config_file=config_file_path)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.create_task(server.start())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(server.stop())
    finally:
        loop.close()


if __name__ == '__main__':
    main()
